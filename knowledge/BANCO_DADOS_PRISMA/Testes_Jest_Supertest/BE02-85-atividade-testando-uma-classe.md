# BE02-85 — Atividade: Testando uma Classe

## Objetivo

Testar uma classe de service com repositório mockado — cobrindo sucesso, erro e bordas sem tocar banco.

## A classe

```ts
// src/services/tarefa.service.ts
export class TarefaService {
  constructor(private repo: ITarefaRepository) {}

  async criar(dados: { titulo: string; prioridade: string }) {
    if (dados.prioridade && !["alta", "media", "baixa"].includes(dados.prioridade)) {
      throw new Error("Prioridade inválida");
    }
    return this.repo.criar({ ...dados, status: "pendente" });
  }

  async concluir(id: number) {
    const tarefa = await this.repo.buscarPorId(id);
    if (!tarefa) throw new Error("Tarefa não encontrada");
    if (tarefa.status === "concluida") throw new Error("Já concluída");

    return this.repo.atualizar(id, { status: "concluida" });
  }
}
```

## A suite com mock

```ts
import { TarefaService } from "../src/services/tarefa.service";

describe("TarefaService", () => {
  const repoMock = {
    criar: jest.fn(),
    buscarPorId: jest.fn(),
    atualizar: jest.fn(),
  };

  let service: TarefaService;

  beforeEach(() => {
    jest.clearAllMocks();
    service = new TarefaService(repoMock as any);
  });

  describe("criar", () => {
    it("cria com status pendente", async () => {
      repoMock.criar.mockResolvedValue({ id: 1, titulo: "X", status: "pendente" });

      const tarefa = await service.criar({ titulo: "X", prioridade: "alta" });

      expect(tarefa.status).toBe("pendente");
      expect(repoMock.criar).toHaveBeenCalledWith(
        expect.objectContaining({ status: "pendente" })
      );
    });

    it("rejeita prioridade inválida", async () => {
      await expect(service.criar({ titulo: "X", prioridade: "urgente" }))
        .rejects.toThrow("Prioridade inválida");

      expect(repoMock.criar).not.toHaveBeenCalled();
    });
  });

  describe("concluir", () => {
    it("conclui tarefa pendente", async () => {
      repoMock.buscarPorId.mockResolvedValue({ id: 1, status: "pendente" });
      repoMock.atualizar.mockResolvedValue({ id: 1, status: "concluida" });

      const tarefa = await service.concluir(1);
      expect(tarefa.status).toBe("concluida");
    });

    it("404 quando não existe", async () => {
      repoMock.buscarPorId.mockResolvedValue(null);

      await expect(service.concluir(99)).rejects.toThrow("não encontrada");
    });

    it("rejeita já concluída", async () => {
      repoMock.buscarPorId.mockResolvedValue({ id: 1, status: "concluida" });

      await expect(service.concluir(1)).rejects.toThrow("Já concluída");
      expect(repoMock.atualizar).not.toHaveBeenCalled();
    });
  });
});
```

## O que está sendo provado

```text
criar → status default "pendente" / prioridade inválida nunca toca repo
concluir → busca → atualiza / inexistente → erro / já concluída → erro sem update
```

Cada `it` é uma **regra de negócio** — o mock isola o service do Prisma.

## Critérios de conclusão

1. `jest.fn()` mockando os métodos do repo
1. `jest.clearAllMocks()` no `beforeEach` — isolamento
1. Sucesso + erro + borda cobertos por método
1. `not.toHaveBeenCalled()` provando que o erro impede efeitos

## Resumo

- Classe + repo mockado = teste unitário puro
- `mockResolvedValue`/`mockRejectedValue` simulam async
- `not.toHaveBeenCalled` é assert tão importante quanto o retorno
- `beforeEach` recria o service + limpa mocks
