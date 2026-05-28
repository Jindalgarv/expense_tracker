from pywebpush import WebPusher
import cryptography.hazmat.primitives.serialization as serialization
from cryptography.hazmat.backends import default_backend
import base64

with open('public_key.pem', 'rb') as f:
    key = serialization.load_pem_public_key(f.read(), backend=default_backend())

pub_bytes = key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)
print(base64.urlsafe_b64encode(pub_bytes).decode('utf-8').rstrip('='))
