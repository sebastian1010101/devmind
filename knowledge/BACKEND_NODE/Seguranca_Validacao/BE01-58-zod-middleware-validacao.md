# BE01-58 — Zod: Middleware para Validação de Dados

## O problema

`safeParse` dentro de cada controller = código repetido em todas as rotas:

```typescript
// ❌ repete em todo endpoint
const r = schema.safeParse(req.body);
if (!r.success) return res.status(400).json(...);
```

## A solução — middleware factory

```typescript
// src/middlewares/validateBody.middleware.ts
import { Request, Response, NextFunction } from "express";
import { ZodSchema } from "zod";

export const validateBody =
  (schema: ZodSchema) =>
  (req: Request, res: Response, next: NextFunction) => {
    req.body = schema.parse(req.body); // lança ZodError se inválido
    next();
  };
```

## Uso na rota

```typescript
import { produtoSchema } from "../schemas/produto.schema";
import { validateBody } from "../middlewares/validateBody.middleware";

router.post("/", validateBody(produtoSchema), controller.criar);
router.patch("/:id", validateBody(produtoSchema.partial()), controller.atualizar);
```

A validação virou **uma linha declarativa** na rota — controller recebe body já limpo e tipado.

## Por que `schema.parse` (e não safeParse)

```typescript
req.body = schema.parse(req.body); // lança ZodError
```

O erro **lançado** cai no `handleErrors` global — que já sabe traduzir `ZodError` para `400` (BE01-61). O middleware fica de 3 linhas e o tratamento é centralizado.

## Organização dos schemas

```text
src/
└── schemas/
    ├── produto.schema.ts    → produtoSchema, produtoUpdateSchema
    ├── usuario.schema.ts
    └── pedido.schema.ts
```

```typescript
// schemas/produto.schema.ts
export const produtoSchema = z.object({
  nome: z.string().min(3),
  preco: z.number().positive(),
});

export const produtoUpdateSchema = produtoSchema.partial(); // tudo opcional

export type CreateProdutoDTO = z.infer<typeof produtoSchema>;
export type UpdateProdutoDTO = z.infer<typeof produtoUpdateSchema>;
```

## O ganho total

```text
schema (1 fonte) ──→ z.infer → tipo TS (compile)
                ──→ parse → validação (runtime)
                ──→ middleware → aplicado na rota

Controller: req.body JÁ é CreateProdutoDTO garantido
Service: recebe dados validados
Erro: handleErrors traduz ZodError → 400
```

## Tipagem no controller

```typescript
// O body passou pelo schema — confie no tipo
criar = (req: Request, res: Response) => {
  const dados: CreateProdutoDTO = req.body; // seguro pós-middleware
  return res.status(201).json(this.service.criar(dados));
};
```

## Resumo

- `validateBody(schema)` = middleware factory — uma linha por rota
- `parse` lança → `handleErrors` global traduz pra 400
- Schemas em `schemas/` — derivados com `.partial()` para PATCH
- Controller e service recebem dados garantidos e tipados
