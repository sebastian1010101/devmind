# BE02-98 — Introdução a Testes Avançados

## Além do happy path + erro básico

```text
Básico:    funciona? dá erro quando deve?
Avançado:  resiste a bordas, concorrência, estado inconsistente?
```

## Conceitos que sobem o nível

### Testes parametrizados — `it.each`

```ts
it.each([
  ["", "vazio"],
  ["abc", "sem @"],
  ["a@", "sem domínio"],
])("rejeita email %s (%s)", async (email, _) => {
  await expect(service.validar(email)).rejects.toThrow();
});
```

Um `it` vira N casos — bordas tabulares sem repetir código.

### Cobertura — `--coverage`

```bash
npx jest --coverage
```

```text
File            | % Stmts | % Branch | % Funcs | % Lines
service.ts      |    92   |    78    |   100   |   91
```

`% Branch` é o que importa — cobre os `if`s? Coverage alto ≠ testes bons, mas coverage baixo = buraco garantido.

### Fakes vs stubs vs mocks

| Tipo | O que é |
| --- | --- |
| **Stub** | Retorna o que você mandou |
| **Mock** | Stub + verifica chamadas (`toHaveBeenCalled`) |
| **Fake** | Implementação real simplificada (repo em memória) |
| **Spy** | `jest.spyOn` — embrulha função real, observa chamadas |

```ts
const fakeRepo = {
  dados: [],
  async criar(x) { this.dados.push(x); return x; },   // fake em memória
};
```

### Contract tests

Mock e implementação real podem divergir — um teste de contrato valida que o fake obedece a interface do real:

```ts
// a mesma suite roda contra PrismaUsuarioRepository E FakeUsuarioRepository
describe.each([prismaRepo, fakeRepo])("IUsuarioRepository", (repo) => {
  it("cria e acha", async () => { ... });
});
```

Se o fake diverge do real, o teste pega.

### Testes de concorrência

```ts
it("estoque não vai negativo com vendas paralelas", async () => {
  await prisma.$transaction([
    service.vender(id, 1),
    service.vender(id, 1),   // estoque = 1
  ]);
});
```

Race conditions só aparecem com execução paralela — difícil, mas existe.

### Snapshot testing

```ts
expect(res.body).toMatchSnapshot();
```

Útil para shapes grandes estáveis; frágil se a resposta muda muito.

## Quando vale o avanço

| Ferramenta | Vale quando |
| --- | --- |
| `it.each` | Muitas entradas, mesma regra |
| Coverage | Auditar o que falta — não perseguir 100% |
| Contract test | Repositories swap (Prisma↔fake) |
| Spy | Observar sem trocar |
| Snapshot | Output estável e grande |

## Erros comuns

| Erro | Correção |
| --- | --- |
| Coverage como meta | 100% não prova qualidade — prova execução |
| Mock que mente | Fake em memória é mais fiel que mock solto |
| Snapshot cego | Mudou a resposta, aceita o snapshot sem olhar — perigo |
| Teste avançado sem base | Pirâmide primeiro — unitário+integração antes |

## Resumo

- `it.each` parametriza bordas; `--coverage` audita
- Stub/mock/fake/spy são níveis diferentes de substituição
- Contract tests alinham fake e real; snapshots servem saídas estáveis
- Avançado vem depois da base — sem unitário+integração não há o que avançar
