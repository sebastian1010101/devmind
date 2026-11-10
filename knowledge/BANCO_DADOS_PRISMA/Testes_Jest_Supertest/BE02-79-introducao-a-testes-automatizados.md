# BE02-79 — Introdução a Testes Automatizados

## Por que testar

```text
Teste manual:  você clica/curi → verifica → esquece → quebra em prod
Teste autom.:  código roda → verifica → roda em todo commit → pega regressão
```

Testes são código que **prova** que seu código faz o que deveria — e continua fazendo depois de cada mudança.

## A pirâmide de testes

```text
        ╱ E2E ╲          ← poucos, lentos, caros
       ╱───────╲
      ╱ Integração ╲     ← alguns — rota + service + banco
     ╱─────────────╲
    ╱   Unitários    ╲   ← muitos, rápidos, isolados
   ╱─────────────────╲
```

| Tipo | Testa | Exemplo |
| --- | --- | --- |
| **Unitário** | Uma unidade isolada | `service.criar()` com repo mockado |
| **Integração** | Peças juntas | `POST /usuarios` → resposta + banco |
| **E2E** | Fluxo completo | Browser real fazendo login |

## Anatomia de um teste

```ts
describe("UsuarioService", () => {          // agrupa
  it("cria um usuário com email válido", async () => {   // um caso
    // Arrange — prepara
    const dados = { nome: "Ana", email: "a@a.com" };

    // Act — executa
    const usuario = await service.criar(dados);

    // Assert — verifica
    expect(usuario.id).toBeDefined();
    expect(usuario.email).toBe("a@a.com");
  });
});
```

AAA: **Arrange, Act, Assert** — prepara, executa, verifica.

## O que testar

| Teste | Não teste |
| --- | --- |
| Regra de negócio | Framework (Express funciona) |
| Casos de erro | Biblioteca (Prisma funciona) |
| Bordas (vazio, limite, null) | Código trivial |
| Status codes da API | Detalhes de implementação |

## As ferramentas do módulo

| Ferramenta | Para |
| --- | --- |
| **Jest** | Runner + assertions + mocks — unitário e integração |
| **Supertest** | Requests HTTP no app Express — integração |
| **jest-mock-extended** | Mock tipado do Prisma Client |

## Teste bom

- **Independente** — não depende de outro teste nem de ordem
- **Determinístico** — roda 100x, mesmo resultado
- **Rápido** — unitários em ms
- **Um comportamento** por teste — falhou, sabe-se o quê
- **Nome descritivo** — `it("rejeita email duplicado com 409")`

## TDD — opcional mas útil

```text
Red   → escreve teste que falha
Green → implementa o mínimo pra passar
Refactor → limpa mantendo verde
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Testar implementação, não comportamento | Teste entrada→saída, não "chamou a função X interna" |
| Testes que dependem de ordem | Cada teste monta seu próprio estado |
| Sem teste de erro | O caminho triste é onde mora o bug |
| Suite lenta desestimulando | Unitários mockam banco — integração usa banco de teste |

## Resumo

- Teste automatizado prova comportamento e pega regressão
- Pirâmide: muitos unitários, alguns de integração, poucos E2E
- Arrange/Act/Assert; um comportamento por teste
- Jest roda, Supertest faz HTTP, mocks isolam o banco
