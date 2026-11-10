# BE02-75 — CORS (Cross-Origin Resource Sharing)

## O problema

```text
Front: http://localhost:5173   (Vite)
API:   https://minha-api.onrender.com
```

Origens diferentes → o **navegador** bloqueia a resposta. É regra do browser, não do servidor — Postman/curl não sofrem CORS.

```text
browser: "servidor, posso ler a resposta pra outra origem?"
server:  "Access-Control-Allow-Origin: ..." → sim/não
```

## O que CORS é e não é

- É mecanismo de **permissão do navegador** — não é autenticação
- Sem CORS configurado, o front vê erro mesmo com a API respondendo `200`
- Preflight (`OPTIONS`) acontece antes de requests não-simples (JSON, headers custom)

## Configurando no Express

```bash
npm install cors
npm install -D @types/cors
```

```ts
import cors from "cors";

const app = express();
app.use(cors());                    // libera tudo — ok pra dev
```

## Restringindo em produção

```ts
app.use(cors({
  origin: "https://meu-front.vercel.app",   // só esse front
  methods: ["GET", "POST", "PATCH", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
}));
```

```ts
// múltiplas origens
app.use(cors({
  origin: ["https://app.com", "https://admin.app.com"],
}));
```

## Origem dinâmica

```ts
app.use(cors({
  origin: (origin, callback) => {
    const permitidas = ["https://meu-front.vercel.app", "http://localhost:5173"];
    if (!origin || permitidas.includes(origin)) {
      callback(null, true);                 // permite (e requests sem origem: curl)
    } else {
      callback(new Error("CORS bloqueado"));
    }
  },
}));
```

## O preflight

```text
PUT /recurso + Content-Type: application/json
        ↓
OPTIONS /recurso    ← navegador pergunta antes (preflight)
        ↓
Access-Control-Allow-* headers → ok → request real vai
```

O middleware `cors` responde `OPTIONS` automaticamente.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `blocked by CORS policy` no console | `app.use(cors())` antes das rotas |
| Funciona no Postman, não no browser | Normal — CORS é só browser; configure no Express |
| `Authorization` header bloqueado | `allowedHeaders` precisa incluir `Authorization` |
| Credentials (cookies) falham | `credentials: true` + origin específico (não `*`) |
| CORS depois das rotas | Middleware de CORS vem **antes** das rotas |

## Resumo

- CORS é regra do navegador — API responde, browser bloqueia a leitura
- `app.use(cors())` antes das rotas; em prod, `origin` restrita ao front real
- Preflight (`OPTIONS`) automaticamente tratado pelo middleware
- `allowedHeaders` precisa cobrir `Authorization` para JWT funcionar
