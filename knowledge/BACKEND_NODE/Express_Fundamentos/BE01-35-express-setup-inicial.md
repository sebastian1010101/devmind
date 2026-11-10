# BE01-35 — Express: Setup Inicial

## Do zero ao servidor

```bash
mkdir minha-api && cd minha-api
npm init -y

# Produção
npm install express

# Dev — TS, tipos e hot reload
npm install -D typescript @types/node @types/express ts-node-dev

npx tsc --init
```

## tsconfig.json mínimo

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

## package.json — scripts

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

## src/index.ts — o mínimo

```typescript
import express from "express";

const app = express();
app.use(express.json()); // sem isso, req.body é undefined

app.get("/", (req, res) => {
  res.json({ mensagem: "API no ar" });
});

app.listen(3000, () => {
  console.log("Servidor rodando em http://localhost:3000");
});
```

```bash
npm run dev
curl http://localhost:3000
# {"mensagem":"API no ar"}
```

## As 3 peças essenciais

```typescript
const app = express();          // 1. a aplicação
app.use(express.json());        // 2. middleware que parseia JSON do body
app.listen(3000);               // 3. sobe o servidor na porta
```

## `.gitignore` e `.env`

```text
node_modules/
dist/
.env
```

```typescript
// .env
PORT=3000
```

```typescript
import "dotenv/config"; // npm i dotenv
const PORT = process.env.PORT || 3000;
app.listen(PORT);
```

## Erros comuns do setup

| Erro | Causa |
| --- | --- |
| `Cannot find module 'express'` | Falta `@types/express` em dev ou express não instalado |
| `req.body` é `undefined` | Falta `app.use(express.json())` |
| `import` não funciona | `module` errado no tsconfig ou rodando `.ts` direto com node |
| Porta ocupada | `EADDRINUSE` — mude a porta ou mate o processo |

## Resumo

- `express` + `@types/express` + `ts-node-dev` = base
- `app.use(express.json())` antes de qualquer rota que lê body
- Scripts: `dev` com reload, `build` com tsc, `start` com node
- `.env` + `dotenv` para porta e segredos
