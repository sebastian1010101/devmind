# BE01-01 — Instalação do Node.js no Windows

## Opção 1 — Instalador oficial (mais simples)

1. Acesse <https://nodejs.org>
2. Baixe a versão **LTS** (Long Term Support — estável, recomendada)
3. Execute o `.msi` — aceite os defaults (marque "Add to PATH")
4. Reinicie o terminal/VS Code

```powershell
node --version
npm --version
```

## Opção 2 — nvm-windows (recomendado para devs)

O **nvm** gerencia múltiplas versões do Node na mesma máquina:

```powershell
# Instale pelo GitHub: nvm-windows (releases .exe)
nvm install lts       # instala a LTS mais recente
nvm use 20.11.0       # ativa uma versão específica
nvm list              # versões instaladas
```

Útil quando projetos diferentes exigem versões diferentes de Node.

## Opção 3 — WSL2 (mais próximo de produção)

Servidores Linux são o padrão em produção. Com o **WSL2** você roda um Ubuntu dentro do Windows:

```powershell
wsl --install   # PowerShell como admin, depois reinicie
```

Dentro do Ubuntu, siga a instalação para Linux (BE01-02). O VS Code conecta no WSL com a extensão **WSL**.

## O que vem junto

| Ferramenta | O que é |
| --- | --- |
| `node` | o runtime — executa arquivos `.js`/`.ts` compilados |
| `npm` | gerenciador de pacotes — instala dependências |
| `npx` | executa pacotes sem instalar globalmente |

## Problemas comuns

| Erro | Correção |
| --- | --- |
| `'node' não é reconhecido` | PATH não atualizado — feche e reabra o terminal |
| Permissão negada no npm | Não use `sudo`/admin; reinstale via nvm |
| Versão antiga | `nvm install lts && nvm use lts` |

## Resumo

- LTS do site oficial resolve 90% dos casos
- nvm-windows para múltiplas versões; WSL2 para ambiente idêntico à produção
- `node -v` e `npm -v` confirmam a instalação
