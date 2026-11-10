# BE02-94 — Atividade: Testes Unitários com Prisma

## Objetivo

Cobrir um service de ponta a ponta com `jest-mock-extended` — todos os métodos, todos os caminhos (sucesso, 404, 409, erro de banco).

## O service

```ts
export class CursoService {
  constructor(private prisma: PrismaClient) {}

  async criar(dados: { titulo: string; instrutorId: number }) {
    const instrutor = await this.prisma.instrutor.findUnique({
      where: { id: dados.instrutorId },
    });
    if (!instrutor) throw new AppError("Instrutor não encontrado", 404);
    return this.prisma.curso.create({ data: dados });
  }

  async buscar(id: number) {
    const curso = await this.prisma.curso.findUnique({
      where: { id },
      include: { aulas: true },
    });
    if (!curso) throw new AppError("Curso não encontrado", 404);
    return curso;
  }

  async listar(ativos = true) {
    return this.prisma.curso.findMany({ where: { ativo: ativos } });
  }
}
```

## A suite

```ts
import { mockDeep, mockReset, DeepMockProxy } from "jest-mock-extended";
import { PrismaClient } from "@prisma/client";
import { CursoService } from "../src/services/curso.service";

describe("CursoService", () => {
  const prismaMock = mockDeep<PrismaClient>();
  const service = new CursoService(prismaMock as unknown as PrismaClient);

  beforeEach(() => mockReset(prismaMock));

  describe("criar", () => {
    it("cria quando instrutor existe", async () => {
      prismaMock.instrutor.findUnique.mockResolvedValue({ id: 1 } as any);
      prismaMock.curso.create.mockResolvedValue({ id: 10, titulo: "SQL" } as any);

      const curso = await service.criar({ titulo: "SQL", instrutorId: 1 });

      expect(curso.id).toBe(10);
      expect(prismaMock.curso.create).toHaveBeenCalledWith({
        data: { titulo: "SQL", instrutorId: 1 },
      });
    });

    it("404 quando instrutor não existe", async () => {
      prismaMock.instrutor.findUnique.mockResolvedValue(null);

      await expect(service.criar({ titulo: "X", instrutorId: 99 }))
        .rejects.toMatchObject({ statusCode: 404 });
      expect(prismaMock.curso.create).not.toHaveBeenCalled();
    });
  });

  describe("buscar", () => {
    it("retorna com aulas", async () => {
      prismaMock.curso.findUnique.mockResolvedValue({
        id: 1, aulas: [{ titulo: "intro" }],
      } as any);

      const curso = await service.buscar(1);

      expect(prismaMock.curso.findUnique).toHaveBeenCalledWith(
        expect.objectContaining({ include: { aulas: true } })
      );
      expect(curso.aulas).toHaveLength(1);
    });

    it("404 quando não existe", async () => {
      prismaMock.curso.findUnique.mockResolvedValue(null);
      await expect(service.buscar(99)).rejects.toMatchObject({ statusCode: 404 });
    });
  });

  describe("listar", () => {
    it("filtra ativos por padrão", async () => {
      prismaMock.curso.findMany.mockResolvedValue([]);

      await service.listar();

      expect(prismaMock.curso.findMany).toHaveBeenCalledWith({
        where: { ativo: true },
      });
    });
  });
});
```

## Cobertura mínima por método

| Método | Caminhos |
| --- | --- |
| `criar` | sucesso, dependência inexistente (404), P2002 |
| `buscar` | achou (com include), não achou (404) |
| `listar` | filtro aplicado corretamente |

## Critérios de conclusão

1. `mockDeep` injetado, `mockReset` por teste
1. Todo método tem sucesso + pelo menos um erro
1. `toHaveBeenCalledWith` valida a query montada
1. `not.toHaveBeenCalled` prova que erro impede efeito

## Resumo

- Um `describe` por método, caminhos separados por `it`
- Mock prova a decisão — qual query, qual erro lançado
- 404s e 409s são as regras de negócio — teste-as
