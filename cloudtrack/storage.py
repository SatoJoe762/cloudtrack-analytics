"""Lectura de un objeto privado de Cloudflare R2 mediante su API compatible con S3."""
import os
from urllib.parse import urlsplit
import boto3
from botocore.config import Config


class R2ConfigurationError(ValueError):
    """Falta la configuración de R2 en el entorno que ejecuta el panel."""


def read_r2_orders() -> bytes:
    bucket = os.environ.get("CLOUDTRACK_S3_BUCKET", "")
    key = os.environ.get("CLOUDTRACK_S3_KEY", "raw/orders.csv")
    if not bucket:
        raise R2ConfigurationError("Falta configurar el bucket de Cloudflare R2.")
    endpoint = os.environ.get("CLOUDTRACK_S3_ENDPOINT", "").strip()
    if not endpoint:
        raise R2ConfigurationError("Falta configurar el endpoint de Cloudflare R2.")
    try:
        url = urlsplit(endpoint)
        valid = (
            url.scheme == "https" and url.hostname
            and url.hostname.endswith(".r2.cloudflarestorage.com")
            and url.port in (None, 443)
            and not url.username and not url.password
            and url.path in ("", "/") and not url.query and not url.fragment
        )
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("CLOUDTRACK_S3_ENDPOINT debe ser el endpoint HTTPS de R2, sin bucket, ruta ni parámetros.")
    client_options = {"endpoint_url": endpoint, "region_name": "auto"}
    client = boto3.client("s3", **client_options, config=Config(
        connect_timeout=5, read_timeout=15, retries={"max_attempts": 2}
    ))
    response = client.get_object(Bucket=bucket, Key=key)
    body = response["Body"]
    try:
        if response.get("ContentLength", 0) > 10 * 1024 * 1024:
            raise ValueError("El objeto cloud supera el límite de 10 MB.")
        content = body.read(10 * 1024 * 1024 + 1)
        if len(content) > 10 * 1024 * 1024:
            raise ValueError("El objeto cloud supera el límite de 10 MB.")
        return content
    finally:
        body.close()
