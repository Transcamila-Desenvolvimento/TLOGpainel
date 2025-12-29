# 🚀 Guia Completo: Deploy para Produção

Este guia mostra passo a passo como preparar e enviar o projeto para o GitHub e colocá-lo em produção.

---

## 📋 CHECKLIST ANTES DE ENVIAR PARA O GITHUB

### ⚠️ **VERIFICAR ARQUIVOS SENSÍVEIS**

Certifique-se de que o arquivo `.gitignore` está configurado corretamente e que os seguintes arquivos **NÃO** sejam enviados:

- ✅ `.env` (contém chaves secretas)
- ✅ `db.sqlite3` (banco de dados local)
- ✅ `venv/` (ambiente virtual)
- ✅ `__pycache__/` (arquivos Python compilados)
- ✅ `*.pyc` (arquivos compilados)
- ✅ `*.log` (logs)
- ✅ `staticfiles/` (arquivos estáticos coletados)

### 🔐 **VERIFICAR SECRETS NO CÓDIGO**

**IMPORTANTE:** Verifique se não há senhas ou chaves secretas hardcoded no código. Se encontrar, mova para o arquivo `.env`.

---

## 📝 PASSO A PASSO: PREPARAR PARA PRODUÇÃO

### **1. Verificar e Configurar .gitignore**

Certifique-se de que o `.gitignore` contém:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
staticfiles/
media/

# Ambiente
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### **2. Preparar Settings para Produção**

No arquivo `painel/settings.py`, você precisa fazer algumas alterações para produção:

**⚠️ ATENÇÃO:** Crie uma cópia de segurança antes de modificar!

```python
# No início do arquivo, após importar os
import os
from dotenv import load_dotenv

load_dotenv()

# Mudar SECRET_KEY para usar variável de ambiente
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-h*qsm%4q^azw!s(0i3^$qaklp42pwtwnivb10m8i8h-_rbsy!n')

# Mudar DEBUG para usar variável de ambiente (False em produção)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Configurar ALLOWED_HOSTS para produção
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'portorestrito.pythonanywhere.com,127.0.0.1,localhost').split(',')

# Adicionar HTTPS no CSRF_TRUSTED_ORIGINS para produção
CSRF_TRUSTED_ORIGINS = [
    'https://portorestrito.pythonanywhere.com',  # HTTPS para produção
    'http://127.0.0.1:8000',  # Para desenvolvimento local
    'http://localhost:8000',
]
```

**OU** crie um arquivo `settings_production.py` separado (recomendado para maior segurança).

### **3. Criar Arquivo .env.example**

Crie um arquivo `.env.example` com as variáveis necessárias (sem valores secretos):

```env
# Django
SECRET_KEY=sua_secret_key_aqui
DEBUG=False
ALLOWED_HOSTS=portorestrito.pythonanywhere.com,seusite.com

# Email (OBRIGATÓRIO: configurar EMAIL_HOST_PASSWORD no servidor)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=digitalmidia@transcamila.com.br
EMAIL_HOST_PASSWORD=sua_senha_de_app_gmail_aqui
DEFAULT_FROM_EMAIL=digitalmidia@transcamila.com.br

# WhatsApp API (opcional)
WHATSAPP_API_URL=
WHATSAPP_API_KEY=
WHATSAPP_API_INSTANCE=default

# Web Push Notifications (VAPID Keys)
VAPID_PUBLIC_KEY=sua_chave_publica_vapid
VAPID_PRIVATE_KEY=sua_chave_privada_vapid
```

Este arquivo pode ser enviado para o GitHub (é apenas um exemplo).

### **4. Verificar Dependências**

Certifique-se de que o `requirements.txt` está atualizado:

```bash
pip freeze > requirements.txt
```

---

## 📤 ENVIAR PARA O GITHUB

### **1. Verificar Status do Git**

```bash
git status
```

Verifique quais arquivos serão adicionados. Certifique-se de que arquivos sensíveis não estão na lista.

### **2. Adicionar Arquivos**

```bash
# Adicionar todos os arquivos (respeitando .gitignore)
git add .

# OU adicionar arquivos específicos
git add *.py
git add templates/
git add static/
git add requirements.txt
```

### **3. Fazer Commit**

```bash
git commit -m "Preparar para produção: adicionar notificações push e validação de status cancelado"
```

### **4. Enviar para GitHub**

```bash
# Se já tiver um repositório remoto configurado
git push origin main

# OU se for a primeira vez
git remote add origin https://github.com/seu-usuario/seu-repositorio.git
git branch -M main
git push -u origin main
```

---

## 🚀 DEPLOY EM PRODUÇÃO

### **Para PythonAnywhere ou Servidor Similar**

