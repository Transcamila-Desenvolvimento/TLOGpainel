# 🔄 Processo Completo de Migração - Resumo Executivo

## ✅ O QUE FOI ALTERADO NO CÓDIGO

Estes arquivos foram modificados e **PRECISAM** ser commitados:

1. ✅ `requirements.txt` - Adicionado mysqlclient
2. ✅ `painel/settings.py` - Configurado para MySQL
3. ✅ `.gitignore` - Adicionados padrões de backup
4. ✅ `migrar_sqlite_para_mysql.py` - Script de migração (NOVO)
5. ✅ `GUIA_MIGRACAO_MYSQL.md` - Documentação (NOVO)
6. ✅ `PASSO_A_PASSO_MIGRACAO.md` - Guia resumido (NOVO)

## ❌ O QUE NÃO DEVE SER COMMITADO

- ❌ `.env` - Contém senhas e credenciais (já está no .gitignore)
- ❌ `db.sqlite3` - Banco de dados local (já está no .gitignore)
- ❌ Backups (`db.sqlite3.backup_*`, `backup_dados_*.json`)

---

## 📤 PASSO 1: COMMITAR E ENVIAR PARA GITHUB

### No seu computador local:

```bash
# 1. Verificar o que será commitado
git status

# 2. Adicionar os arquivos modificados
git add requirements.txt
git add painel/settings.py
git add .gitignore
git add migrar_sqlite_para_mysql.py
git add GUIA_MIGRACAO_MYSQL.md
git add PASSO_A_PASSO_MIGRACAO.md

# 3. Fazer commit
git commit -m "Migração para MySQL: adicionar suporte e script de migração"

# 4. Enviar para GitHub
git push origin main
# (ou git push origin master, dependendo da sua branch)
```

**⚠️ IMPORTANTE**: Verifique que o `.env` NÃO está na lista do `git status`!

---

## 🖥️ PASSO 2: NO PYTHONANYWHERE

### 2.1. Atualizar código do GitHub

No **Bash Console** do PythonAnywhere:

```bash
cd ~/TLOGpainel-main
git pull
```

Isso vai baixar todas as alterações que você fez commit.

---

### 2.2. Criar Banco MySQL (se ainda não criou)

1. Dashboard → **Databases**
2. **Create a new database**
3. Anote: nome, usuário, senha, host

---

### 2.3. Fazer Backup (CRÍTICO!)

```bash
cd ~/TLOGpainel-main
cp db.sqlite3 db.sqlite3.backup
python3.10 manage.py dumpdata > backup_dados.json
```

**Baixe esses arquivos para seu PC!**

---

### 2.4. Instalar mysqlclient

```bash
pip3.10 install --user mysqlclient==2.2.4
```

---

### 2.5. Configurar .env no servidor

```bash
nano .env
```

Cole (substitua pelos valores reais):

```env
USE_MYSQL=True
DB_NAME=seu_banco_mysql
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

Salve: `Ctrl+X`, `Y`, `Enter`

---

### 2.6. Criar estrutura no MySQL

```bash
python3.10 manage.py migrate
```

---

### 2.7. Migrar dados

```bash
python3.10 migrar_sqlite_para_mysql.py
```

Aguarde até ver "MIGRAÇÃO CONCLUÍDA!"

---

### 2.8. Recarregar aplicação

1. Dashboard → **Web**
2. Clique em **Reload**

---

### 2.9. Testar

- Acesse seu site
- Faça login
- Verifique se os dados aparecem

---

## 📋 RESUMO ULTRA-RÁPIDO

### No seu PC:
```bash
git add requirements.txt painel/settings.py .gitignore migrar_sqlite_para_mysql.py *.md
git commit -m "Migração para MySQL"
git push
```

### No PythonAnywhere:
```bash
# 1. Atualizar código
git pull

# 2. Backup
cp db.sqlite3 db.sqlite3.backup

# 3. Instalar driver
pip3.10 install --user mysqlclient==2.2.4

# 4. Configurar .env (editar manualmente)
nano .env

# 5. Criar estrutura
python3.10 manage.py migrate

# 6. Migrar dados
python3.10 migrar_sqlite_para_mysql.py

# 7. Recarregar no Dashboard → Web → Reload
```

---

## ⚠️ ATENÇÃO

1. **NUNCA** commite o arquivo `.env` (contém senhas!)
2. **SEMPRE** faça backup antes de migrar
3. O site continuará funcionando com SQLite até você configurar o `.env` no servidor
4. Após configurar o `.env` e migrar, o site usará MySQL

---

## ✅ CHECKLIST FINAL

- [ ] Commit feito no GitHub
- [ ] Código atualizado no PythonAnywhere (`git pull`)
- [ ] Banco MySQL criado
- [ ] Backup feito
- [ ] mysqlclient instalado
- [ ] `.env` configurado no servidor
- [ ] `migrate` executado
- [ ] Script de migração executado
- [ ] Aplicação recarregada
- [ ] Site testado

**Pronto! 🚀**

