#!/usr/bin/env python
"""Script para gerar chaves VAPID para Web Push"""
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import base64

# Gerar chave privada
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

# Obter chave pública
public_key = private_key.public_key()

# Obter números públicos (x, y) da curva elíptica
public_numbers = public_key.public_numbers()
x = public_numbers.x
y = public_numbers.y

# Converter para bytes (32 bytes cada, total 65 bytes com prefixo 0x04)
x_bytes = x.to_bytes(32, 'big')
y_bytes = y.to_bytes(32, 'big')
public_key_bytes = b'\x04' + x_bytes + y_bytes

# Obter chave privada em bytes
private_key_bytes = private_key.private_numbers().private_value.to_bytes(32, 'big')

# Converter para base64 URL-safe (sem padding)
public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip('=')
private_key_b64 = base64.urlsafe_b64encode(private_key_bytes).decode('utf-8').rstrip('=')

print("=" * 60)
print("CHAVES VAPID GERADAS")
print("=" * 60)
print("\nAdicione estas variáveis ao seu arquivo .env:")
print(f"\nVAPID_PUBLIC_KEY={public_key_b64}")
print(f"VAPID_PRIVATE_KEY={private_key_b64}")
print("\n" + "=" * 60)
print("\nIMPORTANTE: Adicione essas chaves ao arquivo .env na raiz do projeto!")
