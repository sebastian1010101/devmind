# BE01-54 — Utilizando Helmet para Prevenir Ataques

## O que é

Middleware que configura **headers HTTP de segurança** automaticamente:

```bash
npm install helmet
```

```typescript
import helmet from "helmet";

app.use(helmet()); // antes das rotas
```

## O que ele configura

| Header | Protege contra |
| --- | --- |
| `Content-Security-Policy` | XSS — controla quais recursos o browser pode carregar |
| `X-Content-Type-Options: nosniff` | MIME sniffing — browser "adivinhando" tipo errado |
| `X-Frame-Options: DENY` | Clickjacking — seu site dentro de iframe alheio |
| `Strict-Transport-Security` | Força HTTPS |
| `X-Powered-By` | **Remove** — não anuncia que é Express |
| `Referrer-Policy` | Controla o que vai no Referer |

## Antes vs depois

```text
ANTES:
X-Powered-By: Express        ← "oi, sou Express — ataque conhecido X"

DEPOIS (com helmet):
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=15552000
```

## Configuração fina

```typescript
// Ajustar políticas específicas
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "trusted.cdn.com"],
      },
    },
  })
);

// Desligar uma proteção específica (ex.: API que serve iframe legítimo)
app.use(helmet({ frameguard: false }));
```

## Helmet não é suficiente — ele é uma camada

```text
helmet()       → headers
+ cors()       → quem pode chamar
+ rate-limit   → quantas vezes
+ validação    → o que entra
+ auth         → quem é
```

## Companheiros habituais

```typescript
import cors from "cors";
import rateLimit from "express-rate-limit";

app.use(helmet());
app.use(cors({ origin: "https://meu-front.com" })); // não "*" em produção

app.use(
  rateLimit({
    windowMs: 15 * 60 * 1000, // 15 min
    max: 100,                  // 100 requests por IP
  })
);
```

## Resumo

- `app.use(helmet())` = ~10 headers de segurança em uma linha
- Esconde `X-Powered-By`, previne clickjacking, MIME sniffing, XSS
- Uma camada entre várias — cors, rate limit e validação completam
