# BE02-37 — Atividade: Relacionamentos N-N com Prisma

## Objetivo

Implementar N-N das duas formas: implícita (ligações simples) e explícita (relação com dados próprios).

## Modelo — músicas e playlists

```prisma
model Artista {
  id      Int      @id @default(autoincrement())
  nome    String
  musicas Musica[]

  @@map("artistas")
}

model Musica {
  id        Int              @id @default(autoincrement())
  titulo    String
  artista   Artista          @relation(fields: [artistaId], references: [id])
  artistaId Int              @map("artista_id")
  playlists PlaylistMusica[]

  @@map("musicas")
}

model Playlist {
  id      Int              @id @default(autoincrement())
  nome    String
  musicas PlaylistMusica[]

  @@map("playlists")
}

model PlaylistMusica {
  id         Int      @id @default(autoincrement())
  playlist   Playlist @relation(fields: [playlistId], references: [id])
  playlistId Int      @map("playlist_id")
  musica     Musica   @relation(fields: [musicaId], references: [id])
  musicaId   Int      @map("musica_id")
  posicao    Int

  @@unique([playlistId, musicaId])
  @@map("playlist_musicas")
}
```

Aqui é **explícito**: `PlaylistMusica` existe porque `posicao` é atributo da relação — música #3 na playlist A e #1 na B.

```bash
npx prisma migrate dev --name playlists_n_n
```

## Populando

```ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const artista = await prisma.artista.create({
    data: {
      nome: "Djavan",
      musicas: { create: [{ titulo: "Oceano" }, { titulo: "Flor de Lis" }] },
    },
    include: { musicas: true },
  });

  const playlist = await prisma.playlist.create({
    data: { nome: "MPB" },
  });

  // adicionando na ordem
  await prisma.playlistMusica.create({
    data: { playlistId: playlist.id, musicaId: artista.musicas[0].id, posicao: 1 },
  });
  await prisma.playlistMusica.create({
    data: { playlistId: playlist.id, musicaId: artista.musicas[1].id, posicao: 2 },
  });
}

main().finally(() => prisma.$disconnect());
```

## Consultas

```ts
// músicas da playlist em ordem
const faixas = await prisma.playlistMusica.findMany({
  where: { playlistId: playlist.id },
  include: { musica: { include: { artista: true } } },
  orderBy: { posicao: "asc" },
});
console.log(faixas.map(f => `${f.posicao}. ${f.musica.titulo} - ${f.musica.artista.nome}`));

// playlists que contêm uma música
const emQuais = await prisma.playlistMusica.findMany({
  where: { musica: { titulo: "Oceano" } },
  include: { playlist: true },
});
```

## Validando

```ts
// deve falhar: mesma música 2x na playlist
await prisma.playlistMusica.create({
  data: { playlistId: 1, musicaId: 1, posicao: 3 },
});
// P2002: viola @@unique([playlistId, musicaId])
```

## Versão implícita — comparação

Se `posicao` não fosse necessária:

```prisma
model Playlist {
  id      Int      @id @default(autoincrement())
  nome    String
  musicas Musica[]          // N-N implícito
}
```

```ts
await prisma.playlist.update({
  where: { id: 1 },
  data: { musicas: { connect: [{ id: 1 }, { id: 2 }] } },
});
```

## Critérios de conclusão

1. Junção explícita com `@@unique` e atributo `posicao`
1. Create via junção ligando música a playlist
1. Query de 3 níveis: playlist → junção → música → artista
1. P2002 observado ao duplicar par

## Resumo

- N-N explícito no Prisma = model intermediário + `@@unique([a, b])`
- Atributos da relação (`posicao`) moram na junção
- Queries atravessam a junção com `include` aninhado
- Compare com o implícito para saber quando cada um basta
