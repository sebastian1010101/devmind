# BE02-99 — Injeção de Dependência em Testes Unitários

## O ganho — DI existe pra isso

```ts
// sem DI: service acoplado — como testar?
class UsuarioService {
  private repo = new PrismaUsuarioRepository();   // travado no real
}

// com DI: injeta o que quiser
class UsuarioService {
  constructor(private repo: IUsuarioRepository) {}
}
```

O construtor recebe a dependência — no teste, entra o mock.

## O padrão

```ts
describe("UsuarioService", () => {
  const repoMock = {
    criar: jest.fn(),
    buscarPorEmail: jest.fn(),
  };

  const service = new UsuarioService(repoMock);   // repo fake via construtor

  it("rejeita duplicado", async () => {
    repoMock.buscarPorEmail.mockResolvedValue({ id: 1 });
    await expect(service.criar({ email: "x@x.com" })).rejects.toThrow();
  });
});
```

Nenhum `jest.mock` de módulo — a dependência simplesmente é outra. DI torna o teste declarativo.

## Com tsyringe — container de teste

```ts
import { container } from "tsyringe";

describe("service via container", () => {
  let testContainer: DependencyContainer;

  beforeEach(() => {
    testContainer = container.createChildContainer();
    testContainer.registerInstance(TOKENS.UsuarioRepository, repoMock);
    testContainer.registerInstance(TOKENS.EmailService, mailerMock);
  });

  it("resolve com mocks", async () => {
    const service = testContainer.resolve(UsuarioService);
    // todas as dependências são mocks — teste unitário puro
  });
});
```

`createChildContainer()` herda registros e permite overrides — o global fica limpo.

## Por que é melhor que jest.mock de módulo

| `jest.mock("../repo")` | DI |
| --- | --- |
| Troca o módulo inteiro | Troca só a peça |
| Mágica de hoisting | Explícito no construtor |
| Difícil variar por teste | `registerInstance` por caso |
| Acoplamento escondido | Dependência declarada |

## Dependências múltiplas

```ts
const service = new PedidoService(
  repoMock,        // pedidos
  estoqueMock,     // estoque
  mailerMock,      // email
  loggerMock,      // logs — mock trivial: { info: jest.fn() }
);
```

Cada peça isolada — o teste verifica **interações**:

```ts
it("venda notifica por email", async () => {
  repoMock.criar.mockResolvedValue({ id: 1 });

  await service.vender(dados);

  expect(mailerMock.enviar).toHaveBeenCalledWith(
    expect.objectContaining({ assunto: expect.stringContaining("confirmado") })
  );
});
```

## Sem DI? Monta manual

```ts
// factories de teste — mesmo efeito, sem container
function makeService(overrides = {}) {
  return new UsuarioService(
    overrides.repo ?? repoMock,
    overrides.mailer ?? mailerMock,
  );
}
```

`makeService` centraliza a montagem — override só do que o teste muda.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `jest.mock` quando DI bastaria | Injete — é mais limpo e tipado |
| Mock incompleto | O service chama métodos que o mock não tem → `undefined is not a function` |
| Container global sujo | `createChildContainer` isola overrides |
| Dependências fixas demais | Teste cada peça por seu contrato, não pelo conjunto |

## Resumo

- DI foi feita para testes — construtor recebe mock, não real
- `jest.mock` de módulo torna-se desnecessário
- `createChildContainer` do tsyringe isola registros de teste
- Testes verificam interações entre peças — `toHaveBeenCalledWith`
