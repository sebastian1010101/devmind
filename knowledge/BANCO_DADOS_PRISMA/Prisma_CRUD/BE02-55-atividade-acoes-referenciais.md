# BE02-55 — Atividade: Ações Referenciais

## Objetivo

Exercitar as três ações na prática — ver o `delete` se comportar diferente conforme a configuração do schema.

## Schema de teste

```prisma
model Blog {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

model Post {
  id        Int        @id @default(autoincrement())
  titulo    String
  blog      Blog       @relation(fields: [blogId], references: [id], onDelete: Cascade)
  blogId    Int        @map("blog_id")
  comentarios Comentario[]
}

model Comentario {
  id      Int   @id @default(autoincrement())
  texto   String
  post    Post? @relation(fields: [postId], references: [id], onDelete: SetNull)
  postId  Int?  @map("post_id")
}

model Tag {
  id    Int   @id @default(autoincrement())
  nome  String
  posts TagPost[]
}

model TagPost {
  post   Post @relation(fields: [postId], references: [id], onDelete: Restrict)
  postId Int  @map("post_id")
  tag    Tag  @relation(fields: [tagId], references: [id])
  tagId  Int  @map("tag_id")

  @@id([postId, tagId])
}
```

## O experimento

```ts
// 1. CASCADE — deletar blog limpa os posts
await prisma.blog.delete({ where: { id: 1 } });
// posts do blog 1 sumiram junto
// comentários dos posts: postId virou NULL (SetNull)

// 2. RESTRICT — post com tag vinculada não deleta
await prisma.post.delete({ where: { id: 2 } });
// P2014: viola FK de tag_posts → bloqueado

// para deletar: desvincule primeiro
await prisma.tagPost.deleteMany({ where: { postId: 2 } });
await prisma.post.delete({ where: { id: 2 } });   // agora funciona
```

## Efeito em cadeia

```text
delete blog (Cascade)
  → posts deletados (Cascade no blog)
    → comentarios.postId = NULL (SetNull no post)
      → tag_posts? bloquearia! Restrict barra a cascata
```

**Atenção**: `Restrict` num nível impede o cascade acima — o delete do blog falha se algum post tiver tag vinculada. Ações referenciais se compõem.

## Comparando as escolhas

| Cenário | Escolha | Resultado |
| --- | --- | --- |
| Post de blog | `Cascade` | Some com o blog |
| Comentário de post | `SetNull` | Sobrevive órfão |
| Tag em post | `Restrict` | Impede delete sem desvincular |

## Critérios de conclusão

1. `Cascade` observado — filhos somem com o pai
1. `SetNull` observado — filhos ficam com FK nula
1. `Restrict` observado — P2014 ao tentar deletar
1. Interação entre ações entendida (Restrict corta a cascata)

## Resumo

- A ação referencial decide o destino dos filhos no delete do pai
- `Cascade` limpa, `SetNull` orfa, `Restrict` protege
- Elas se compõem em cadeia — um `Restrict` no meio bloqueia o cascade de cima
- Escolha consciente por relação — é decisão de domínio, não conveniência
