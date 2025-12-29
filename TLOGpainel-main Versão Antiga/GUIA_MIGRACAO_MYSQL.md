# Guia de Migração: SQLite para MySQL

Este guia explica como migrar seu projeto Django de SQLite para MySQL no PythonAnywhere.

## Por que MySQL é melhor?

- ✅ **Melhor performance** com múltiplos usuários simultâneos
- ✅ **Transações mais robustas** e controle de concorrência
- ✅ **Melhor escalabilidade** para crescimento futuro
- ✅ **Backups mais eficientes** e restauração mais rápida
- ✅ **Padrão da indústria** para aplicações em produção

---

## Passo 1: Configurar MySQL no PythonAnywhere

### 1.1. Criar o banco de dados MySQL

1. Acesse o **Dashboard** do PythonAnywhere
2. Vá em **Databases**
3. Clique em **Create a new database**
4. Escolha um nome para o banco (ex: `tlogpainel_db`)
5. Anote o nome do banco, usuário e senha gerados

**IMPORTANTE**: O PythonAnywhere cria automaticamente um usuário com o mesmo nome do banco.

### 1.2. Obter informações de conexão

No PythonAnywhere, você terá:
- **Host**: `seu_usuario.mysql.pythonanywhere-services.com`
- **Usuário**: (geralmente o mesmo nome do banco)
- **Senha**: (a senha que você definiu)
- **Nome do banco**: (o nome que você escolheu)
- **Porta**: `3306` (padrão)

---

## Passo 2: Atualizar o Projeto Localmente

### 2.1. Atualizar requirements.txt

O arquivo já foi atualizado com `mysqlclient==2.2.4`. Se estiver fazendo localmente:

```bash
pip install mysqlclient==2.2.4
```

**Nota para Windows**: Se tiver problemas instalando `mysqlclient`, use `pip install mysqlclient-binary` ou instale o MySQL Connector/C primeiro.

### 2.2. Configurar variáveis de ambiente

Crie ou atualize o arquivo `.env` na raiz do projeto:

```env
# Banco de dados
USE_MYSQL=True

# Configurações MySQL (PythonAnywhere)
DB_NAME=seu_banco_mysql
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

**⚠️ IMPORTANTE**: 
- NUNCA commite o arquivo `.env` no Git (deve estar no `.gitignore`)
- Use variáveis de ambiente diferentes para desenvolvimento e produção

### 2.3. Testar conexão localmente (opcional)

Para testar a conexão antes de fazer o deploy:

1. Configure o `.env` com as credenciais do PythonAnywhere
2. Execute: `python manage.py migrate`
3. Se funcionar, a conexão está OK!

---

## Passo 3: Fazer Backup dos Dados Atuais

**⚠️ CRÍTICO: Faça backup ANTES de qualquer alteração!**

### 3.1. No PythonAnywhere (via Bash Console)

```bash
# Navegar até o diretório do projeto
cd ~/TLOGpainel-main

# Fazer backup do SQLite
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)

# Exportar dados como JSON (backup adicional)
python manage.py dumpdata > backup_dados_$(date +%Y%m%d_%H%M%S).json
```

### 3.2. Baixar o backup

Baixe o arquivo `db.sqlite3.backup_*` e o `backup_dados_*.json` para seu computador local.

---

## Passo 4: Deploy no PythonAnywhere

### 4.1. Atualizar arquivos no servidor

1. Faça commit das alterações:
   ```bash
   git add requirements.txt painel/settings.py migrar_sqlite_para_mysql.py
   git commit -m "Migração para MySQL"
   git push
   ```

2. No PythonAnywhere, atualize o código:
   ```bash
   cd ~/TLOGpainel-main
   git pull
   ```

### 4.2. Instalar mysqlclient

No **Bash Console** do PythonAnywhere:

```bash
cd ~/TLOGpainel-main
pip3.10 install --user mysqlclient==2.2.4
```

**Nota**: Use `pip3.10` (ou a versão do Python que você está usando).

### 4.3. Configurar variáveis de ambiente

No PythonAnywhere, você pode configurar variáveis de ambiente de duas formas:

**Opção A: Arquivo .env** (recomendado)
```bash
cd ~/TLOGpainel-main
nano .env
```

Adicione:
```env
USE_MYSQL=True
DB_NAME=seu_banco_mysql
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=seu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

