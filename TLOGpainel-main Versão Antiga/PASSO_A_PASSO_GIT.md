# 📤 Passo a Passo: Enviar Atualizações para o Git

## ⚠️ PRIMEIRA VEZ (Se o repositório ainda não foi inicializado)

Se esta é a primeira vez, você precisa inicializar o repositório:

```bash
# 1. Inicializar repositório Git
git init

# 2. Adicionar repositório remoto (substitua pela URL do seu repositório)
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git

# 3. Verificar se foi adicionado
git remote -v
```

**Pule esta seção se o repositório já existe!**

---

## ✅ Checklist Antes de Começar

- [ ] Arquivo `.env` está no `.gitignore` (não será enviado)
- [ ] Verificar se há arquivos sensíveis que não devem ser enviados

---

## 🚀 Passo a Passo Completo

### **PASSO 0: Verificar se é Repositório Git**

```bash
git status
```

Se aparecer erro "not a git repository", execute os comandos da seção "PRIMEIRA VEZ" acima.

### **PASSO 1: Verificar Status**

Verifique quais arquivos foram modificados:

```bash
git status
```

**O que esperar:**
- Arquivos modificados aparecerão em vermelho
- Arquivos não rastreados aparecerão
- Arquivo `.env` NÃO deve aparecer (está no .gitignore)

---

### **PASSO 2: Ver o que Será Enviado**

Ver as mudanças detalhadas (opcional):

```bash
git diff
```

---

### **PASSO 3: Adicionar Arquivos ao Stage**

Adicionar todos os arquivos modificados:

```bash
git add .
```

**OU** adicionar arquivos específicos:

```bash
git add painel/settings.py
git add rondonopolis/utils.py
git add rondonopolis/mensagens.py
git add rondonopolis/views.py
git add static/sw.js
git add requirements.txt
```

---

### **PASSO 4: Verificar o que Foi Adicionado**

Confirmar o que será commitado:

```bash
git status
```

**O que esperar:**
- Arquivos adicionados aparecerão em verde com "Changes to be committed"
- Arquivo `.env` NÃO deve aparecer

---

### **PASSO 5: Fazer Commit**

Fazer commit com uma mensagem descritiva:

```bash
git commit -m "Adicionar notificações push, validação de status cancelado e configurações de email no .env"
```

**OU** uma mensagem mais simples:

```bash
git commit -m "Atualizações: notificações push e melhorias no sistema"
```

---

### **PASSO 6: Verificar Branch Atual**

Verificar em qual branch você está:

```bash
git branch
```

A branch atual aparecerá com um `*` na frente.

---

### **PASSO 7: Enviar para o GitHub**

Enviar as atualizações para o repositório remoto:

```bash
git push origin main
```

**OU** se a branch for diferente (ex: master):

```bash
git push origin master
```

---

### **PASSO 8: Confirmar Envio**

Verificar se foi enviado com sucesso:

```bash
git status
```

**O que esperar:**
- Deve aparecer "Your branch is up to date with 'origin/main'"
- Nenhum arquivo pendente

---

## 🔍 Comandos Rápidos (Resumo)

```bash
# 1. Verificar status
git status

# 2. Adicionar arquivos
git add .

# 3. Fazer commit
git commit -m "Sua mensagem de commit"

# 4. Enviar para GitHub
git push origin main
```

---

## ⚠️ Problemas Comuns

### **Erro: "fatal: not a git repository"**

**Solução:** Você não está na pasta do projeto. Execute:
```bash
cd "caminho/para/seu/projeto"
```

### **Erro: "Please tell me who you are"**

**Solução:** Configure seu usuário Git:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### **Erro: "Permission denied"**

**Solução:** Verifique suas credenciais do GitHub ou configure SSH keys.

### **Erro: "Updates were rejected"**

**Solução:** Alguém enviou mudanças antes. Faça pull primeiro:
```bash
git pull origin main
# Resolva conflitos se houver
git push origin main
```

---

## 📝 Exemplo Completo

```bash
# 1. Navegar para a pasta do projeto
cd "c:\Users\adm10\Desktop\TLOGpainel-main - Copia Segurança - Copia"

# 2. Verificar status
git status

# 3. Adicionar todos os arquivos
git add .

# 4. Fazer commit
git commit -m "Implementar notificações push, validação de status cancelado e melhorias de segurança"

# 5. Enviar para GitHub
git push origin main
```

---

## ✅ Checklist Final

- [ ] `git status` mostra os arquivos corretos
- [ ] `.env` NÃO está na lista de arquivos a serem enviados
- [ ] Commit foi feito com sucesso
- [ ] Push foi enviado para o GitHub
- [ ] Código atualizado no repositório remoto

---

**Pronto! 🎉**

