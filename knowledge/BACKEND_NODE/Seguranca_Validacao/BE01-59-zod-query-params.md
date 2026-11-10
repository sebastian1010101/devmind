# BE01-59 — Zod: Validando req.query e req.params

## O problema

`params` e `query` são **sempre strings** — `?pagina=2` chega `"2"`, `:id=abc` chega `"abc"`. Validação manual espalha `Number()`/`isNaN()` por todo lado.

## Middleware genérico

```typescript
// src/middlewares/validate.middleware.ts
import { ZodSchema } from "zod";

type Fonte = "body" | "query" | "params";

export const validate =
  (fonte: Fonte) =>
  (schema: ZodSchema) =>
  (req: Request, res: Response, next: NextFunction) => {
    req[fonte] = schema.parse(req[fonte]);
    next();
  };
```

```typescript
router.get("/:id", validate("params")(idSchema), controller.buscar);
router.get("/", validate("query")(filtroSchema), controller.listar);
router.post("/", validate("body")(criarSchema), controller.criar);
```

## `z.coerce` — string → número

```typescript
// Query chega string — coerce converte antes de validar
const filtroSchema = z.object({
  pagina: z.coerce.number().int().positive().default(1),
  limite: z.coerce.number().int().max(100).default(20),
  busca: z.string().optional(),
});

// GET /produtos?pagina=2&limite=10
// parse({ pagina: "2", limite: "10" }) → { pagina: 2, limite: 10 } ✅
```

`z.coerce.number()` = `Number(v)` automático — essencial para query/params.

## Validando params

```typescript
const paramsSchema = z.object({
  id: z.coerce.number().int().positive("ID inválido"),
});

router.get("/:id", validate("params")(paramsSchema), controller.buscar);

// GET /produtos/abc → 400 "ID inválido" — antes mesmo do controller
```

## Booleans em query — a pegadinha

```typescript
// ?ativo=true chega "true" — string, não boolean
const schema = z.object({
  ativo: z
    .enum(["true", "false"])
    .transform((v) => v === "true")
    .optional(),
});
```

`z.coerce.boolean()` existe mas `"false"` vira `true` (string não-vazia é truthy) — prefira `enum` + `transform`.

## Transformações

```typescript
const schema = z.object({
  email: z.string().email().transform((e) => e.toLowerCase().trim()),
  tags: z
    .string()
    .transform((t) => t.split(","))
    .optional(), // ?tags=a,b,c → ["a","b","c"]
});
```

`.transform` normaliza no parse — controller recebe pronto.

## Resumo

- `validate("body"|"query"|"params")` — um middleware pras três fontes
- `z.coerce.number()` converte strings de query/params
- Boolean em query: `enum` + `transform`, nunca `coerce.boolean`
- `.transform` normaliza (lowercase, trim, split) já na validação
