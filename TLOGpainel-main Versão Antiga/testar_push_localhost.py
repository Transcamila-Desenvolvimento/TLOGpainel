#!/usr/bin/env python
"""
Script para testar push notifications no localhost
Execute este script para verificar se as notificações estão funcionando
"""
import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'painel.settings')
django.setup()

from django.contrib.auth import get_user_model
from rondonopolis.models import PreferenciaNotificacaoUsuario
from rondonopolis.views import enviar_push_notification
from django.conf import settings

User = get_user_model()

print("=" * 70)
print("🧪 TESTE DE PUSH NOTIFICATIONS - LOCALHOST")
print("=" * 70)

# 1. Verificar configurações VAPID
print("\n1️⃣ Verificando configurações VAPID...")
vapid_public = getattr(settings, 'VAPID_PUBLIC_KEY', None)
vapid_private = getattr(settings, 'VAPID_PRIVATE_KEY', None)

if not vapid_public:
    print("   ❌ ERRO: VAPID_PUBLIC_KEY não configurada!")
    print("   💡 Execute: python gerar_vapid_keys.py")
    print("   💡 Depois adicione as chaves no arquivo .env")
    exit(1)
else:
    print(f"   ✅ VAPID_PUBLIC_KEY configurada: {vapid_public[:30]}...")

if not vapid_private:
    print("   ❌ ERRO: VAPID_PRIVATE_KEY não configurada!")
    print("   💡 Execute: python gerar_vapid_keys.py")
    print("   💡 Depois adicione as chaves no arquivo .env")
    exit(1)
else:
    print(f"   ✅ VAPID_PRIVATE_KEY configurada: {vapid_private[:30]}...")

# 2. Verificar biblioteca pywebpush
print("\n2️⃣ Verificando biblioteca pywebpush...")
try:
    from pywebpush import webpush, WebPushException
    print("   ✅ pywebpush instalado")
except ImportError:
    print("   ❌ ERRO: pywebpush não instalado!")
    print("   💡 Execute: pip install pywebpush")
    exit(1)

# 3. Listar usuários com subscription
print("\n3️⃣ Buscando usuários com notificações ativadas...")
usuarios_com_subscription = PreferenciaNotificacaoUsuario.objects.filter(
    push_subscription__isnull=False,
    receber_navegador=True
).exclude(push_subscription='').select_related('usuario')

if not usuarios_com_subscription.exists():
    print("   ⚠️  Nenhum usuário encontrado com notificações ativadas!")
    print("   💡 Para ativar:")
    print("      1. Acesse o sistema no navegador (localhost:8000)")
    print("      2. Faça login com sua conta")
    print("      3. Vá em 'Configurações e Perfil'")
    print("      4. Marque 'Receber notificações push do navegador'")
    print("      5. Clique em 'Clique aqui para ativar notificações push'")
    print("      6. Permita as notificações quando o navegador pedir")
    print("      7. Execute este script novamente")
    exit(1)

print(f"   ✅ Encontrados {usuarios_com_subscription.count()} usuário(s) com notificações ativadas:")

# Mostrar usuários
for pref in usuarios_com_subscription:
    try:
        subscription = json.loads(pref.push_subscription)
        endpoint = subscription.get('endpoint', 'N/A')
        print(f"      - {pref.usuario.username} ({pref.usuario.email or 'sem email'})")
        print(f"        Endpoint: {endpoint[:60]}...")
    except:
        print(f"      - {pref.usuario.username} (subscription inválida)")

# 4. Perguntar qual usuário testar
print("\n4️⃣ Escolha o usuário para testar:")
print("   (Digite o número ou Enter para testar o primeiro)")

usuarios_lista = list(usuarios_com_subscription)
for idx, pref in enumerate(usuarios_lista, 1):
    print(f"   {idx}. {pref.usuario.username}")

try:
    escolha = input("\n   Escolha: ").strip()
    if escolha == "":
        escolha = "1"
    idx_escolhido = int(escolha) - 1
    if idx_escolhido < 0 or idx_escolhido >= len(usuarios_lista):
        print("   ⚠️  Escolha inválida, usando o primeiro usuário")
        idx_escolhido = 0
except:
    print("   ⚠️  Escolha inválida, usando o primeiro usuário")
    idx_escolhido = 0

pref_selecionada = usuarios_lista[idx_escolhido]
usuario_selecionado = pref_selecionada.usuario

print(f"\n   ✅ Testando com usuário: {usuario_selecionado.username}")

# 5. Enviar notificação de teste
print("\n5️⃣ Enviando notificação de teste...")
print("   ⏳ Aguarde...")

try:
    mensagem = "Esta é uma notificação de teste do TLOGpainel! ✅"
    titulo = "🧪 Teste de Notificações Push"
    url = "/"
    tag = "teste-localhost"
    
    sucesso = enviar_push_notification(
        usuario_selecionado,
        mensagem,
        titulo,
        url=url,
        tag=tag
    )
    
    if sucesso:
        print("   ✅ Notificação ENVIADA com sucesso!")
        print("\n   📱 O QUE ESPERAR:")
        print("      - A notificação deve aparecer no seu computador")
        print("      - Funciona mesmo se o navegador estiver minimizado")
        print("      - Funciona mesmo se o site estiver fechado")
        print("\n   ⚠️  IMPORTANTE:")
        print("      - Se não aparecer, verifique:")
        print("        1. O navegador está aberto? (não precisa estar na página)")
        print("        2. As notificações estão permitidas no Windows?")
        print("        3. O Service Worker está registrado? (verifique no console F12)")
        print("        4. Você está usando localhost ou 127.0.0.1?")
        print("\n   💡 DICA: Abra o Console do navegador (F12) para ver logs detalhados")
    else:
        print("   ❌ Falha ao enviar notificação")
        print("   💡 Verifique:")
        print("      - Se as notificações estão ativadas nas configurações")
        print("      - Se o navegador permitiu as notificações")
        print("      - Se está usando localhost ou 127.0.0.1 (não funciona em IP da rede)")
        
except Exception as e:
    print(f"   ❌ ERRO ao enviar notificação: {e}")
    import traceback
    traceback.print_exc()
    print("\n   💡 POSSÍVEIS SOLUÇÕES:")
    print("      - Verifique se as chaves VAPID estão corretas no .env")
    print("      - Reinicie o servidor Django")
    print("      - Reative as notificações nas configurações do sistema")

print("\n" + "=" * 70)
print("✅ Teste concluído!")
print("=" * 70)

