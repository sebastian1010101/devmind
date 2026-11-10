# FE02-01 — Instalando o Git

## Instalação por Sistema Operacional

---

## 1. Linux (Ubuntu / Debian e derivados)

Abra o terminal e execute os comandos de atualização de pacotes:

```bash
sudo apt update
sudo apt install git -y
```

Verifique a instalação:

```bash
git --version
```

---

## 2. Windows

1. Baixe o instalador oficial em [git-scm.com](https://git-scm.com/download/win).
2. Durante a instalação do instalador, mantenha as opções recomendadas:
   - Certifique-se de marcar o **Git Bash** (emulador de terminal Unix para Windows).
   - Escolha o VS Code como editor padrão do Git.
   - Defina o nome da branch padrão como `main`.

---

## 3. macOS

Caso utilize o gerenciador de pacotes Homebrew:

```bash
brew install git
```

Ou execute qualquer comando Git no Terminal; caso ainda não esteja instalado, o sistema abrirá o instalador das ferramentas de desenvolvedor da Apple (*Command Line Developer Tools*).

---

## Configuração Inicial Obrigatória (First-Time Setup)

Após instalar o Git pela primeira vez, é obrigatório registrar sua identidade global. Todas as alterações e commits futuros carregarão esse nome e e-mail:

```bash
# 1. Definir seu nome completo público
git config --global user.name "Seu Nome Completo"

# 2. Definir o mesmo e-mail cadastrado na sua conta do GitHub
git config --global user.email "seuemail@exemplo.com"

# 3. Definir 'main' como nome padrão para branches iniciais
git config --global init.defaultBranch main
```

Para verificar se as configurações foram salvas corretamente:

```bash
git config --list
```
