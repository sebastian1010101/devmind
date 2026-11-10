# BE02-34 — Prisma: Relacionamento 1-N

## Modelando

Um autor tem muitos livros; cada livro tem um autor:

```prisma
model Autor {
  id     Int     @id @default(autoincrement())
  nome   String
  livros Livro[]          // ← lista: o lado "muitos"

  @@map("autores")
}

model Livro {
  id      Int   @id @default(autoincrement())
  titulo  String
  autor   Autor @relation(fields: [autorId], references: [id])
  autorId Int   @map("autor_id")

  @@map("livros")
}
```

## Diferença do 1-1

```text
1-1:  FK com @unique          → perfil Perfil?
1-N:  FK sem @unique          → livros Livro[]
```

- Lado N (`livros`): array `Livro[]` — sem FK própria
- Lado 1 (`livro`): FK `autorId` **sem** `@unique` — pode repetir
- `Livro[]` não é coluna — é a lista de filhos que o `include` carrega

## Criando — aninhado ou pela FK

```ts
// cria autor + livros junto
const autor = await prisma.autor.create({
  data: {
    nome: "Machado de Assis",
    livros: {
      create: [
        { titulo: "Dom Casmurro" },
        { titulo: "Brás Cubas" },
      ],
    },
  },
  include: { livros: true },
});

// adiciona livro a autor existente
await prisma.livro.create({
  data: { titulo: "Quincas Borba", autorId: autor.id },
});
```

## Lendo

```ts
// autor com seus livros
const autor = await prisma.autor.findUnique({
  where: { id: 1 },
  include: { livros: true },
});
// autor.livros → Livro[]

// livros com o autor
const livros = await prisma.livro.findMany({
  include: { autor: true },
});

// filtrando filhos no include
const autor2 = await prisma.autor.findUnique({
  where: { id: 1 },
  include: {
    livros: {
      where: { anoPublicacao: { lt: 1900 } },
      orderBy: { titulo: "asc" },
    },
  },
});
```

## Contando filhos — _count

```ts
const autores = await prisma.autor.findMany({
  include: {
    _count: { select: { livros: true } },
  },
});
// autores[0]._count.livros → 2
```

`_count` evita carregar os objetos quando só o número interessa.

## Relação opcional

```prisma
model Livro {
  autor   Autor? @relation(fields: [autorId], references: [id])
  autorId Int?   @map("autor_id")
}
```

`Autor?` + `Int?` = livro pode existir sem autor. Remova os `?` para exigir.

## Ações referenciais no schema

```prisma
autor Autor @relation(fields: [autorId], references: [id], onDelete: Cascade)
```

| `onDelete` | Ao deletar o autor... |
| --- | --- |
| `Restrict` (padrão) | Erro se houver livros |
| `Cascade` | Deleta os livros junto |
| `SetNull` | `autorId` vira NULL (precisa ser `Int?`) |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `@unique` na FK do lado N | Remove — isso transformaria em 1-1 |
| `livros` veio `undefined` | Relações precisam de `include` ou `select` |
| Deletar pai com filhos | Defina `onDelete` na relação — ou delete filhos antes |
| `Int` FK com `SetNull` | FK precisa ser `Int?` para receber NULL |

## Resumo

- 1-N no Prisma: lista `[]` no lado 1, `@relation` + FK no lado N — sem `@unique`
- `include: { livros: true }` carrega filhos; `include` aceita `where`/`orderBy`
- `_count: { select: { livros: true } }` conta sem carregar
- `onDelete: Cascade/SetNull` na `@relation` define o destino dos filhos
