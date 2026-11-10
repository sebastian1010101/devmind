# BE01-02 — Instalação do Node.js no Linux

## Opção 1 — nvm (recomendada)

```bash
# Instala o nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Recarrega o shell
source ~/.bashrc   # ou ~/.zshrc

# Instala e usa a LTS
nvm install --lts
nvm use --lts

node --version
```

O nvm coloca o Node no seu usuário — **sem `sudo`** — e permite trocar de versão por projeto.

## Opção 2 — Repositório da distro (simples, mas desatualizado)

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install nodejs npm

# Fedora
sudo dnf install nodejs
```

O problema: a distro empacota versões antigas. Prefira NodeSource ou nvm.

## Opção 3 — NodeSource (versão atual sem nvm)

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

## Evitando sudo no npm global

Se `npm install -g` pedir permissão, aponte o prefixo para o seu usuário:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

Com nvm isso não é necessário — tudo já fica em `~/.nvm`.

## Verificando

```bash
node --version   # v20.x.x
npm --version    # 10.x.x
which node       # caminho do executável
```

## Resumo

- nvm é o padrão para desenvolvimento — sem sudo, múltiplas versões
- Repositório da distro é fácil mas desatualizado
- Nunca instale pacotes npm globais com `sudo`
