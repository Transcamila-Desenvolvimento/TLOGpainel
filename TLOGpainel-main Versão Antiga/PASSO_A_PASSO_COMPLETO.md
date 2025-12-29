# 🚀 Passo a Passo Completo - Migração SQLite → MySQL

## 📍 PARTE 1: NO SEU COMPUTADOR

### 1. Verificar o que será commitado
```bash
git status
```
**Certifique-se que `.env` NÃO aparece na lista!**

### 2. Adicionar arquivos ao Git
```bash
git add requirements.txt
git add painel/settings.py
git add .gitignore
git add migrar_sqlite_para_mysql.py  # ⚠️ IMPORTANTE: Este arquivo DEVE ser commitado!
git add *.md
```

**⚠️ ATENÇÃO**: O arquivo `migrar_sqlite_para_mysql.py` **DEVE** ser commitado e enviado para o GitHub, pois será usado no servidor!

### 3. Fazer commit
```bash
git commit -m "Migração para MySQL"
```

### 4. Enviar para GitHub
```bash
git push origin main
```
(ou `git push origin master` se sua branch for master)

---

## 📍 PARTE 2: NO PYTHONANYWHERE

### 5. Abrir Bash Console
No Dashboard do PythonAnywhere, clique em **Bash**

### 6. Navegar para o projeto
```bash
cd ~/TLOGpainel-main
```

### 7. Atualizar código do GitHub
```bash
git pull
```

### 8. Criar Banco MySQL
1. No Dashboard, vá em **Databases**
2. Clique em **Create a new database**
3. Escolha um nome (ex: `tlogpainel_db`)
4. **ANOTE**: nome do banco, usuário, senha
5. O host será: `seu_usuario.mysql.pythonanywhere-services.com`

### 9. Fazer Backup (IMPORTANTE!)
```bash
cp db.sqlite3 db.sqlite3.backup
python3.10 manage.py dumpdata > backup_dados.json
```

### 10. Instalar mysqlclient
```bash
pip3.10 install --user mysqlclient==2.2.4
```

### 11. Criar arquivo .env
```bash
nano .env
```

Cole este conteúdo (substitua pelos seus valores):
```env
USE_MYSQL=True
DB_NAME=seu_banco_mysql
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

Salvar: `Ctrl+X`, depois `Y`, depois `Enter`

### 12. Criar estrutura no MySQL
```bash
python3.10 manage.py migrate
```

### 13. Migrar dados do SQLite para MySQL
```bash
python3.10 migrar_sqlite_para_mysql.py
```

Aguarde até aparecer: **"MIGRAÇÃO CONCLUÍDA!"**

### 14. Recarregar aplicação
1. No Dashboard, vá em **Web**
2. Clique no botão **Reload**

### 15. Testar
- Acesse seu site
- Faça login
- Verifique se os dados aparecem corretamente
- Teste criar/editar algo

---

## ✅ CHECKLIST RÁPIDO

**No seu PC:**
- [ ] `git status` (verificar que .env não está)
- [ ] `git add requirements.txt painel/settings.py .gitignore migrar_sqlite_para_mysql.py *.md`
- [ ] `git commit -m "Migração para MySQL"`
- [ ] `git push`

**No PythonAnywhere:**
- [ ] `git pull`
- [ ] Criar banco MySQL no Dashboard
- [ ] `cp db.sqlite3 db.sqlite3.backup` (backup)
- [ ] `pip3.10 install --user mysqlclient==2.2.4`
- [ ] Criar `.env` com credenciais MySQL
- [ ] `python3.10 manage.py migrate`
- [ ] `python3.10 migrar_sqlite_para_mysql.py`
- [ ] Recarregar aplicação no Dashboard
- [ ] Testar site

---

## ⚠️ IMPORTANTE

1. **NUNCA** commite o arquivo `.env` (contém senhas!)
2. **SEMPRE** faça backup antes de migrar
3. O site continua funcionando com SQLite até você configurar o `.env`
4. Após configurar o `.env` e migrar, o site usará MySQL automaticamente

---

## 🆘 SE DER ERRO

### Erro: "ModuleNotFoundError: No module named 'MySQLdb'"
```bash
pip3.10 install --user mysqlclient==2.2.4
```

### Erro: "Access denied"
- Verifique usuário/senha no `.env`
- Confirme que o banco foi criado

### Erro: "Unknown database"
- Verifique o nome do banco no `.env`
- Confirme que criou o banco no Dashboard

### Dados não aparecem
- Verifique se o script de migração rodou sem erros
- Confirme que `USE_MYSQL=True` no `.env`

---

**Pronto! Siga os passos na ordem e tudo vai funcionar! 🚀**

