#!/usr/bin/env python
"""Script para testar push notifications"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'painel.settings')
django.setup()

from django.contrib.auth import get_user_model
from rondonopolis.models import PreferenciaNotificacaoUsuario
from rondonopolis.views import enviar_push_notification
from django.conf import settings

User = get_user_model()

print("=" * 60)
print("TESTE DE PUSH NOTIFICATIONS")
print("=" * 60)

# Verificar configurações VAPID
print("\n1. Verificando configurações VAPID...")
vapid_public = getattr(settings, 'VAPID_PUBLIC_KEY', None)
vapid_private = getattr(settings, 'VAPID_PRIVATE_KEY', None)

if not vapid_public:
    print("❌ ERRO: VAPID_PUBLIC_KEY não configurada no .env")
else:
    print(f"✅ VAPID_PUBLIC_KEY: {vapid_public[:20]}...")

if not vapid_private:
    print("❌ ERRO: VAPID_PRIVATE_KEY não configurada no .env")
else:
    print(f"✅ VAPID_PRIVATE_KEY: {vapid_private[:20]}...")

# Verificar pywebpush
print("\n2. Verificando biblioteca pywebpush...")
try:
    from pywebpush import webpush, WebPushException
    print("✅ pywebpush instalado")
except ImportError:
    print("❌ ERRO: pywebpush não instalado")
    print("   Execute: pip install pywebpush")

# Verificar usuários com subscription
print("\n3. Verificando usuários com subscription...")
usuarios_com_subscription = PreferenciaNotificacaoUsuario.objects.filter(
    push_subscription__isnull=False
).exclude(push_subscription='')

if usuarios_com_subscription.exists():
    print(f"✅ Encontrados {usuarios_com_subscription.count()} usuário(s) com subscription:")
    for pref in usuarios_com_subscription:
        print(f"   - {pref.usuario.username} ({pref.usuario.email or 'sem email'})")
        print(f"     Receber navegador: {pref.receber_navegador}")
        
        # Testar envio
        print(f"\n4. Testando envio de push notification para {pref.usuario.username}...")
        try:
            resultado = enviar_push_notification(
                pref.usuario,
                "Teste de notificação push",
                "TLOGpainel - Teste"
            )
            if resultado:
                print("✅ Push notification enviada com sucesso!")
            else:
                print("❌ Falha ao enviar push notification")
        except Exception as e:
            print(f"❌ ERRO ao enviar: {e}")
            import traceback
            traceback.print_exc()
else:
    print("⚠️  Nenhum usuário com subscription encontrado")
    print("   Configure as notificações push em: Configurações e Perfil")

print("\n" + "=" * 60)







