#!/usr/bin/env python
"""Verificar se Service Worker está acessível"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'painel.settings')
django.setup()

from django.conf import settings
from pathlib import Path

print("=" * 70)
print("VERIFICAÇÃO DO SERVICE WORKER")
print("=" * 70)

# Verificar se arquivo existe
sw_path = Path(settings.BASE_DIR) / 'static' / 'sw.js'
print(f"\n1. Verificando arquivo Service Worker...")
if sw_path.exists():
    print(f"   ✅ Arquivo encontrado: {sw_path}")
    print(f"   Tamanho: {sw_path.stat().st_size} bytes")
    
    # Ler conteúdo
    with open(sw_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()
        if 'addEventListener' in conteudo and 'push' in conteudo:
            print(f"   ✅ Conteúdo válido (contém addEventListener e push)")
        else:
            print(f"   ❌ Conteúdo pode estar incorreto")
else:
    print(f"   ❌ Arquivo NÃO encontrado em: {sw_path}")

# Verificar configuração STATIC_URL
print(f"\n2. Verificando configuração estática...")
print(f"   STATIC_URL: {settings.STATIC_URL}")
print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"   DEBUG: {settings.DEBUG}")

# Verificar se está em HTTPS
print(f"\n3. Verificando ambiente...")
print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"   ⚠️  IMPORTANTE: Web Push só funciona em:")
print(f"      - HTTPS (produção)")
print(f"      - localhost (desenvolvimento)")
print(f"      - 127.0.0.1 (desenvolvimento)")

# Verificar VAPID keys
print(f"\n4. Verificando VAPID keys...")
vapid_public = getattr(settings, 'VAPID_PUBLIC_KEY', None)
vapid_private = getattr(settings, 'VAPID_PRIVATE_KEY', None)

if vapid_public and vapid_private:
    print(f"   ✅ VAPID keys configuradas")
else:
    print(f"   ❌ VAPID keys NÃO configuradas")

print("\n" + "=" * 70)
print("DIAGNÓSTICO:")
print("=" * 70)
print("\nSe você está em desenvolvimento:")
print("  - Use http://localhost:8000 ou http://127.0.0.1:8000")
print("  - NÃO use o IP da rede (ex: http://192.168.x.x:8000)")
print("\nSe você está em produção:")
print("  - Deve estar em HTTPS (https://)")
print("  - Service Worker só funciona em HTTPS ou localhost")







