# BE02-47 — Prisma: Paginação

## Por que paginar

```ts
// ❌ tabela com 1M de usuários → 1M de objetos na memória
await prisma.usuario.findMany();

// ✅ traz uma página
await prisma.usuario.findMany({ take: 20 });
```

## take + skip — offset pagination

```ts
const page = 2;
const pageSize = 20;

const usuarios = await prisma.usuario.findMany({
  skip: (page - 1) * pageSize,   // pula 20
  take: pageSize,                // traz 20
  orderBy: { id: "asc" },        // SEMPRE ordene
});
```

Equivalente a `LIMIT 20 OFFSET 20` — e igual ao SQL, **exige `orderBy`** para ser determinístico.

## Resposta paginada completa

```ts
async function listar(page: number, pageSize: number) {
  const [items, total] = await prisma.$transaction([
    prisma.usuario.findMany({
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { id: "asc" },
    }),
    prisma.usuario.count(),
  ]);

  return {
    data: items,
    meta: {
      page,
      pageSize,
      total,
      totalPages: Math.ceil(total / pageSize),
    },
  };
}
```

`$transaction` com array roda as duas queries juntas — `data` + `meta` é o formato padrão de APIs REST.

## Cursor pagination — o alternativo

Em vez de "pule N", cursor diz "continue a partir do último id visto":

```ts
// primeira página
const page1 = await prisma.usuario.findMany({
  take: 20,
  orderBy: { id: "asc" },
});
const lastId = page1[page1.length - 1].id;

// próxima página — a partir do cursor
const page2 = await prisma.usuario.findMany({
  take: 20,
  skip: 1,                    // pula o próprio cursor
  cursor: { id: lastId },
  orderBy: { id: "asc" },
});
```

| Offset (`skip`/`take`) | Cursor |
| --- | --- |
| "Página 3" direto | "Próxima página" sequencial |
| Simples de implementar | Um pouco mais de código |
| Lento em offsets grandes (lê tudo até pular) | O(1) — vai direto pelo índice |
| Linhas novas deslocam páginas | Estável mesmo com inserts |

Cursor brilha em feeds infinitos; offset em tabelas com "ir para página N".

## Paginação em relações

```ts
const autor = await prisma.autor.findUnique({
  where: { id: 1 },
  include: {
    livros: { take: 10, skip: 0, orderBy: { titulo: "asc" } },
  },
});
```

`take`/`skip` funcionam dentro do `include` — a relação também pagina.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `skip`/`take` sem `orderBy` | Páginas inconsistentes — sempre ordene |
| Esquecer `skip: 1` com cursor | A página repete o item do cursor |
| `count` fora da transação | Race — pode divergir da lista; transacione |
| Offset gigante (`skip: 50000`) | Lento — cursor pagination escala melhor |

## Resumo

- `take` = LIMIT, `skip` = OFFSET — sempre com `orderBy`
- Resposta padrão: `{ data, meta: { page, total, totalPages } }` via `$transaction`
- `cursor` + `skip: 1` pagina por posição — estável e rápido em tabelas grandes
- `include` também aceita `take`/`skip`/`orderBy`
