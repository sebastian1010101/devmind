# BE02-96 — Atividade: Testes de Integração com Prisma

## Objetivo

Suite de integração sobre o service de matrículas — banco de teste real provando constraints e queries de relação.

## Setup

```env
# .env.test
DATABASE_URL="postgresql://postgres:senha@localhost:5432/cursos_test"
```

```bash
npx dotenv -e .env.test -- npx prisma migrate deploy
```

## A suite

```ts
import { prisma } from "../../src/database/prisma";
import { MatriculaService } from "../../src/services/matricula.service";

describe("MatriculaService — integração", () => {
  const service = new MatriculaService(prisma);

  beforeAll(async () => {
    await prisma.$connect();
  });

  beforeEach(async () => {
    await prisma.matricula.deleteMany();
    await prisma.curso.deleteMany();
    await prisma.estudante.deleteMany();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  it("matricula estudante em curso", async () => {
    const estudante = await prisma.estudante.create({
      data: { nome: "Ana", email: "a@a.com" },
    });
    const curso = await prisma.curso.create({
      data: { nome: "SQL" },
    });

    const matricula = await service.matricular(estudante.id, curso.id);

    expect(matricula.id).toBeDefined();

    const noBanco = await prisma.matricula.findUnique({
      where: { estudanteId_cursoId: { estudanteId: estudante.id, cursoId: curso.id } },
    });
    expect(noBanco).not.toBeNull();
  });

  it("@@unique barra matrícula duplicada", async () => {
    const e = await prisma.estudante.create({ data: { nome: "B", email: "b@b.com" } });
    const c = await prisma.curso.create({ data: { nome: "JS" } });

    await service.matricular(e.id, c.id);

    await expect(service.matricular(e.id, c.id))
      .rejects.toMatchObject({ statusCode: 409 });
  });

  it("404 em estudante inexistente", async () => {
    const c = await prisma.curso.create({ data: { nome: "X" } });

    await expect(service.matricular(999, c.id))
      .rejects.toMatchObject({ statusCode: 404 });
  });

  it("include traz curso na matrícula", async () => {
    const e = await prisma.estudante.create({ data: { nome: "C", email: "c@c.com" } });
    const curso = await prisma.curso.create({ data: { nome: "React" } });
    await service.matricular(e.id, curso.id);

    const lista = await service.matriculasDoEstudante(e.id);

    expect(lista[0].curso.nome).toBe("React");
  });

  it("cascade: deletar curso remove matrículas", async () => {
    const e = await prisma.estudante.create({ data: { nome: "D", email: "d@d.com" } });
    const c = await prisma.curso.create({ data: { nome: "TS" } });
    await service.matricular(e.id, c.id);

    await prisma.curso.delete({ where: { id: c.id } });

    const resto = await prisma.matricula.findMany({ where: { cursoId: c.id } });
    expect(resto).toHaveLength(0);
  });
});
```

## O que cada teste prova

| Teste | Prova real |
| --- | --- |
| matricula | FKs ligam de verdade — registro no banco |
| duplicata 409 | `@@unique` existe e o service traduz P2002 |
| 404 | Service valida existência antes do insert |
| include | Query de relação retorna o objeto certo |
| cascade | `onDelete` declarado funciona |

## Critérios de conclusão

1. `.env.test` isolado + `migrate deploy` aplicado
1. `beforeEach` limpa na ordem certa (filhos → pais)
1. Pelo menos um teste por regra de constraint
1. Asserts confirmam no banco (`prisma.find*`), não só o retorno

## Resumo

- Integração com Prisma prova o que mock não pode: constraints reais
- `@@unique`, FK, cascade — todos testáveis contra banco de verdade
- Confirme o efeito no banco com uma query — o retorno pode mentir
