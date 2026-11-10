# BE01-03 — Instalação do Node.js no macOS

## Opção 1 — Homebrew (recomendada)

```bash
# Instala o Homebrew (se ainda não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instala o Node LTS
brew install node@20

# Adiciona ao PATH (Apple Silicon)
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Opção 2 — nvm (múltiplas versões)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.zshrc

nvm install --lts
nvm use --lts
```

## Opção 3 — Instalador oficial

Baixe o `.pkg` em <https://nodejs.org> — instala `node` e `npm` em `/usr/local/bin`.

## Apple Silicon vs Intel

| Chip | Homebrew em | Prefixo |
| --- | --- | --- |
| M1/M2/M3/M4 | `/opt/homebrew` | `node@20/bin` lá dentro |
| Intel | `/usr/local` | `/usr/local/bin` |

O Node roda nativo em ARM — sem necessidade de Rosetta.

## Verificando

```bash
node --version
npm --version
which node
```

## Problemas comuns

| Erro | Correção |
| --- | --- |
| `command not found: node` | Recarregue `~/.zshrc` ou ajuste o PATH do brew |
| `EACCES` no npm global | Use nvm ou mude o prefixo do npm — nunca `sudo npm` |
| Xcode tools pedindo | `xcode-select --install` |

## Resumo

- Homebrew ou nvm — ambos corretos; nvm para trocar de versão
- Nunca use `sudo` com npm
- `node -v` confirma a instalação
