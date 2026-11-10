# BE01-63 — Zod: Infer

## `z.infer` — o tipo nasce do schema

```typescript
const produtoSchema = z.object({
  nome: z.string().min(3),
  preco: z.number().positive(),
  ativo: z.boolean().default(true),
});

type Produto = z.infer<typeof produtoSchema>;
// { nome: string; preco: number; ativo: boolean }
```

O schema é a **fonte única**: validação e tipo sempre sincronizados.

## `z.input` vs `z.output` — antes e depois do parse

```typescript
const schema = z.object({
  pagina: z.coerce.number().default(1),
});

type Input = z.input<typeof schema>;   // { pagina?: unknown } — o que chega
type Output = z.output<typeof schema>; // { pagina: number } — o que sai
```

- `z.input` — formato **antes** do parse (string de query, defaults ausentes)
- `z.output` (= `z.infer`) — formato **depois** do parse (tipado, defaults aplicados)

## Ligando schema → tipo → service

```typescript
// schemas/usuario.schema.ts
export const createUsuarioSchema = z.object({
  nome: z.string().min(3),
  email: z.string().email(),
  senha: z.string().min(8),
});

export type CreateUsuarioDTO = z.infer<typeof createUsuarioSchema>;
```

```typescript
// services — usa o tipo inferido
class UsuarioService {
  criar(dados: CreateUsuarioDTO): Usuario { /* ... */ }
}
```

```typescript
// controller — req.body já passou no middleware
criar = (req: Request, res: Response) => {
  const dados: CreateUsuarioDTO = req.body;
  return res.status(201).json(this.service.criar(dados));
};
```

Nenhuma interface manual — o DTO **é** o schema inferido.

## infer em schemas derivados

```typescript
const updateSchema = createUsuarioSchema.partial();
type UpdateUsuarioDTO = z.infer<typeof updateSchema>;
// { nome?: string; email?: string; senha?: string }

const responseSchema = usuarioSchema.omit({ senha: true });
type UsuarioResponse = z.infer<typeof responseSchema>;
// { id, nome, email, criadoEm } — sem senha, garantido
```

## Quando interface vs infer

| Interface manual | `z.infer` |
| --- | --- |
| Entidade de banco (modelo interno) | DTOs de entrada/saída da API |
| Contratos de camada (repository) | Tudo que tem schema Zod |
| Não precisa de validação | Precisa validar dados externos |

Fronteira (request) → Zod + infer. Interior (service, repo) → interfaces/classicas.

## infer + refinements

```typescript
const schema = z.object({
  email: z.string().email().transform((e) => e.toLowerCase()),
});

type Output = z.infer<typeof schema>; // string — o transform não muda o tipo final
```

Se o transform mudasse o tipo (`z.string().transform(Number)`), o infer reflete o **resultado**: `number`.

## Resumo

- `z.infer<typeof schema>` — tipo TS derivado do schema, zero duplicação
- `z.input` = antes do parse; `z.output`/`z.infer` = depois
- Schema → DTO → service — validação e tipo de uma fonte só
- Interfaces manuais para o interior; infer para as fronteiras
