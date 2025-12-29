#!/usr/bin/env python
"""Teste completo de push notifications com detalhes"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'painel.settings')
django.setup()

from django.contrib.auth import get_user_model
from rondonopolis.models import PreferenciaNotificacaoUsuario
from django.conf import settings

User = get_user_model()

print("=" * 70)
print("TESTE COMPLETO DE PUSH NOTIFICATIONS")
print("=" * 70)

# 1. Verificar usuário com subscription
print("\n1. Verificando subscription do usuário...")
usuarios = PreferenciaNotificacaoUsuario.objects.filter(
    push_subscription__isnull=False
).exclude(push_subscription='')

if not usuarios.exists():
    print("❌ Nenhum usuário com subscription encontrado!")
    print("   Configure as notificações push em: Configurações e Perfil")
    exit(1)

for pref in usuarios:
    print(f"\n✅ Usuário: {pref.usuario.username}")
    print(f"   Email: {pref.usuario.email or 'sem email'}")
    print(f"   Receber navegador: {pref.receber_navegador}")
    
    # Verificar subscription
    try:
        subscription = json.loads(pref.push_subscription)
        print(f"   ✅ Subscription válida")
        print(f"   Endpoint: {subscription.get('endpoint', 'N/A')[:50]}...")
        print(f"   Keys: {list(subscription.get('keys', {}).keys())}")
    except Exception as e:
        print(f"   ❌ Erro ao parsear subscription: {e}")
        continue
    
    # 2. Verificar VAPID keys
    print("\n2. Verificando VAPID keys...")
    vapid_public = getattr(settings, 'VAPID_PUBLIC_KEY', None)
    vapid_private = getattr(settings, 'VAPID_PRIVATE_KEY', None)
    
    if not vapid_public or not vapid_private:
        print("❌ VAPID keys não configuradas!")
        print("   Execute: python gerar_vapid_keys.py")
        print("   Adicione ao arquivo .env")
        continue
    else:
        print(f"   ✅ VAPID_PUBLIC_KEY: {vapid_public[:30]}...")
        print(f"   ✅ VAPID_PRIVATE_KEY: {vapid_private[:30]}...")
    
    # 3. Testar envio
    print("\n3. Testando envio de push notification...")
    try:
        from pywebpush import webpush, WebPushException
        
        payload_data = {
            'title': 'TLOGpainel - Teste',
            'body': 'Esta é uma notificação de teste do sistema',
            'icon': '/static/imagens/icone.png',
            'tag': 'teste-notification',
            'url': '/'
        }
        payload = json.dumps(payload_data)
        
        vapid_claims = getattr(settings, 'VAPID_CLAIMS', {
            "sub": "mailto:digitalmidia@transcamila.com.br"
        })
        
        print(f"   Enviando para: {subscription.get('endpoint', 'N/A')[:50]}...")
        print(f"   Payload: {payload[:100]}...")
        
        webpush(
            subscription_info=subscription,
            data=payload,
            vapid_private_key=vapid_private,
            vapid_claims=vapid_claims
        )
        
        print("   ✅ Push notification enviada com sucesso!")
        print("\n   ⚠️  IMPORTANTE:")
        print("   - Verifique se o navegador está aberto")
        print("   - Verifique se o Service Worker está registrado")
        print("   - Verifique o console do navegador (F12) para logs")
        print("   - A notificação deve aparecer mesmo com o site fechado")
        
    except WebPushException as e:
        print(f"   ❌ Erro WebPush: {e}")
        if "410" in str(e) or "expired" in str(e).lower():
            print("   ⚠️  Subscription expirada ou inválida")
            print("   💡 Solução: Reative as notificações push nas configurações")
        elif "401" in str(e) or "unauthorized" in str(e).lower():
            print("   ⚠️  Erro de autenticação VAPID")
            print("   💡 Solução: Verifique se as chaves VAPID estão corretas no .env")
        else:
            print(f"   💡 Detalhes: {str(e)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("TESTE CONCLUÍDO")
print("=" * 70)







