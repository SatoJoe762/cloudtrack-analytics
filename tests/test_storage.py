from io import BytesIO
import boto3
import pytest
from botocore.response import StreamingBody
from botocore.stub import Stubber
from cloudtrack.storage import read_s3_orders


def test_s3_reads_exact_configured_object_and_closes_stream(monkeypatch):
    client = boto3.client('s3', region_name='us-east-1', aws_access_key_id='testing', aws_secret_access_key='testing')
    body = StreamingBody(BytesIO(b'example'), 7)
    monkeypatch.setenv('CLOUDTRACK_S3_BUCKET', 'cloudtrack-test')
    monkeypatch.setenv('CLOUDTRACK_S3_KEY', 'raw/orders.csv')
    monkeypatch.setattr('cloudtrack.storage.boto3.client', lambda *args, **kwargs: client)
    with Stubber(client) as stub:
        stub.add_response('get_object', {'Body': body, 'ContentLength': 7}, {'Bucket': 'cloudtrack-test', 'Key': 'raw/orders.csv'})
        assert read_s3_orders() == b'example'
        assert body._raw_stream.closed
        stub.assert_no_pending_responses()


def test_s3_oversized_object_is_rejected_and_closed(monkeypatch):
    client = boto3.client('s3', region_name='us-east-1', aws_access_key_id='testing', aws_secret_access_key='testing')
    body = StreamingBody(BytesIO(b''), 11 * 1024 * 1024)
    monkeypatch.setenv('CLOUDTRACK_S3_BUCKET', 'cloudtrack-test')
    monkeypatch.setenv('CLOUDTRACK_S3_KEY', 'raw/orders.csv')
    monkeypatch.setattr('cloudtrack.storage.boto3.client', lambda *args, **kwargs: client)
    with Stubber(client) as stub:
        stub.add_response('get_object', {'Body': body, 'ContentLength': 11 * 1024 * 1024})
        with pytest.raises(ValueError, match='10 MB'):
            read_s3_orders()
        assert body._raw_stream.closed


def test_s3_missing_configuration(monkeypatch):
    monkeypatch.delenv('CLOUDTRACK_S3_BUCKET', raising=False)
    with pytest.raises(ValueError, match='CLOUDTRACK_S3_BUCKET'):
        read_s3_orders()


def test_r2_uses_custom_endpoint_auto_region_and_read_only_get(monkeypatch):
    endpoint = 'https://0123456789abcdef0123456789abcdef.r2.cloudflarestorage.com'
    client = boto3.client('s3', endpoint_url=endpoint, region_name='auto',
                          aws_access_key_id='testing', aws_secret_access_key='testing')
    body = StreamingBody(BytesIO(b'orders'), 6)
    calls = []

    def create_client(*args, **kwargs):
        calls.append((args, kwargs))
        return client

    monkeypatch.setenv('CLOUDTRACK_S3_BUCKET', 'cloudtrack-datos')
    monkeypatch.setenv('CLOUDTRACK_S3_KEY', 'raw/orders.csv')
    monkeypatch.setenv('CLOUDTRACK_S3_ENDPOINT', endpoint)
    monkeypatch.setattr('cloudtrack.storage.boto3.client', create_client)
    with Stubber(client) as stub:
        stub.add_response('get_object', {'Body': body, 'ContentLength': 6},
                          {'Bucket': 'cloudtrack-datos', 'Key': 'raw/orders.csv'})
        assert read_s3_orders() == b'orders'
        stub.assert_no_pending_responses()
    assert body._raw_stream.closed
    assert calls[0][0] == ('s3',)
    assert calls[0][1]['endpoint_url'] == endpoint
    assert calls[0][1]['region_name'] == 'auto'


@pytest.mark.parametrize('endpoint', [
    'http://test.r2.cloudflarestorage.com',
    'https://example.org',
    'https://test.r2.cloudflarestorage.com.attacker.example',
    'https://user:secret@test.r2.cloudflarestorage.com',
    'https://test.r2.cloudflarestorage.com/raw/orders.csv',
    'https://test.r2.cloudflarestorage.com?token=private',
    'https://test.r2.cloudflarestorage.com#fragment',
    'https://test.r2.cloudflarestorage.com:invalid',
])
def test_r2_invalid_endpoint_is_rejected_before_using_credentials(monkeypatch, endpoint):
    monkeypatch.setenv('CLOUDTRACK_S3_BUCKET', 'cloudtrack-datos')
    monkeypatch.setenv('CLOUDTRACK_S3_ENDPOINT', endpoint)

    def unexpected_client(*args, **kwargs):
        pytest.fail('No debe crearse un cliente con un endpoint inválido')

    monkeypatch.setattr('cloudtrack.storage.boto3.client', unexpected_client)
    with pytest.raises(ValueError, match='endpoint HTTPS'):
        read_s3_orders()
