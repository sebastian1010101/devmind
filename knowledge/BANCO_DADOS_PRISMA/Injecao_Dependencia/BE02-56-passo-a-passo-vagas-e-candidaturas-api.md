# BE02-56 — Passo a Passo: Vagas e Candidaturas API

## O que é

Aula de revisão integrada — construir uma API completa juntando Express + Prisma: **vagas de emprego** e **candidaturas** (N-N com dados próprios).

## Modelo de domínio

```text
Candidato >───< Vaga   via   Candidatura
                          (aplicou_em, status)
```

Candidatura = junção explícita — tem atributos próprios (`status`, `criadoEm`).

## Schema

```prisma
model Candidato {
  id           Int           @id @default(autoincrement())
  nome         String
  email        String        @unique
  candidaturas Candidatura[]

  @@map("candidatos")
}

model Vaga {
  id           Int           @id @default(autoincrement())
  titulo       String
  empresa      String
  descricao    String?
  candidaturas Candidatura[]

  @@map("vagas")
}

model Candidatura {
  id          Int       @id @default(autoincrement())
  candidato   Candidato @relation(fields: [candidatoId], references: [id], onDelete: Cascade)
  candidatoId Int       @map("candidato_id")
  vaga        Vaga      @relation(fields: [vagaId], references: [id], onDelete: Cascade)
  vagaId      Int       @map("vaga_id")
  status      String    @default("pendente")
  criadoEm    DateTime  @default(now()) @map("criado_em")

  @@unique([candidatoId, vagaId])
  @@map("candidaturas")
}
```

`@@unique([candidatoId, vagaId])` — candidato não se candidata 2x na mesma vaga.

## Estrutura de camadas

```text
src/
├─ database/prisma.ts        ← singleton do client
├─ routes/                   ← só HTTP (req → res)
├─ services/                 ← regras de negócio + Prisma
├─ controllers/              ← opcional: ponte rota↔service
└─ app.ts / server.ts
```

```ts
// services/vaga.service.ts
export async function criarVaga(dados: { titulo: string; empresa: string }) {
  return prisma.vaga.create({ data: dados });
}

export async function candidatar(candidatoId: number, vagaId: number) {
  const [candidato, vaga] = await Promise.all([
    prisma.candidato.findUnique({ where: { id: candidatoId } }),
    prisma.vaga.findUnique({ where: { id: vagaId } }),
  ]);
  if (!candidato || !vaga) throw new AppError("Recurso não encontrado", 404);

  const existe = await prisma.candidatura.findUnique({
    where: { candidatoId_vagaId: { candidatoId, vagaId } },
  });
  if (existe) throw new AppError("Já candidatado", 409);

  return prisma.candidatura.create({ data: { candidatoId, vagaId } });
}
```

## Rotas resultantes

```text
POST   /vagas                    → criar vaga
GET    /vagas                    → listar com _count de candidaturas
POST   /candidatos               → cadastrar
POST   /vagas/:id/candidaturas   → candidatar-se (N-N explícito)
GET    /vagas/:id/candidaturas   → candidatos da vaga (include aninhado)
PATCH  /candidaturas/:id         → mudar status (pendente → entrevista)
DELETE /candidatos/:id           → cascade apaga candidaturas
```

```ts
// GET /vagas/:id/candidaturas — atravessando a junção
const vaga = await prisma.vaga.findUnique({
  where: { id },
  include: {
    candidaturas: { include: { candidato: { select: { nome: true, email: true } } } },
  },
});
```

## O que a aula consolida

1. N-N explícito com atributos (`status`, `criadoEm`)
1. `@@unique` composta impedindo duplicata — P2002 tratável
1. Validação dos dois lados antes do insert na junção
1. `include` multinível para relatórios
1. `onDelete: Cascade` simplificando o delete

## Resumo

- API Vagas+Candidaturas = N-N explícito clássico com dados na relação
- Service valida os dois lados → 404 semântico antes do P2003
- `@@unique` + `findUnique` por chave composta → 409 de duplicata
- `include` aninhado resolve "quem se candidatou a esta vaga"
