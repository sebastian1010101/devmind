# BE01-60 — Atividade: Refinando Middleware de Validação de Dados

Exercício: middleware de validação completo — fontes, erros formatados, tipagem.

## Versão refinada

```typescript
// src/middlewares/validate.middleware.ts
import { Request, Response, NextFunction } from "express";
import { ZodSchema } from "zod";

type Fonte = "body" | "query" | "params";

export const validate =
  (fonte: Fonte) =>
  (schema: ZodSchema) =>
  (req: Request, res: Response, next: NextFunction) => {
    const resultado = schema.safeParse(req[fonte]);

    if (!resultado.success) {
      return res.status(400).json({
        message: "Dados inválidos",
        errors: resultado.error.flatten().fieldErrors,
      });
    }

    req[fonte] = resultado.data; // substitui pelo dado parseado/transformado
    next();
  };
```

Aqui `safeParse` no middleware — retorno `400` direto, sem depender do error-handler. (As duas abordagens funcionam; BE01-61 compara.)

## Schemas de uma API real

```typescript
// schemas/produto.schema.ts
export const createProdutoSchema = z.object({
  nome: z.string().min(3).max(100),
  preco: z.number().positive(),
  categoria: z.enum(["A", "B", "C"]),
});

export const updateProdutoSchema = createProdutoSchema.partial();

export const produtoParamsSchema = z.object({
  id: z.coerce.number().int().positive(),
});

export const produtoQuerySchema = z.object({
  pagina: z.coerce.number().int().min(1).default(1),
  categoria: z.enum(["A", "B", "C"]).optional(),
  busca: z.string().trim().optional(),
});
```

## Aplicando em todas as rotas

```typescript
router.get(
  "/",
  validate("query")(produtoQuerySchema),
  controller.listar
);

router.get(
  "/:id",
  validate("params")(produtoParamsSchema),
  controller.buscar
);

router.post(
  "/",
  validate("body")(createProdutoSchema),
  controller.criar
);

router.patch(
  "/:id",
  validate("params")(produtoParamsSchema),
  validate("body")(updateProdutoSchema), // dois middlewares em sequência
  controller.atualizar
);
```

## Testando

```bash
# Query inválida
curl "http://localhost:3000/produtos?pagina=abc"
# 400 { "errors": { "pagina": ["Expected number..."] } }

# Param inválido
curl http://localhost:3000/produtos/xyz
# 400 { "errors": { "id": ["..."] } }

# Body inválido
curl -X POST /produtos -d '{"nome":"ab"}'
# 400 { "errors": { "nome": [...], "preco": ["Required"], "categoria": ["Required"] } }
```

## Checklist

- [ ] Um middleware, três fontes (`body`/`query`/`params`)
- [ ] `safeParse` retorna `400` com `fieldErrors` formatados
- [ ] `req[fonte]` substituído pelo dado parseado (com transforms/defaults)
- [ ] Múltiplos middlewares encadeados na mesma rota
- [ ] `.partial()` para PATCH, `coerce` para params/query

## Resumo

- `validate(fonte)(schema)` cobre as três fontes de input
- Substituir `req[fonte]` propaga dados normalizados adiante
- Encadeie middlewares: params E body validados no mesmo PATCH
