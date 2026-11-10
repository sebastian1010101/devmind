# BE02-83 — Jest: Hooks de Teste

## Os quatro hooks

```ts
describe("suite", () => {
  beforeAll(() => { /* 1x antes de TODOS os testes */ });
  afterAll(() => { /* 1x depois de todos */ });
  beforeEach(() => { /* antes de CADA teste */ });
  afterEach(() => { /* depois de cada teste */ });
});
```

```text
beforeAll
 ├─ beforeEach → it(1) → afterEach
 ├─ beforeEach → it(2) → afterEach
 └─ beforeEach → it(3) → afterEach
afterAll
```

## Quando usar cada

| Hook | Uso típico |
| --- | --- |
| `beforeAll` | Conectar banco de teste, subir app — custoso, uma vez |
| `afterAll` | `$disconnect`, fechar conexão |
| `beforeEach` | Resetar dados, criar fixtures frescas — isolamento |
| `afterEach` | Limpar mocks (`jest.clearAllMocks`), deletar dados |

## Exemplo — com banco

```ts
describe("UsuarioService", () => {
  beforeAll(async () => {
    await prisma.$connect();
  });

  beforeEach(async () => {
    await prisma.usuario.deleteMany();   // tabela limpa a cada teste
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  it("cria usuário", async () => { ... });
  it("rejeita duplicado", async () => { ... });  // banco limpo — sem interferência
});
```

## Isolamento — por que beforeEach limpa

```ts
// ❌ sem limpeza: teste 2 depende do que teste 1 deixou
it("lista usuários", async () => {
  const todos = await prisma.usuario.findMany();
  expect(todos).toHaveLength(0);   // falha se outro teste inseriu
});

// ✅ estado conhecido por teste
beforeEach(async () => {
  await prisma.usuario.deleteMany();
});
```

## Ordem de execução aninhada

```ts
describe("externo", () => {
  beforeAll(() => console.log("outer beforeAll"));
  beforeEach(() => console.log("outer beforeEach"));

  describe("interno", () => {
    beforeEach(() => console.log("inner beforeEach"));

    it("teste", () => {});
    // ordem: outer beforeAll → outer beforeEach → inner beforeEach → it
  });
});
```

Hooks externos rodam **antes** dos internos.

## Escopo de variáveis

```ts
describe("suite", () => {
  let usuario: Usuario;

  beforeEach(async () => {
    usuario = await prisma.usuario.create({ data: fixture });   // fresco
  });

  it("usa o usuario", async () => {
    expect(usuario.email).toBe(...);   // criado no beforeEach
  });
});
```

`let` declarado no describe + atribuído no hook — o padrão de fixture.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Estado vazando entre testes | `beforeEach` reseta — não confie na ordem |
| `afterEach` limpando cedo | afterEach roda pós-teste — para mocks use `clearMocks: true` |
| `beforeAll` com fixture mutável | Cada teste pode alterá-la — `beforeEach` para dados frescos |
| Esquecer `$disconnect` | Processo Jest não encerra — `afterAll` |

## Resumo

- `All` = uma vez por suite; `Each` = por teste
- `beforeEach` garante isolamento — cada teste com estado conhecido
- `afterAll` fecha conexões — sem isso o Jest pendura
- Hooks externos rodam antes dos internos no aninhamento
