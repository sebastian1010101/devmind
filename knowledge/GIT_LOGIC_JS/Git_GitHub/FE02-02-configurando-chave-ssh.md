# FE02-02 — Configurando Chave SSH

## Por que Usar Chaves SSH com o GitHub?

O GitHub não permite mais autenticação de push no terminal utilizando a senha comum da sua conta por razões de segurança. As duas formas modernas aceitas são **Tokens de Acesso Pessoal (PAT)** ou **Chaves SSH**.

O protocolo **SSH (Secure Shell)** é o método mais prático e seguro: após configurado uma única vez na sua máquina, você realiza comandos `git push` e `git clone` instantaneamente sem precisar digitar senhas ou tokens a cada envio.

---

## Passo a Passo para Gerar e Configurar Chave SSH

### 1. Gerar um Novo Par de Chaves SSH

Abra o terminal e execute o comando abaixo (substituindo pelo seu e-mail cadastrado no GitHub):

```bash
ssh-keygen -t ed25519 -C "seuemail@exemplo.com"
```

*Nota: o algoritmo `ed25519` é o padrão criptográfico moderno mais seguro e eficiente.*

- Pressione `Enter` para salvar no caminho padrão sugerido (`~/.ssh/id_ed25519`).
- (Opcional) Digite uma senha (*passphrase*) de proteção para a chave ou pressione `Enter` duas vezes para deixar sem senha.

### 2. Iniciar o Agente SSH e Adicionar a Chave

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 3. Copiar a Chave Pública Gerada

O par de chaves consiste em uma chave privada (`id_ed25519`, que **nunca** deve ser compartilhada com ninguém) e uma chave pública (`id_ed25519.pub`), que é a que enviamos para o GitHub.

Exiba o conteúdo da chave pública no terminal e copie o texto completo:

```bash
cat ~/.ssh/id_ed25519.pub
```

*(O texto começa com `ssh-ed25519` e termina com o seu e-mail).*

### 4. Adicionar a Chave na sua Conta do GitHub

1. Acesse o [GitHub](https://github.com) e faça login.
2. Clique na sua foto de perfil no canto superior direito &rarr; **Settings (Configurações)**.
3. No menu lateral esquerdo, clique em **SSH and GPG keys**.
4. Clique no botão verde **New SSH key**.
5. No campo **Title**, dê um nome para identificar seu computador (ex: `Notebook Pessoal Linux`).
6. No campo **Key**, cole todo o conteúdo copiado da chave pública.
7. Clique em **Add SSH key**.

### 5. Testar a Conexão

Execute no terminal:

```bash
ssh -T git@github.com
```

Ao receber a mensagem:
> `Hi username! You've successfully authenticated, but GitHub does not provide shell access.`

Sua chave SSH está perfeitamente configurada e pronta para uso.
