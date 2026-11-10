# BE02-36 — Prisma: Relacionamento N-N

## As duas formas

```text
implícita:  o Prisma cria a tabela intermediária sozinho
explícita:  você modela a tabela junção (quando ela tem dados próprios)
```

## N-N implícito

```prisma
model Estudante {
  id     Int     @id @default(autoincrement())
  nome   String
  cursos Curso[]          // só a lista — sem junção visível

  @@map("estudantes")
}

model Curso {
  id         Int         @id @default(autoincrement())
  titulo     String
  estudantes Estudante[]

  @@map("cursos")
}
```

O `migrate` cria sozinho:

```sql
CREATE TABLE "_CursoToEstudante" (
  "A" INTEGER NOT NULL REFERENCES cursos(id),
  "B" INTEGER NOT NULL REFERENCES estudantes(id)
);
```

Prático, mas a tabela é invisível no schema — e **não pode ter atributos próprios** (nota, data, posição).

## N-N explícito — a junção como model

Quando a relação tem dados, modele-a:

```prisma
model Matricula {
  id           Int       @id @default(autoincrement())
  estudante    Estudante @relation(fields: [estudanteId], references: [id])
  estudanteId  Int       @map("estudante_id")
  curso        Curso     @relation(fields: [cursoId], references: [id])
  cursoId      Int       @map("curso_id")
  dataMatricula DateTime @default(now()) @map("data_matricula")
  nota         Decimal?

  @@unique([estudanteId, cursoId])   // impede matrícula dupla
  @@map("matriculas")
}
```

```text
Estudante ──1:N── Matricula ──N:1── Curso
```

O N-N explícito é literalmente **dois 1-N** com a junção no meio.

## Implícito — connect/disconnect

```ts
// matricular estudante 1 nos cursos 2 e 3
await prisma.estudante.update({
  where: { id: 1 },
  data: { cursos: { connect: [{ id: 2 }, { id: 3 }] } },
});

// desmatricular
await prisma.estudante.update({
  where: { id: 1 },
  data: { cursos: { disconnect: { id: 2 } } },
});

// criar com relação já ligada
await prisma.curso.create({
  data: { titulo: "SQL", estudantes: { connect: { id: 1 } } },
});
```

## Explícito — create na junção

```ts
await prisma.matricula.create({
  data: {
    estudanteId: 1,
    cursoId: 2,
    nota: 9.5,
  },
});

// consulta atravessando a junção
const cursos = await prisma.matricula.findMany({
  where: { estudanteId: 1 },
  include: { curso: true },
});
// cursos.map(m => m.curso.titulo)
```

## Lendo os dois lados

```ts
// implícito: direto
const cursos = await prisma.curso.findMany({
  include: { estudantes: true },   // Estudante[] direto
});

// explícito: pela junção
const curso = await prisma.curso.findUnique({
  where: { id: 1 },
  include: {
    matriculas: { include: { estudante: true } },
  },
});
// curso.matriculas[].estudante — passa pela junção
```

## Qual escolher

| Implícito | Explícito |
| --- | --- |
| Ligação pura, sem atributos | Relação com dados (nota, data, papel) |
| Schema mais limpo | Controle total (nome, constraints) |
| Sem acesso direto à junção | Pode virar entidade rica depois |

Dúvida? A maioria dos N-N do mundo real **ganha atributos cedo ou tarde** — explícito é o caminho seguro.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Precisou de campo na relação com N-N implícito | Migre para junção explícita |
| `@@unique` esquecida na explícita | Pares duplicados — adicione `@@unique([a, b])` |
| `connect` com id inexistente | P2025 — o registro precisa existir |
| Esperar `estudantes` direto na explícita | Na explícita se consulta pela junção — `include` aninhado |

## Resumo

- Implícito: `Curso[] ↔ Estudante[]` — Prisma cria a junção; só para ligação pura
- Explícito: model da junção com 2 `@relation` + `@@unique` — quando a relação tem atributos
- `connect`/`disconnect` gerenciam vínculos no implícito; na explícita é `create`/`delete` na junção
- Consulta explícita atravessa: `curso → matriculas → estudante`
