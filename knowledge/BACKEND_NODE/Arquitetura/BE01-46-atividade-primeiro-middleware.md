# BE01-46 — Atividade: Meu Primeiro Middleware

Exercício: criar middlewares reais e entender a ordem do pipeline.

## 1. Logger de requisições

```typescript
// src/middlewares/logger.middleware.ts
import { Request, Response, NextFunction } from "express";

export const logger = (req: Request, res: Response, next: NextFunction) => {
  const inicio = Date.now();

  res.on("finish", () => {
    const duracao = Date.now() - inicio;
    console.log(`${req.method} ${req.path} → ${res.statusCode} (${duracao}ms)`);
  });

  next();
};
```

`res.on("finish")` dispara quando a resposta termina — mede o tempo total.

## 2. Guarda de horário

```typescript
export const horarioComercial = (req: Request, res: Response, next: NextFunction) => {
  const hora = new Date().getHours();
  if (hora < 8 || hora >= 18) {
    return res.status(403).json({ message: "Fora do horário comercial" });
  }
  next();
};
```

## 3. Middleware que anexa dados

```typescript
export const marcaRequest = (req: Request, res: Response, next: NextFunction) => {
  res.locals.requestId = crypto.randomUUID();
  res.locals.inicio = Date.now();
  next();
};

// no handler:
app.get("/ping", (req, res) => {
  res.json({ requestId: res.locals.requestId });
});
```

## Montando

```typescript
app.use(marcaRequest);            // 1. anexa dados
app.use(logger);                  // 2. loga tudo
app.use("/admin", horarioComercial); // 3. só rotas /admin
app.use("/tarefas", tarefasRouter);
```

## Experimento — a ordem

```typescript
app.use((req, res, next) => { console.log("A"); next(); });
app.use((req, res, next) => { console.log("B"); next(); });
app.get("/x", (req, res) => { console.log("C"); res.send("ok"); });
// GET /x → logs: A, B, C — pipeline sequencial
```

Troque a ordem e veja o que acontece quando um middleware não chama `next()`.

## Checklist

- [ ] `next()` sempre chamado (senão a request trava)
- [ ] `return` antes de `res.*` quando bloqueia
- [ ] `res.locals` para dados entre middlewares
- [ ] Middleware por último não alcança rotas já respondidas

## Desafios

1. Rate limit simples: conte requests por IP, bloqueie após N por minuto
2. Middleware `validaId` — `req.params.id` deve ser número, senão `400`
3. Middleware que mede tempo e adiciona header `X-Response-Time`

## Resumo

- Middlewares comuns: logger, auth, validação, rate limit
- `res.on("finish")` mede o ciclo completo
- `next()` ausente = request pendurada