**Opção B: No arquivo WSGI** (alternativa)

Edite o arquivo WSGI e adicione antes de `application = get_wsgi_application()`:

```python
import os
os.environ['USE_MYSQL'] = 'True'
os.environ['DB_NAME'] = 'seu_banco_mysql'
os.environ['DB_USER'] = 'seu_usuario_mysql'
os.environ['DB_PASSWORD'] = 'sua_senha_mysql'
os.environ['DB_HOST'] = 'seu_usuario.mysql.pythonanywhere-services.com'
os.environ['DB_PORT'] = '3306'
```

---

## Passo 5: Migrar os Dados

### 5.1. Criar estrutura no MySQL

No **Bash Console** do PythonAnywhere:

```bash
cd ~/TLOGpainel-main
python3.10 manage.py migrate
```

Isso criará todas as tabelas no MySQL (ainda vazias).

### 5.2. Executar script de migração

```bash
python3.10 migrar_sqlite_para_mysql.py
```

O script irá:
1. Conectar ao SQLite
2. Conectar ao MySQL
3. Criar a estrutura (se necessário)
4. Migrar todos os dados
5. Mostrar progresso e estatísticas

### 5.3. Verificar migração

```bash
# Verificar quantos registros foram migrados
python3.10 manage.py shell
```

No shell do Django:
```python
from django.contrib.auth.models import User
from core.models import Lancamento  # ajuste conforme seus modelos

print(f"Usuários: {User.objects.count()}")
print(f"Lançamentos: {Lancamento.objects.count()}")
# Verifique outras tabelas importantes
```

---

## Passo 6: Testar a Aplicação

### 6.1. Recarregar a aplicação

No **Dashboard** do PythonAnywhere:
1. Vá em **Web**
2. Clique em **Reload** para reiniciar a aplicação

### 6.2. Testar funcionalidades

- Faça login
- Verifique se os dados aparecem corretamente
- Teste operações de criação/edição
- Verifique se não há erros no console

---

## Passo 7: Limpeza (Opcional)

Após confirmar que tudo está funcionando:

### 7.1. Manter backup do SQLite

**NÃO DELETE** o `db.sqlite3` imediatamente. Mantenha por alguns dias como backup.

### 7.2. Atualizar .gitignore

Certifique-se de que `.env` está no `.gitignore`:

```
.env
*.db
*.sqlite3
db.sqlite3.backup_*
backup_dados_*.json
```

---

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'MySQLdb'"

**Solução**: Instale o mysqlclient:
```bash
pip3.10 install --user mysqlclient==2.2.4
```

### Erro: "Access denied for user"

**Solução**: Verifique:
- Nome de usuário e senha no `.env`
- Se o usuário tem permissões no banco
- Se o host está correto

### Erro: "Unknown database"

**Solução**: 
- Verifique se o banco foi criado no PythonAnywhere
- Confirme o nome do banco no `.env`

### Erro: "Table doesn't exist"

**Solução**: Execute as migrations:
```bash
python3.10 manage.py migrate
```

### Dados não aparecem após migração

**Solução**:
1. Verifique se o script de migração rodou sem erros
2. Confirme que está usando o banco MySQL (não SQLite)
3. Verifique os logs do script de migração

---

## Checklist Final

- [ ] MySQL criado no PythonAnywhere
- [ ] Variáveis de ambiente configuradas
- [ ] mysqlclient instalado
- [ ] Backup do SQLite feito
- [ ] Estrutura criada no MySQL (`migrate`)
- [ ] Dados migrados (script executado)
- [ ] Aplicação testada e funcionando
- [ ] Backup mantido por segurança

---

## Suporte

Se encontrar problemas:
1. Verifique os logs do PythonAnywhere
2. Confirme todas as credenciais
3. Teste a conexão MySQL separadamente
4. Mantenha os backups até confirmar que tudo está OK

**Boa sorte com a migração! 🚀**

