#!/usr/bin/env python
"""Diagnóstico completo do sistema de push notifications"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'painel.settings')
django.setup()

from django.contrib.auth import get_user_model
from rondonopolis.models import PreferenciaNotificacaoUsuario, ConfiguracaoNotificacao
from django.conf import settings

User = get_user_model()

print("=" * 80)
print("DIAGNÓSTICO COMPLETO - PUSH NOTIFICATIONS")
print("=" * 80)

# 1. Verificar usuários
print("\n1. VERIFICANDO USUÁRIOS E CONFIGURAÇÕES")
print("-" * 80)

usuarios_com_subscription = PreferenciaNotificacaoUsuario.objects.filter(
    push_subscription__isnull=False
).exclude(push_subscription='')

if not usuarios_com_subscription.exists():
    print("❌ NENHUM USUÁRIO COM SUBSCRIPTION ENCONTRADO!")
    print("\n   Isso significa que:")
    print("   - O usuário não ativou as notificações push")
    print("   - Ou o Service Worker não foi registrado corretamente")
    print("   - Ou a subscription não foi salva no banco")
    print("\n   SOLUÇÃO:")
    print("   1. Vá em Configurações e Perfil")
    print("   2. Ative o toggle 'Receber notificações push do navegador?'")
    print("   3. Clique em 'Clique aqui para ativar notificações push'")
    print("   4. Permita quando o navegador solicitar")
    exit(1)

for pref in usuarios_com_subscription:
    print(f"\n✅ Usuário: {pref.usuario.username}")
    print(f"   Email: {pref.usuario.email or 'sem email'}")
    print(f"   Receber navegador: {pref.receber_navegador}")
    
    # Verificar subscription
    try:
        subscription = json.loads(pref.push_subscription)
        print(f"   ✅ Subscription válida")
        endpoint = subscription.get('endpoint', '')
        print(f"   Endpoint: {endpoint[:60]}...")
        
        # Verificar se é Google FCM
        if 'fcm.googleapis.com' in endpoint:
            print(f"   ✅ Usando Google FCM (correto)")
        else:
            print(f"   ⚠️  Endpoint não é Google FCM: {endpoint[:50]}")
            
        keys = subscription.get('keys', {})
        if 'p256dh' in keys and 'auth' in keys:
            print(f"   ✅ Chaves de criptografia presentes")
        else:
            print(f"   ❌ Chaves de criptografia faltando!")
            
    except Exception as e:
        print(f"   ❌ Erro ao parsear subscription: {e}")
        continue

# 2. Verificar VAPID
print("\n2. VERIFICANDO CHAVES VAPID")
print("-" * 80)
vapid_public = getattr(settings, 'VAPID_PUBLIC_KEY', None)
vapid_private = getattr(settings, 'VAPID_PRIVATE_KEY', None)

if not vapid_public:
    print("❌ VAPID_PUBLIC_KEY não configurada!")
    print("   Execute: python gerar_vapid_keys.py")
    print("   Adicione ao arquivo .env")
    exit(1)
else:
    print(f"✅ VAPID_PUBLIC_KEY: {vapid_public[:40]}...")

if not vapid_private:
    print("❌ VAPID_PRIVATE_KEY não configurada!")
    print("   Execute: python gerar_vapid_keys.py")
    print("   Adicione ao arquivo .env")
    exit(1)
else:
    print(f"✅ VAPID_PRIVATE_KEY: {vapid_private[:40]}...")

# 3. Verificar pywebpush
print("\n3. VERIFICANDO BIBLIOTECA PYWEBPUSH")
print("-" * 80)
try:
    from pywebpush import webpush, WebPushException
    print("✅ pywebpush instalado")
except ImportError:
    print("❌ pywebpush NÃO instalado!")
    print("   Execute: pip install pywebpush")
    exit(1)

# 4. Testar envio real
print("\n4. TESTANDO ENVIO DE PUSH NOTIFICATION")
print("-" * 80)

for pref in usuarios_com_subscription:
    try:
        subscription = json.loads(pref.push_subscription)
        
        payload_data = {
            'title': 'TLOGpainel - Teste de Diagnóstico',
            'body': 'Se você recebeu isso, o sistema está funcionando!',
            'icon': '/static/imagens/icone.png',
            'tag': 'teste-diagnostico',
            'url': '/'
        }
        payload = json.dumps(payload_data)
        
        vapid_claims = getattr(settings, 'VAPID_CLAIMS', {
            "sub": "mailto:digitalmidia@transcamila.com.br"
        })
        
        print(f"\n   Enviando para {pref.usuario.username}...")
        print(f"   Endpoint: {subscription.get('endpoint', '')[:50]}...")
        
        webpush(
            subscription_info=subscription,
            data=payload,
            vapid_private_key=vapid_private,
            vapid_claims=vapid_claims
        )
        
        print(f"   ✅ Push notification ENVIADA com sucesso!")
        print(f"\n   ⚠️  IMPORTANTE:")
        print(f"   - Verifique se você está usando localhost ou HTTPS")
        print(f"   - Verifique se o navegador está aberto")
        print(f"   - Verifique o console do navegador (F12) para logs")
        print(f"   - A notificação deve aparecer em alguns segundos")
        
    except Exception as e:
        print(f"   ❌ ERRO ao enviar: {e}")
        import traceback
        traceback.print_exc()

# 5. Verificar grupos e usuários
print("\n5. VERIFICANDO GRUPOS E USUÁRIOS")
print("-" * 80)
from rondonopolis.models import GrupoUsuario

grupos = GrupoUsuario.objects.filter(ativo=True)
print(f"Grupos ativos: {grupos.count()}")
for grupo in grupos:
    usuarios_count = grupo.usuarios.filter(is_active=True).count()
    print(f"  - {grupo.get_nome_display()}: {usuarios_count} usuário(s)")

print("\n" + "=" * 80)
print("DIAGNÓSTICO CONCLUÍDO")
print("=" * 80)
print("\nPRÓXIMOS PASSOS:")
print("1. Se o teste enviou com sucesso mas você não recebeu:")
print("   - Verifique se está usando localhost (não IP de rede)")
print("   - Verifique permissões do navegador")
print("   - Verifique permissões do Windows")
print("\n2. Se deu erro no envio:")
print("   - Verifique os logs acima")
print("   - Verifique se as chaves VAPID estão corretas")
print("\n3. Se não tem subscription:")
print("   - Ative nas configurações do perfil")
print("   - Use localhost ao invés de IP de rede")







