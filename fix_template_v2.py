import re

# Ler o arquivo
filepath = r'templates\processos_dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Antes das substituições:")
print(f"Ocorrências de 'periodo_selecionado==\"': {content.count('periodo_selecionado==\"')}")
print(f"Ocorrências de 'tipo_filtro==\"': {content.count('tipo_filtro==\"')}")

# Substituir TODAS as ocorrências de == sem espaços por == com espaços
# Usando uma regex mais específica para pegar variável==
content = re.sub(r'(\w+)==(")', r'\1 == \2', content)

print("\nDepois das substituições:")
print(f"Ocorrências de 'periodo_selecionado == \"': {content.count('periodo_selecionado == \"')}")
print(f"Ocorrências de 'tipo_filtro == \"': {content.count('tipo_filtro == \"')}")

# Salvar o arquivo
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Arquivo corrigido com sucesso!")

# Verificar algumas linhas específicas
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"\nLinha 51: {lines[50].strip()}")
    print(f"Linha 85: {lines[84].strip()}")
    print(f"Linha 99: {lines[98].strip()}")
