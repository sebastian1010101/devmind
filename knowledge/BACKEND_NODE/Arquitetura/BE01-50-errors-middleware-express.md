# BE01-50 — Errors: Middleware para Lidar com Erros no Express

## O error-handler — 4 parâmetros

```typescript
// src/middlewares/handleErrors.middleware.ts
import { Request, Response, NextFunction } from "express";
import { AppError } from "../errors/AppError";

export const handleErrors = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ message: err.message });
  }

  console.error(err); // erro inesperado — loga para investigar
  return res.status(500).json({ message: "Erro interno do servidor" });
};
```

O Express reconhece o handler pelos **4 parâmetros** — a assinatura é a mágica.

## Registro — por último, depois das rotas

```typescript
const app = express();

app.use(express.json());
app.use("/produtos", produtosRouter);
app.use("/usuarios", usuariosRouter);

app.use(handleErrors); // ← SEMPRE por último
```

Middleware registrado antes das rotas nunca vê os erros delas.

## O fluxo completo

```text
Service lança: throw new NotFoundError("Produto")
       ↓
Express captura (sync) ou next(e) (async)
       ↓
Procura o primeiro middleware com 4 parâmetros
       ↓
handleErrors: instanceof AppError? → statusCode + message
              não? → log + 500 genérico
```

## Tratando erros conhecidos

```typescript
import { ZodError } from "zod";

export const handleErrors = (err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ message: err.message });
  }

  if (err instanceof ZodError) {
    return res.status(400).json({
      message: "Dados inválidos",
      errors: err.flatten().fieldErrors,
    });
  }

  console.error(err);
  return res.status(500).json({ message: "Erro interno" });
};
```

Um único ponto decide como cada tipo de erro vira resposta — BE01-61 integra com Zod.

## Async — o detalhe que morde

```typescript
// ❌ Express 4 — promise rejeitada NÃO chega no error-handler
app.get("/x", async (req, res) => {
  throw new AppError("falhou");
});

// ✅ captura manual
app.get("/x", async (req, res, next) => {
  try {
    /* ... */
  } catch (e) {
    next(e);
  }
});

// ✅ ou wrapper global
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get("/x", asyncHandler(async (req, res) => { /* ... */ }));
```

## Por que não vazar detalhes no 500

```typescript
// ❌ expõe internals — stack trace, caminhos, queries
res.status(500).json({ message: err.message, stack: err.stack });

// ✅ mensagem neutra; o erro real vai pro log do servidor
console.error(err);
res.status(500).json({ message: "Erro interno do servidor" });
```

Stack trace na resposta = informação para atacante.

## Resumo

- Error-handler: 4 parâmetros, registrado depois de todas as rotas
- `instanceof AppError` → statusCode próprio; resto → log + 500 neutro
- Async no Express 4 precisa de `try/catch` + `next(e)` ou wrapper
- Nunca vaze stack/detalhes internos na resposta
