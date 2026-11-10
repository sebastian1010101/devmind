# BE02-42 — Atividade: Serviços de Inserção de Estudantes

## Objetivo

Criar uma camada de **services** para inserção de estudantes e matrículas — encapsulando a lógica de negócio fora da rota.

## Modelo

```prisma
model Estudante {
  id         Int         @id @default(autoincrement())
  nome       String
  email      String      @unique
  matriculas Matricula[]

  @@map("estudantes")
}

model Curso {
  id         Int         @id @default(autoincrement())
  nome       String      @unique
  matriculas Matricula[]

  @@map("cursos")
}

model Matricula {
  id          Int       @id @default(autoincrement())
  estudante   Estudante @relation(fields: [estudanteId], references: [id])
  estudanteId Int       @map("estudante_id")
  curso       Curso     @relation(fields: [cursoId], references: [id])
  cursoId     Int       @map("curso_id")
  criadoEm    DateTime  @default(now()) @map("criado_em")

  @@unique([estudanteId, cursoId])
  @@map("matriculas")
}
```

## O service de criação

```ts
// services/estudante.service.ts
import { prisma } from "../database/prisma";

interface CreateEstudante {
  nome: string;
  email: string;
  cursoIds?: number[];
}

export async function criarEstudante(dados: CreateEstudante) {
  const existe = await prisma.estudante.findUnique({
    where: { email: dados.email },
  });
  if (existe) throw new Error("Email já cadastrado");

  return prisma.estudante.create({
    data: {
      nome: dados.nome,
      email: dados.email,
      matriculas: dados.cursoIds?.length
        ? { create: dados.cursoIds.map(cursoId => ({ cursoId })) }
        : undefined,
    },
    include: { matriculas: { include: { curso: true } } },
  });
}
```

`matriculas.create` cria as linhas da junção junto — um `create` gera estudante + N matrículas numa transação.

## Service de matrícula avulsa

```ts
export async function matricular(estudanteId: number, cursoId: number) {
  // valida existência dos dois lados antes
  const [estudante, curso] = await Promise.all([
    prisma.estudante.findUnique({ where: { id: estudanteId } }),
    prisma.curso.findUnique({ where: { id: cursoId } }),
  ]);

  if (!estudante) throw new Error("Estudante não encontrado");
  if (!curso) throw new Error("Curso não encontrado");

  return prisma.matricula.create({
    data: { estudanteId, cursoId },
    include: { estudante: true, curso: true },
  });
}
```

Validar antes dá erro semântico ("Curso não encontrado") em vez do `P2003` genérico.

## Na rota

```ts
router.post("/estudantes", async (req, res) => {
  const estudante = await criarEstudante(req.body);
  return res.status(201).json(estudante);
});

router.post("/matriculas", async (req, res) => {
  const matricula = await matricular(req.body.estudanteId, req.body.cursoId);
  return res.status(201).json(matricula);
});
```

## Critérios de conclusão

1. `criarEstudante` com matrículas aninhadas funcionando
1. `matricular` validando os dois lados antes do insert
1. `@@unique` impedindo matrícula duplicada (P2002)
1. Resposta traz as relações via `include`

## Resumo

- Services encapsulam Prisma — a rota só cuida de HTTP
- Nested `create` na junção resolve "criar já matriculado"
- Validar existência antes do `create` dá erros melhores que `P2003` cru
- `@@unique` na junção é a última linha de defesa contra duplicatas
