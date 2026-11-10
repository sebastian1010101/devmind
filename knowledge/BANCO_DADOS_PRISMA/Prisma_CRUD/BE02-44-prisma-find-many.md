# BE02-44 — Prisma: Find Many

## O básico

```ts
const usuarios = await prisma.usuario.findMany();
// → Usuario[] — todos os registros
```

## where — filtros

```ts
await prisma.usuario.findMany({
  where: { ativo: true },
});

await prisma.usuario.findMany({
  where: {
    idade: { gte: 18, lt: 65 },
    cidade: { in: ["SP", "RJ"] },
  },
});
```

### Operadores do where

| Operador | Equivale a |
| --- | --- |
| `equals` | `=` |
| `not` | `!=` |
| `gt`, `gte`, `lt`, `lte` | `>`, `>=`, `<`, `<=` |
| `in`, `notIn` | `IN (...)` |
| `contains` | `LIKE '%x%'` |
| `startsWith`, `endsWith` | `LIKE 'x%'`, `LIKE '%x'` |
| `mode: "insensitive"` | `ILIKE` — ignora case |

```ts
where: { nome: { contains: "silva", mode: "insensitive" } }
```

## Lógica — AND, OR, NOT

```ts
await prisma.usuario.findMany({
  where: {
    OR: [
      { cidade: "SP" },
      { cidade: "RJ" },
    ],
    NOT: { ativo: false },
  },
});
```

Campos no mesmo objeto já são `AND` implícito — `{ ativo: true, idade: { gte: 18 } }`.

## orderBy

```ts
await prisma.usuario.findMany({
  orderBy: { criadoEm: "desc" },
});

// múltiplos critérios
await prisma.usuario.findMany({
  orderBy: [{ idade: "desc" }, { nome: "asc" }],
});
```

## NULL no where

```ts
where: { telefone: null }          -- IS NULL
where: { telefone: { not: null } } -- IS NOT NULL
```

## Campos de relação no where

```ts
// livros cujo autor se chama Machado
await prisma.livro.findMany({
  where: { autor: { nome: { contains: "Machado" } } },
});

// autores que TÊM livros
await prisma.autor.findMany({
  where: { livros: { some: {} } },
});

// autores SEM livros
await prisma.autor.findMany({
  where: { livros: { none: {} } },
});

// autores com TODOS os livros antes de 1900
await prisma.autor.findMany({
  where: { livros: { every: { anoPublicacao: { lt: 1900 } } } },
});
```

| Operador de relação | Significa |
| --- | --- |
| `some` | Existe filho que casa (EXISTS) |
| `every` | Todos os filhos casam |
| `none` | Nenhum filho casa |
| `is` | No lado 1/1-1 — filtra o objeto |

## select vs include

```ts
select: { id: true, nome: true }                    // whitelist de campos
include: { livros: true }                           // traz relações
```

Valem para `findMany` igual — detalhes na próxima aula.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `equals` escrito direto | `{ nome: "Ana" }` é shorthand — `equals` opcional |
| `contains` sem `mode` | Case-sensitive; `mode: "insensitive"` para `ILIKE` |
| Filtrar relação com campo plano | `where: { autor: { nome: ... } }` — objeto aninhado |
| `findMany` sem `take` em tabela grande | Sempre considere paginação — `take`/`skip` |

## Resumo

- `findMany({ where, orderBy })` = SELECT com filtro e ordenação
- `contains`/`in`/`gte`/`mode: insensitive` cobrem os filtros comuns
- `some`/`every`/`none`/`is` filtram por relações — EXISTS/EACH/NONE
- Campos juntos são AND implícito; `OR`/`NOT` para o resto
