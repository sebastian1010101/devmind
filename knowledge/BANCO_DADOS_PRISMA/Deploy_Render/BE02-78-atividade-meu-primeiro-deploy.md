# BE02-78 — Atividade: Meu Primeiro Deploy

## Objetivo

Colocar a API no ar: banco Postgres no Render, web service conectado ao GitHub, migrations aplicadas e endpoint respondendo publicamente.

## Checklist

```text
1. Projeto com build/start configurados
2. Repo no GitHub (sem .env commitado)
3. PostgreSQL criado no Render
4. Web Service criado apontando pro repo
5. Env vars configuradas
6. Migrations aplicadas
7. Endpoint público respondendo
```

## Preparação do projeto

```json
{
  "scripts": {
    "dev": "ts-node-dev src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "postinstall": "prisma generate"
  }
}
```

```ts
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server on ${PORT}`));
```

```gitignore
node_modules/
dist/
.env
```

## Passos no Render

```text
1. New → PostgreSQL
   Name: minha-api-db | Plan: Free
   → copie a Internal Database URL

2. New → Web Service → connect repo
   Build:  npm install && npm run build && npx prisma migrate deploy
   Start:  npm run start

3. Environment:
   DATABASE_URL = <internal url do passo 1>
   JWT_SECRET   = <novo segredo>
   NODE_ENV     = production

4. Create → acompanhe os logs do deploy
```

## Testando

```bash
curl https://sua-api.onrender.com/vagas
# → JSON ou rota conhecida respondendo

curl -X POST https://sua-api.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"a@a.com","senha":"12345678"}'
```

## Verificações finais

1. `GET` público retorna dados
1. Rota protegida → `401` sem token, ok com token
1. Migrations rodaram (tabelas existem — confira pelo Studio na URL externa)
1. Cold start tolerado — primeira request após sleep demora

## Erros comuns

| Erro | Correção |
| --- | --- |
| Build falha | Rode `npm run build` local primeiro — corrija e pushe |
| 503 persistente | Logs → provavelmente `start` ou `DATABASE_URL` |
| Migration travou | URL interna acessível? `migrate deploy` rodou? |
| Rotas 404 | Confirme que `app.ts`/`server.ts` compilados exportam certo |

## Critérios de conclusão

1. URL pública respondendo
1. Auth funciona em produção (register → login → rota protegida)
1. `.env` fora do git; secrets só no painel do Render
1. README atualizado com a URL de produção

## Resumo

- Deploy = repo limpo + build/start corretos + Postgres gerenciado + env vars
- `migrate deploy` no build command sobe o schema junto
- Teste do zero: `curl` nas rotas públicas e protegidas
