# BE02-33 — Prisma: Relacionamento 1-1

## Modelando no schema

Um usuário tem um perfil; um perfil pertence a um usuário:

```prisma
model Usuario {
  id     Int     @id @default(autoincrement())
  nome   String
  email  String  @unique
  perfil Perfil?

  @@map("usuarios")
}

model Perfil {
  id        Int     @id @default(autoincrement())
  bio       String?
  avatarUrl String? @map("avatar_url")
  usuario   Usuario @relation(fields: [usuarioId], references: [id])
  usuarioId Int     @unique @map("usuario_id")

  @@map("perfis")
}
```

## As três peças de uma relação

```prisma
perfil    Perfil?                                     // campo de relação (lado A)
usuario   Usuario @relation(fields: [usuarioId], references: [id])  // (lado B)
usuarioId Int     @unique                             // a FK real
```

- **Campo de relação** (`perfil`, `usuario`) — não vira coluna; é o acesso `include`
- **FK** (`usuarioId`) — coluna real no banco
- **`@unique` na FK** — é isso que faz ser 1-1 e não 1-N

```sql
-- o SQL gerado:
usuario_id INTEGER NOT NULL UNIQUE REFERENCES usuarios(id)
```

## Qual lado fica com a FK?

Como no SQL puro: a FK vai no lado **dependente** — `Perfil` não existe sem `Usuario`.

No Prisma, o lado com `fields: [...]` é quem ganha a coluna FK. O outro lado declara só o campo de relação (`perfil Perfil?`).

## Criando com relação — nested write

```ts
const usuario = await prisma.usuario.create({
  data: {
    nome: "Ana",
    email: "ana@mail.com",
    perfil: {
      create: { bio: "dev backend" },   // cria o perfil junto
    },
  },
  include: { perfil: true },            // traz o perfil na resposta
});
```

Alternativa — conectar a um existente:

```ts
await prisma.perfil.create({
  data: { bio: "nova", usuario: { connect: { id: 1 } } },
});
// ou pela FK direta:
await prisma.perfil.create({
  data: { bio: "nova", usuarioId: 1 },
});
```

## Lendo a relação

```ts
const usuario = await prisma.usuario.findUnique({
  where: { id: 1 },
  include: { perfil: true },
});
// usuario.perfil → objeto ou null
```

Sem `include`, `usuario.perfil` **não existe** no resultado — relações não vêm por padrão.

## 1-1 opcional vs obrigatório

```prisma
perfil    Perfil?      // usuário PODE não ter perfil

// no Perfil:
usuario   Usuario      // perfil OBRIGATORIAMENTE tem usuário
usuarioId Int @unique  // sem ? — NOT NULL
```

`?` no campo de relação = relação opcional; `?` na FK = NULL permitido.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Faltou `@unique` na FK | Vira 1-N — Prisma exige para 1-1 |
| `perfil` não vem no resultado | Adicione `include: { perfil: true }` |
| `relation ... is missing` | Falta um dos lados — ambos declaram o campo de relação |
| `fields`/`references` invertidos | `fields` = coluna local (FK), `references` = coluna do outro lado |
| Optional na FK errada | `usuarioId Int?` permite perfil órfão — pense se faz sentido |

## Resumo

- 1-1 no Prisma = `@relation(fields, references)` + `@unique` na FK
- Campo de relação não é coluna — é acesso; a FK (`usuarioId`) é a coluna real
- `create` aninhado cria os dois de uma vez; `connect` liga existente
- `include: { perfil: true }` traz a relação — sem ele não vem
