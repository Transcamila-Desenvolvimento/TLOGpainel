# Passo a Passo Resumido - Migração SQLite → MySQL

## ✅ Pré-requisitos
- Site funcionando no PythonAnywhere
- Acesso ao Dashboard do PythonAnywhere
- Backup do banco atual (importante!)

---

## 📋 Passo 1: Criar Banco MySQL no PythonAnywhere

1. Acesse: **Dashboard** → **Databases**
2. Clique: **Create a new database**
3. Escolha um nome (ex: `tlogpainel_db`)
4. **Anote**: nome do banco, usuário e senha

**Host será**: `seu_usuario.mysql.pythonanywhere-services.com`

---

## 📋 Passo 2: Fazer Backup dos Dados

No **Bash Console** do PythonAnywhere:

```bash
cd ~/TLOGpainel-main
cp db.sqlite3 db.sqlite3.backup
python3.10 manage.py dumpdata > backup_dados.json
```

**Baixe** esses arquivos para seu computador!

---

## 📋 Passo 3: Atualizar Código no Servidor

No **Bash Console**:

```bash
cd ~/TLOGpainel-main
git pull  # ou faça upload dos arquivos atualizados
```

---

## 📋 Passo 4: Instalar mysqlclient

```bash
pip3.10 install --user mysqlclient==2.2.4
```

---

## 📋 Passo 5: Configurar Variáveis de Ambiente

Crie/edite o arquivo `.env`:

```bash
nano .env
```

Cole (substitua pelos seus valores reais):

```env
USE_MYSQL=True
DB_NAME=seu_banco_mysql
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

Salve: `Ctrl+X`, depois `Y`, depois `Enter`

---

## 📋 Passo 6: Criar Estrutura no MySQL

```bash
python3.10 manage.py migrate
```

Isso cria todas as tabelas (ainda vazias).

---

## 📋 Passo 7: Migrar os Dados

```bash
python3.10 migrar_sqlite_para_mysql.py
```

O script vai:
- Ler dados do SQLite
- Copiar para MySQL
- Mostrar progresso

**Aguarde** até ver "MIGRAÇÃO CONCLUÍDA!"

---

## 📋 Passo 8: Recarregar Aplicação

1. Vá em **Dashboard** → **Web**
2. Clique em **Reload**

---

## 📋 Passo 9: Testar

- Acesse seu site
- Faça login
- Verifique se os dados aparecem
- Teste criar/editar algo

---

## ⚠️ Se Der Erro

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

## ✅ Checklist Final

- [ ] Banco MySQL criado
- [ ] Backup feito
- [ ] Código atualizado
- [ ] mysqlclient instalado
- [ ] `.env` configurado
- [ ] `migrate` executado
- [ ] Script de migração executado
- [ ] Aplicação recarregada
- [ ] Site testado e funcionando

---

## 🎯 Resumo Ultra-Rápido

```bash
# 1. Criar banco no Dashboard
# 2. Backup
cp db.sqlite3 db.sqlite3.backup

# 3. Atualizar código
git pull

# 4. Instalar driver
pip3.10 install --user mysqlclient==2.2.4

# 5. Configurar .env (editar manualmente)
nano .env

# 6. Criar estrutura
python3.10 manage.py migrate

# 7. Migrar dados
python3.10 migrar_sqlite_para_mysql.py

# 8. Recarregar no Dashboard → Web → Reload
```

**Pronto! 🚀**

