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
