# BE02-76 — Deploy: Build, Start e Migrate

## Os três comandos do deploy

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node-dev src/server.ts"
  }
}
```

| Comando | Quando | O que faz |
| --- | --- | --- |
| `build` | No deploy | Compila TS → `dist/` |
| `migrate` | No deploy | Aplica migrations pendentes |
| `start` | Todo boot | Sobe o servidor compilado |

## Build — compilando TS

```json
// tsconfig.json — o essencial para prod
{
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

```bash
npm run build     # gera dist/
node dist/server.js
```

O Render roda `npm install` + `npm run build` automaticamente — devDependencies (`typescript`, `ts-node-dev`) existem no build, não no runtime.

## Migrate — schema do banco

```bash
npx prisma migrate deploy
```

| Comando | Uso |
| --- | --- |
| `migrate dev` | Só desenvolvimento — cria migrations |
| `migrate deploy` | Produção — só aplica pendentes, não gera |

No Render, o deploy roda:

```text
Build Command:  npm install && npm run build && npx prisma migrate deploy
Start Command:  npm run start
```

Ou separe: build com `migrate deploy` embutido — o banco já sobe migrado.

## generate — o client no build

```json
"postinstall": "prisma generate"
```

`prisma generate` no `postinstall` garante o Client tipado no build — sem isso, `@prisma/client` não existe no node_modules de prod.

## Start — o entrypoint de produção

```ts
// src/server.ts
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`on ${PORT}`));
```

- `process.env.PORT` — o Render define a porta real
- `node dist/server.js` — sem `ts-node-dev`, sem watch
- Erro no start = deploy falha → logs do Render mostram

## Ordem típica do pipeline

```text
git push
  ↓
npm install            (deps + devDeps; postinstall → prisma generate)
npm run build          (tsc → dist/)
npx prisma migrate deploy   (schema no banco)
npm run start          (node dist/server.js)
  ↓
health check → live
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `prisma.user` undefined em prod | Falta `postinstall: prisma generate` |
| `migrate dev` no build | `migrate deploy` — dev é local |
| Build passa local, falha no Render | `tsc` strict pega erros que dev ignora — builde local antes |
| App escuta porta fixa | `process.env.PORT` |
| Migration falha no deploy | Banco remoto inacessível ou migration quebrada — confira `DATABASE_URL` |

## Resumo

- `build` = `tsc` → `dist/`; `start` = `node dist/server.js`
- `migrate deploy` aplica o schema no banco de produção
- `postinstall: prisma generate` mantém o Client disponível no build
- O deploy é a sequência: install → build → migrate → start
