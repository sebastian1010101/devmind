# BE02-73 — Render: Primeiros Passos

## O que é o Render

Plataforma de deploy (PaaS) — sobe sua API e seu banco Postgres gerenciados, sem administrar servidor.

```text
git push → Render detecta → build → start → URL pública
```

## O que você vai criar

| Recurso | O que é |
| --- | --- |
| **PostgreSQL** (managed) | O banco — Render hospeda e gerencia |
| **Web Service** | A API — builda do seu repo e serve HTTP |
| **Environment variables** | `.env` da produção — configurado no painel |

## Conta e conexão com GitHub

1. Criar conta em `render.com` (GitHub login é o caminho mais rápido)
1. O serviço conecta ao repositório — push → redeploy automático
1. Free tier: webservice dorme após inatividade (cold start de ~30s no primeiro acesso)

## O fluxo de deploy

```text
┌──────────┐   git push    ┌──────────┐
│  GitHub  │ ────────────► │  Render  │
└──────────┘               │ build: npm run build
                           │ start: npm run start
                           │ env: DATABASE_URL, JWT_SECRET
                           └────┬─────┘
                                ▼
                    https://minha-api.onrender.com
```

## Antes de subir — checklist do projeto

- `npm run build` gera `dist/` (TypeScript compilado)
- `npm run start` roda `node dist/server.js` — **não** `ts-node-dev`
- `app.listen(process.env.PORT)` — a porta vem da plataforma, não fixa
- `.env` fora do git — variáveis vão no painel do Render

## O que NÃO vai pro deploy

```text
.env                  → variáveis no painel do Render
node_modules/         → build instala do zero
ts-node-dev, jest     → devDependencies — build não usa
```

## Free tier — as limitações

- **Sleep**: sem tráfego, o serviço dorme — primeira request demora
- **Banco free expira**: Postgres gratuito do Render expira após ~90 dias (planeje migrar ou backup)
- Um deploy por vez por serviço

## Erros comuns

| Erro | Correção |
| --- | --- |
| `start` aponta para `ts-node-dev` | Start é `node dist/...` — dev tools não existem em prod |
| Porta fixa 3000 | `process.env.PORT` — o Render atribui a porta |
| `.env` commitado | Variáveis vão no painel Environment |
| Push sem build testado | `npm run build` local primeiro — o erro aparece antes |

## Resumo

- Render = banco gerenciado + web service que builda do GitHub
- Push → build → start automático; env vars no painel
- `start` usa código compilado (`dist/`), porta de `process.env.PORT`
- Free tier dorme sem tráfego e o Postgres expira — bom pra estudo, ciente dos limites
