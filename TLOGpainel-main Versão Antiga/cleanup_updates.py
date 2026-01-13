import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "painel.settings")
django.setup()

from rondonopolis.models import ControleAtualizacao

# Delete old snake_case key
count, _ = ControleAtualizacao.objects.filter(tela='liberacao_documentos').delete()
print(f"Deleted {count} legacy 'liberacao_documentos' entries.")

# Verify kebab case
kebab = ControleAtualizacao.objects.filter(tela='liberacao-documentos').first()
if kebab:
    print(f"Active key 'liberacao-documentos' found (updated: {kebab.ultima_atualizacao})")
else:
    print("Warning: Active key 'liberacao-documentos' not found yet (will be created on next update)")
