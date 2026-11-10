# BE01-05 — Instalação e Configuração do Ambiente

## Iniciando um projeto backend

```bash
mkdir minha-api && cd minha-api

npm init -y                      # cria package.json

# TypeScript + tipos do Node (dev dependencies)
npm install --save-dev typescript @types/node

# Gera o tsconfig.json
npx tsc --init
```

## Por que `@types/node`

O Node tem APIs próprias (`fs`, `http`, `process`, `Buffer`) que não existem no JS do browser. O pacote `@types/node` traz as definições de tipo para o TS entendê-las:

```typescript
import fs from "fs";
import process from "process";

fs.readFile("x.txt", "utf8", callback); // autocomplete funciona
process.env.PORT;                        // tipado como string | undefined
```

Regra: pacote `@types/<nome>` = definições de tipo de `<nome>`.

## Estrutura inicial

```text
minha-api/
├── src/
│   └── index.ts          # código fonte TypeScript
├── dist/                 # JS compilado (gerado, não commite)
├── node_modules/
├── package.json
└── tsconfig.json
```

`.gitignore` mínimo:

```text
node_modules/
dist/
.env
```

## Scripts do package.json

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

| Script | Quando |
| --- | --- |
| `dev` | desenvolvimento — recompila e reinicia a cada save |
| `build` | gera o `dist/` pra produção |
| `start` | roda o JS compilado |

## Fluxo completo

```bash
# Desenvolvimento
npm run dev        # ts-node-dev observa src/

# Produção
npm run build      # tsc → dist/
npm start          # node dist/index.js
```

## Dependências: `dependencies` vs `devDependencies`

- `dependencies` — necessárias em produção (`express`, `zod`, `prisma`)
- `devDependencies` — só desenvolvimento (`typescript`, `@types/*`, `ts-node-dev`)

```bash
npm install express            # → dependencies
npm install -D typescript      # → devDependencies
```

## Resumo

- `npm init -y` + `typescript` + `@types/node` + `tsc --init`
- `src/` para TS, `dist/` para JS compilado — dist no `.gitignore`
- Scripts: `dev` (ts-node-dev), `build` (tsc), `start` (node)
- `@types/*` traz tipos de libs JS para o TS