#### **1. Conectar ao Servidor**

```bash
ssh usuario@servidor.com
```

#### **2. Clonar Repositório**

```bash
cd /var/www  # ou pasta apropriada
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

#### **3. Criar Ambiente Virtual**

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows
```

#### **4. Instalar Dependências**

```bash
pip install -r requirements.txt
```

#### **5. Criar Arquivo .env**

Crie o arquivo `.env` no servidor com todas as variáveis de ambiente:

```env
SECRET_KEY=sua_secret_key_segura_aqui
DEBUG=False
ALLOWED_HOSTS=portorestrito.pythonanywhere.com
EMAIL_HOST_USER=digitalmidia@transcamila.com.br
EMAIL_HOST_PASSWORD=sua_senha_aqui
VAPID_PUBLIC_KEY=sua_chave_publica
VAPID_PRIVATE_KEY=sua_chave_privada
```

#### **6. Executar Migrations**

```bash
python manage.py migrate
```

#### **7. Coletar Arquivos Estáticos**

```bash
python manage.py collectstatic --noinput
```

#### **8. Criar Superusuário (se necessário)**

```bash
python manage.py createsuperuser
```

#### **9. Configurar Web Server**

**Para PythonAnywhere:**
- Configure o WSGI file apontando para `painel.wsgi.application`
- Configure Static Files mapping: `/static/` → `/home/usuario/projeto/staticfiles/`
- Configure HTTPS (obrigatório para notificações push!)

**Para outros servidores:**
- Configure Nginx/Apache para servir arquivos estáticos
- Configure Gunicorn ou uWSGI para servir a aplicação Django
- Configure HTTPS com certificado SSL

#### **10. Reiniciar Servidor**

No PythonAnywhere, use o botão "Reload" no dashboard.

---

## ✅ CHECKLIST FINAL ANTES DE ENVIAR

- [ ] `.env` está no `.gitignore` e **NÃO** será enviado
- [ ] `db.sqlite3` está no `.gitignore`
- [ ] Não há senhas ou chaves secretas hardcoded no código
- [ ] `requirements.txt` está atualizado
- [ ] `DEBUG=False` em produção (via .env)
- [ ] `SECRET_KEY` está no .env (não hardcoded)
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] `CSRF_TRUSTED_ORIGINS` inclui HTTPS do site de produção
- [ ] `.env.example` criado (opcional, mas recomendado)

---

## 🔒 SEGURANÇA EM PRODUÇÃO

### **Configurações Importantes:**

1. **DEBUG = False** em produção
2. **SECRET_KEY** deve ser único e seguro (não usar a do exemplo!)
3. **HTTPS obrigatório** para notificações push funcionarem
4. **ALLOWED_HOSTS** configurado apenas com domínios permitidos
5. **CSRF_TRUSTED_ORIGINS** com HTTPS configurado

### **Gerar Nova SECRET_KEY:**

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Use essa chave no `.env` de produção.

---

## 📱 NOTIFICAÇÕES PUSH EM PRODUÇÃO

### **Requisitos:**

1. **HTTPS obrigatório** - Notificações push só funcionam em HTTPS
2. **Chaves VAPID configuradas** - No arquivo `.env` do servidor
3. **Service Worker funcionando** - Verifique se `/static/sw.js` está acessível

### **Verificar se Está Funcionando:**

1. Acesse o site em produção via HTTPS
2. Faça login
3. Vá em "Configurações e Perfil"
4. Ative as notificações push
5. Teste enviando uma notificação

---

## 🐛 TROUBLESHOOTING

### **Erro: "DisallowedHost"**

**Solução:** Adicione o domínio em `ALLOWED_HOSTS` no `.env`

### **Notificações Push não funcionam**

**Solução:**
- Verifique se está usando HTTPS (obrigatório!)
- Verifique se as chaves VAPID estão no `.env`
- Verifique se o Service Worker está acessível em `/static/sw.js`

### **Arquivos estáticos não aparecem**

**Solução:**
- Execute `python manage.py collectstatic`
- Verifique se o servidor web está configurado para servir `/static/`

---

## 📞 PRECISA DE AJUDA?

Se tiver problemas:
1. Verifique os logs do servidor
2. Verifique se todas as variáveis de ambiente estão configuradas
3. Verifique se o `.env` existe no servidor
4. Verifique se o banco de dados foi migrado

---

## 🎯 RESUMO RÁPIDO

```bash
# 1. Verificar .gitignore
git status

# 2. Adicionar arquivos
git add .

# 3. Commit
git commit -m "Preparar para produção"

# 4. Push
git push origin main

# No servidor:
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Reiniciar servidor
```

**Pronto! 🎉**

