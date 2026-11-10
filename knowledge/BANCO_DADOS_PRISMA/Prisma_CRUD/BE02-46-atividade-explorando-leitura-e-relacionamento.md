# BE02-46 — Atividade: Explorando Leitura e Relacionamento

## Objetivo

Praticar `findMany`/`findFirst` com filtros, ordenação e `include`/`select` sobre relações — respondendo perguntas reais sobre os dados.

## Cenário — livraria

```prisma
model Autor {
  id     Int     @id @default(autoincrement())
  nome   String
  livros Livro[]
}

model Livro {
  id       Int     @id @default(autoincrement())
  titulo   String
  preco    Decimal
  ano      Int     @map("ano_publicacao")
  autor    Autor   @relation(fields: [autorId], references: [id])
  autorId  Int     @map("autor_id")
}
```

## Consultas para implementar

```ts
// 1. livros abaixo de R$ 50, ordenados por preço
await prisma.livro.findMany({
  where: { preco: { lt: 50 } },
  orderBy: { preco: "asc" },
});

// 2. livros com "mar" no título (case-insensitive)
await prisma.livro.findMany({
  where: { titulo: { contains: "mar", mode: "insensitive" } },
});

// 3. autor com todos os livros
await prisma.autor.findUnique({
  where: { id: 1 },
  include: { livros: true },
});

// 4. autores SEM livros
await prisma.autor.findMany({
  where: { livros: { none: {} } },
});

// 5. livros com nome do autor (só campos necessários)
await prisma.livro.findMany({
  select: {
    titulo: true,
    autor: { select: { nome: true } },
  },
});

// 6. autor que mais tem livros
await prisma.autor.findMany({
  include: { _count: { select: { livros: true } } },
  orderBy: { livros: { _count: "desc" } },
  take: 1,
});
```

## Ordenando por campo de relação

```ts
// livros por nome do autor
await prisma.livro.findMany({
  orderBy: { autor: { nome: "asc" } },
});
```

O `orderBy` também navega relações — `autor.nome` ordena pela tabela relacionada.

## Filtro por relação + projeção

```ts
// livros do Machado, só título e ano
await prisma.livro.findMany({
  where: { autor: { nome: { contains: "Machado" } } },
  select: { titulo: true, ano: true },
});
```

## Agregação com Prisma

```ts
// ticket médio dos livros
await prisma.livro.aggregate({
  _avg: { preco: true },
  _max: { preco: true },
  _min: { preco: true },
});

// agrupando por autor
await prisma.livro.groupBy({
  by: ["autorId"],
  _count: { id: true },
  _avg: { preco: true },
});
```

## Critérios de conclusão

1. Filtros com operadores (`lt`, `contains`, `in`) funcionando
1. `include` e `select` retornando estruturas aninhadas
1. `none`/`some` aplicados corretamente
1. `orderBy` por campo de relação e por `_count`

## Resumo

- `where` + `orderBy` + `select`/`include` respondem quase toda pergunta de leitura
- Filtros e ordenação atravessam relações: `where: { autor: {...} }`
- `aggregate`/`groupBy` cobrem o que `GROUP BY` faria em SQL
