import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "painel.settings")
django.setup()

from rondonopolis.models import ControleAtualizacao

print("--- Ultimas Atualizacoes ---")
for c in ControleAtualizacao.objects.all().order_by('-ultima_atualizacao')[:10]:
    print(f"Tela: '{c.tela}' | Ultima: {c.ultima_atualizacao}")

print("\n--- Verificando 'liberacao-documentos' (kebab) ---")
kebab = ControleAtualizacao.objects.filter(tela='liberacao-documentos').first()
print(f"Kebab ('liberacao-documentos'): {kebab}")

print("\n--- Verificando 'liberacao_documentos' (snake) ---")
snake = ControleAtualizacao.objects.filter(tela='liberacao_documentos').first()
print(f"Snake ('liberacao_documentos'): {snake}")
