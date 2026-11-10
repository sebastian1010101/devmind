# BE02-43 — Prisma: Find First

## O que é

```ts
const usuario = await prisma.usuario.findFirst({
  where: { nome: { contains: "Ana" } },
});
// → primeiro que casa, ou null
```

`findFirst` busca **um** registro por critérios **não-únicos** — retorna o primeiro que casa ou `null`.

## vs findUnique

| | `findUnique` | `findFirst` |
| --- | --- | --- |
| Critério | Só campos `@id`/`@unique` | Qualquer campo |
| Retorno | objeto ou `null` | objeto ou `null` |
| Ordem | — | respeita `orderBy` |

```ts
// findUnique — só por campo único
await prisma.usuario.findUnique({ where: { id: 1 } });
await prisma.usuario.findUnique({ where: { email: "ana@mail.com" } });

// findFirst — qualquer filtro
await prisma.usuario.findFirst({ where: { idade: { gte: 18 } } });
```

`where: { idade: 18 }` com `findUnique` é erro de tipo — idade não é única.

## Com orderBy — "o primeiro" definido

Sem `orderBy`, "primeiro" é imprevisível:

```ts
// o livro mais antigo
const antigo = await prisma.livro.findFirst({
  orderBy: { anoPublicacao: "asc" },
});

// o mais recente
const recente = await prisma.pedido.findFirst({
  where: { clienteId: 1 },
  orderBy: { criadoEm: "desc" },
});
```

`orderBy` + `findFirst` = "o X mais/menos Y" — MAX/MIN via query.

## OrThrow — quando null é erro

```ts
const usuario = await prisma.usuario.findFirstOrThrow({
  where: { email: "ana@mail.com" },
});
// se não achar → lança P2025 em vez de retornar null
```

```ts
await prisma.usuario.findUniqueOrThrow({ where: { id: 1 } });
```

Em API, `OrThrow` converte "não achou" em exceção — mapeável para `404` no middleware de erro. Ou faça manual:

```ts
const usuario = await prisma.usuario.findUnique({ where: { id } });
if (!usuario) throw new AppError("Usuário não encontrado", 404);
```

## Selecionando campos

```ts
const usuario = await prisma.usuario.findFirst({
  where: { email: "ana@mail.com" },
  select: { id: true, nome: true },   // só esses campos
});
```

## Uso típico em service

```ts
// unicidade de email no cadastro
const existe = await prisma.usuario.findFirst({
  where: { email: dados.email },
  select: { id: true },          // só precisa saber se existe
});
if (existe) throw new AppError("Email já em uso", 409);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `findUnique` com campo não-único | Erro de tipo — use `findFirst` |
| Tratar `null` como objeto | Cheque antes de usar: `if (!usuario)` |
| "Primeiro" sem `orderBy` | Resultado indefinido — sempre ordene |
| P2025 inesperado | `OrThrow` lança se não achar — mapeie para 404 |

## Resumo

- `findFirst` = um registro por qualquer critério; `findUnique` = só por `@id`/`@unique`
- `orderBy` + `findFirst` = "o mais X" (top-1)
- `findFirstOrThrow`/`findUniqueOrThrow` lançam P2025 — caminho natural pro 404
- `select` no find reduz o tráfego quando só um campo importa
