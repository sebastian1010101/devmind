# BE02-77 — Render: Criando um Web Service

## Passo a passo

```text
Dashboard → New → Web Service → Connect repository (GitHub)
```

1. Escolhe o repo da API
1. Configura o serviço:

| Campo | Valor |
| --- | --- |
| Name | `minha-api` (vira `minha-api.onrender.com`) |
| Region | mesma do banco |
| Branch | `main` |
| Build Command | `npm install && npm run build && npx prisma migrate deploy` |
| Start Command | `npm run start` |

## Environment — as variáveis

```text
Environment → Add Environment Variable:

DATABASE_URL  → Internal Database URL do Postgres do Render
JWT_SECRET    → segredo forte (gere um novo pra prod)
NODE_ENV      → production
```

A `DATABASE_URL` usa a **internal** — mesma rede, sem latência externa.

## Deploy

```text
Create Web Service → primeiro deploy começa
├─ Logs ao vivo — install, build, migrate, start
├─ "Your service is live 🎉" → https://minha-api.onrender.com
└─ push novo → redeploy automático (auto-deploy ligado por padrão)
```

## Verificando

```bash
curl https://minha-api.onrender.com/vagas
```

```text
primeira request pode demorar — free tier acorda do sleep
```

## Auto-deploy

- Push na `main` → redeploy automático
- Desative em Settings se quiser deploy manual (`Manual Deploy → Deploy latest commit`)

## Domínio e HTTPS

- `*.onrender.com` já tem HTTPS gerenciado
- Domínio próprio: Settings → Custom Domain + DNS

## Logs e debugging

```text
Dashboard → Logs    → stdout/stderr do processo
            Events  → deploys, falhas, restarts
            Shell   → terminal dentro do container (paid)
```

`console.log` cai nos logs — erros de boot aparecem ali.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Deploy falha no build | Log mostra o erro — geralmente `tsc` ou migration |
| `Application failed to respond` | Start não escuta `process.env.PORT` |
| API não acha o banco | `DATABASE_URL` errada — internal URL, não external |
| Service dorme | Free tier — primeiro acesso acorda (cold start) |
| Env var não lida | Salvou a variável? Redeploy depois de adicionar |

## Resumo

- Web Service = repo + build command + start command + env vars
- `DATABASE_URL` interna no painel; `JWT_SECRET` novo para prod
- Logs do dashboard são o primeiro lugar de debug
- Auto-deploy em push — desligável se quiser controle manual
