# BE01-56 — Zod: Introdução

## O que é

Biblioteca de **validação de schemas** — declara o formato esperado e o Zod valida em runtime:

```bash
npm install zod
```

```typescript
import { z } from "zod";

const usuarioSchema = z.object({
  nome: z.string().min(3),
  email: z.string().email(),
  idade: z.number().int().positive().optional(),
});

usuarioSchema.parse({
  nome: "Ana",
  email: "ana@email.com",
}); // ✅ passa — retorna os dados tipados
```

## O superpoder: validação + tipo juntos

```typescript
const usuarioSchema = z.object({
  nome: z.string(),
  email: z.string().email(),
});

// O tipo TypeScript é derivado DO schema — fonte única
type Usuario = z.infer<typeof usuarioSchema>;
// { nome: string; email: string }
```

Declarou uma vez — tem validação runtime **e** tipo compile-time.

## parse vs safeParse

```typescript
// parse — lança ZodError se inválido (ideal com handleErrors)
const dados = usuarioSchema.parse(req.body);

// safeParse — retorna resultado sem lançar
const resultado = usuarioSchema.safeParse(req.body);
if (!resultado.success) {
  resultado.error.issues; // lista de problemas
} else {
  resultado.data;         // dados válidos e tipados
}
```

## Os validadores principais

```typescript
z.string().min(3).max(100).email().url().uuid().regex(/^\d{8}$/)
z.number().int().positive().min(0).max(150)
z.boolean()
z.array(z.string()).min(1)
z.enum(["ADMIN", "USER"])
z.date()
z.literal("valor exato")
z.union([z.string(), z.number()])
z.null(), z.undefined(), z.any()
```

## Modificadores

```typescript
z.string().optional()           // pode não vir
z.string().nullable()           // pode ser null
z.string().default("user")      // preenche se ausente
z.string().min(3, "Mínimo 3")   // mensagem customizada
```

## Objeto complexo

```typescript
const produtoSchema = z.object({
  nome: z.string().min(3, "Nome muito curto"),
  preco: z.number().positive("Preço deve ser positivo"),
  categorias: z.array(z.string()).min(1),
  tags: z.array(z.string()).optional(),
  destaque: z.boolean().default(false),
});
```

## O erro — ZodError

```typescript
try {
  schema.parse(dados);
} catch (e) {
  if (e instanceof z.ZodError) {
    e.issues;    // [{ path: ["preco"], message: "...", code: "..." }]
    e.flatten(); // { fieldErrors: { preco: ["..."] } } — formato de API
  }
}
```

## Resumo

- Zod = schema declarativo que valida em runtime
- `z.infer` deriva o tipo TS do schema — validação e tipo de uma fonte só
- `parse` lança; `safeParse` retorna
- Cadeia fluente: `.min().max().email().optional().default()`
