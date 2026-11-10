# BE01-62 — Zod: Omit, Pick e Partial

## Schemas derivados — sem reescrever

Zod tem os mesmos conceitos dos utility types do TS — mas para **schemas**:

```typescript
const usuarioSchema = z.object({
  id: z.number(),
  nome: z.string().min(3),
  email: z.string().email(),
  senha: z.string().min(8),
  criadoEm: z.date(),
});
```

## `.partial()` — tudo opcional (PATCH)

```typescript
const updateUsuarioSchema = usuarioSchema.partial();
// todos os campos viram .optional()

// PATCH /usuarios/42 — cliente manda só o que muda
```

`.partial()` profundo: `usuarioSchema.deepPartial()` para objetos aninhados.

## `.omit()` — remove campos

```typescript
const createUsuarioSchema = usuarioSchema.omit({
  id: true,
  criadoEm: true,
});
// { nome, email, senha } — id e data o servidor gera
```

## `.pick()` — seleciona campos

```typescript
const loginSchema = usuarioSchema.pick({
  email: true,
  senha: true,
});
// { email, senha }
```

## `.extend()` — adiciona campos

```typescript
const cadastroSchema = createUsuarioSchema.extend({
  confirmarSenha: z.string(),
}).refine((d) => d.senha === d.confirmarSenha, {
  message: "Senhas não conferem",
  path: ["confirmarSenha"],
});
```

## O mapa completo de derivações

```typescript
// Base
const usuarioSchema = z.object({ /* ... */ });

// Create — sem id/criadoEm
const createSchema = usuarioSchema.omit({ id: true, criadoEm: true });

// Update — base do create, tudo opcional
const updateSchema = createSchema.partial();

// Response — sem senha
const responseSchema = usuarioSchema.omit({ senha: true });

// Login — só email + senha
const loginSchema = usuarioSchema.pick({ email: true, senha: true });
```

Um schema base → 4 contratos derivados. Mudou o `email` no base? Todos seguem.

## Comparativo TS vs Zod

| TypeScript (compile-time) | Zod (runtime) |
| --- | --- |
| `Partial<T>` | `schema.partial()` |
| `Omit<T, K>` | `schema.omit({ k: true })` |
| `Pick<T, K>` | `schema.pick({ k: true })` |
| `T & { extra }` | `schema.extend({ extra })` |
| `Readonly<T>` | `schema.readonly()` |

Mesmos conceitos, alvos diferentes — tipo vs validação.

## Resumo

- `.partial()` → PATCH; `.omit()` → create/response; `.pick()` → login
- `.extend()` + `.refine()` → cadastro com confirmação
- Schema base único — contratos derivados seguem sozinhos
- Espelha os utility types: mesma família, runtime vs compile-time
