# 📦 Arquivos que DEVEM ser Commitados

## ✅ ARQUIVOS QUE VÃO PARA O GITHUB

Estes arquivos **DEVEM** ser commitados:

1. ✅ `requirements.txt` - Adicionado mysqlclient
2. ✅ `painel/settings.py` - Configurado para MySQL
3. ✅ `.gitignore` - Atualizado com padrões de backup
4. ✅ `migrar_sqlite_para_mysql.py` - **Script de migração (DEVE ir!)**
5. ✅ `GUIA_MIGRACAO_MYSQL.md` - Documentação
6. ✅ `PASSO_A_PASSO_MIGRACAO.md` - Guia resumido
7. ✅ `PASSO_A_PASSO_COMPLETO.md` - Guia completo
8. ✅ `PROCESSO_COMPLETO_MIGRACAO.md` - Processo completo

## ❌ ARQUIVOS QUE NÃO DEVEM ser Commitados

Estes arquivos **NÃO** devem ser commitados (já estão no .gitignore):

- ❌ `.env` - Contém senhas e credenciais
- ❌ `db.sqlite3` - Banco de dados local
- ❌ `db.sqlite3.backup_*` - Backups
- ❌ `backup_dados_*.json` - Backups em JSON
- ❌ `venv/` - Ambiente virtual
- ❌ `__pycache__/` - Arquivos Python compilados

---

## 🎯 Comando Completo para Commit

```bash
# Verificar o que será commitado
git status

# Adicionar TODOS os arquivos necessários
git add requirements.txt
git add painel/settings.py
git add .gitignore
git add migrar_sqlite_para_mysql.py  # ⚠️ ESTE ARQUIVO DEVE IR!
git add *.md

# Verificar novamente
git status

# Fazer commit
git commit -m "Migração para MySQL: adicionar suporte e script de migração"

# Enviar para GitHub
git push origin main
```

---

## ✅ Verificação Final

Antes de fazer `git push`, verifique com `git status` que:

- ✅ `migrar_sqlite_para_mysql.py` aparece na lista
- ❌ `.env` NÃO aparece na lista
- ❌ `db.sqlite3` NÃO aparece na lista

---

**O arquivo `migrar_sqlite_para_mysql.py` É ESSENCIAL e DEVE ser commitado!** 🚀

