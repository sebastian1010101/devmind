# BE01-61 — Zod: Relacionando o Middleware de Validação com HandleErrors

## Duas abordagens para o erro de validação

```typescript
// Abordagem A — safeParse no middleware, responde 400 ali
const resultado = schema.safeParse(req.body);
if (!resultado.success) {
  return res.status(400).json({ errors: resultado.error.flatten().fieldErrors });
}

// Abordagem B — parse lança ZodError, handleErrors global trata
req.body = schema.parse(req.body);
next();
```

| A (responde no middleware) | B (lança pro handleErrors) |
| --- | --- |
| Erro formatado ali mesmo | Um ponto central traduz TODOS os erros |
| Duplica o formato de erro | Formato único no `handleErrors` |
| Middleware não depende de nada | Middleware de 3 linhas |

Abordagem B é a do curso — **um lugar decide como erro vira resposta**.

## O handleErrors completo

```typescript
// src/middlewares/handleErrors.middleware.ts
import { Request, Response, NextFunction } from "express";
import { ZodError } from "zod";
import { AppError } from "../errors/AppError";

export const handleErrors = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // 1. Erros de validação → 400 com detalhes por campo
  if (err instanceof ZodError) {
    return res.status(400).json({
      message: "Dados inválidos",
      errors: err.flatten().fieldErrors,
    });
  }

  // 2. Erros de domínio → statusCode próprio
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ message: err.message });
  }

  // 3. Inesperado → log + 500 neutro
  console.error(err);
  return res.status(500).json({ message: "Erro interno do servidor" });
};
```

## O pipeline completo de erro

```text
validate("body")(schema)
    → schema.parse lança ZodError
         ↓
service lança: throw new NotFoundError("Produto")
         ↓
handleErrors decide pela CLASSE do erro:

  ZodError   → 400 + fieldErrors
  AppError   → statusCode + message
  qualquer   → 500 neutro + log
```

## Ordem de verificação

`ZodError` antes de `AppError` — são classes independentes, mas a convenção é: mais específico primeiro, genérico (inesperado) por último.

## O middleware de validação final

```typescript
export const validate =
  (fonte: "body" | "query" | "params") =>
  (schema: ZodSchema) =>
  (req: Request, res: Response, next: NextFunction) => {
    req[fonte] = schema.parse(req[fonte]); // lança → handleErrors pega
    next();
  };
```

Simples porque **delegou o erro** — a responsabilidade de formato é do handleErrors.

## A cadeia de responsabilidades

| Quem | Faz |
| --- | --- |
| Schema | define o que é válido |
| `validate` | executa o parse, substitui `req[fonte]` |
| `handleErrors` | traduz qualquer erro pra HTTP |
| Service | lança `AppError` de domínio |

## Resumo

- `parse` lança → `handleErrors` centraliza tradução de erros
- Ordem: `ZodError` → `400` campos; `AppError` → `statusCode`; resto → `500`
- Middleware de validação fica mínimo — o formato de erro é centralizado
- Cada erro tem uma classe; cada classe tem um destino no handler
