# BE01-34 — O que é o Express e por que Usá-lo

## HTTP puro vs Express

```typescript
// http nativo — verboso
import http from "http";

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/usuarios") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify([{ nome: "Ana" }]));
  }
});

server.listen(3000);
```

```typescript
// Express — o mesmo, legível
import express from "express";

const app = express();
app.use(express.json());

app.get("/usuarios", (req, res) => {
  res.json([{ nome: "Ana" }]);
});

app.listen(3000);
```

Express = camada fina e minimalista sobre `http` do Node.

## O que o Express oferece

| Recurso | O que faz |
| --- | --- |
| **Rotas** | `app.get/post/patch/delete(caminho, handler)` |
| **req/res** | `req.params`, `req.query`, `req.body`; `res.json()`, `res.status()` |
| **Middlewares** | pipeline de funções `(req, res, next)` |
| **Router** | agrupamento de rotas em módulos |
| **Ecossistema** | milhares de middlewares prontos (cors, helmet, zod) |

## O que o Express NÃO faz

- Não valida dados (isso é o Zod — BE01-56)
- Não estrutura projeto (arquitetura é decisão sua — BE01-43)
- Não tem ORM, auth, testes embutidos — é minimalista por design

## Por que ainda é o padrão

- Maduro: +15 anos, bugs mapeados, docs infinitas
- Ecossistema: qualquer problema já tem middleware pronto
- Base de outros frameworks: NestJS, Feathers, etc.
- Dominado no mercado — requisito de vaga clássico

## Alternativas

| Framework | Diferença |
| --- | --- |
| **Fastify** | Mais rápido, validação com schema embutida |
| **NestJS** | Opinativo, POO + decorators + DI — Angular do backend |
| **Hono** | Ultraleve, roda em edge/serverless |
| **Koa** | Dos mesmos criadores, mais minimalista ainda |

## Resumo

- Express = wrapper minimalista sobre `http` — rotas, req/res, middlewares
- Não traz validação nem arquitetura — você monta em cima
- Padrão de mercado; alternativas: Fastify, NestJS, Hono
