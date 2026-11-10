# BE01-63-1 — Projeto: API de Livros — Parte 2

> **Status: [NO IMPLEMENT]** — anotações de referência sobre o escopo.

## Escopo esperado

Evolução do projeto da Parte 1 (BE01-53-1) adicionando a camada de validação:

- Schemas Zod para create/update de livros
- Middleware `validate("body"|"query"|"params")` nas rotas
- `handleErrors` traduzindo `ZodError` → `400` com `fieldErrors`
- Tipos inferidos com `z.infer` alimentando os services
- Validação de `req.params` (`:id`) e `req.query` (filtros/paginação)

## Esqueleto de referência

```typescript
export const createLivroSchema = z.object({
  titulo: z.string().min(1),
  autor: z.string().min(3),
  ano: z.number().int().min(1450).max(new Date().getFullYear()),
});

export const updateLivroSchema = createLivroSchema.partial();
export type CreateLivroDTO = z.infer<typeof createLivroSchema>;
```

```typescript
router.post("/", validate("body")(createLivroSchema), controller.criar);
router.patch("/:id",
  validate("params")(idSchema),
  validate("body")(updateLivroSchema),
  controller.atualizar
);
```

## Checklist do projeto completo

- Arquitetura em camadas (BE01-43..52)
- `AppError` + `handleErrors` (BE01-49/50)
- `helmet()` + boas práticas OWASP (BE01-53/54)
- Validação Zod em middleware (BE01-56..61)
- Schemas derivados + `z.infer` (BE01-62/63)

## Resumo

- Parte 2 = Parte 1 + validação completa com Zod
- Não implementado — referência para implementação futura
- Consolida tudo do módulo 06 antes do Prisma (módulo 07)
