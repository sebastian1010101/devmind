# BE02-84 — Jest: Object Mock

## Por que mockar

```ts
// service depende de repository (que vai ao banco)
// teste unitário: isola o service — repo vira mock
```

```text
sem mock:  service → repo → banco    (teste de integração)
com mock:  service → repo fake       (teste unitário — sem banco)
```

O mock substitui a dependência por uma **função controlada** — você decide o que ela retorna e verifica como foi chamada.

## jest.fn — a peça básica

```ts
const buscar = jest.fn();

buscar.mockReturnValue(42);            // retorna sempre 42
buscar(1); buscar(2);

buscar.mock.calls.length               // → 2 (vezes chamada)
buscar.mock.calls[0]                   // → [1] (args da 1ª chamada)
```

## Mock de objeto

```ts
const repoMock = {
  criar: jest.fn().mockResolvedValue({ id: 1, nome: "Ana" }),
  buscarPorEmail: jest.fn().mockResolvedValue(null),
};

const service = new UsuarioService(repoMock);   // injeta o mock
const usuario = await service.criar({ nome: "Ana" });
```

O service acha que fala com o repo real — retorna o que o mock define.

## Async — resolved/rejected

```ts
mockResolvedValue(x)     // → Promise.resolve(x)
mockRejectedValue(e)     // → Promise.reject(e)
mockResolvedValueOnce(x) // só na próxima chamada
```

```ts
repoMock.buscarPorEmail
  .mockResolvedValueOnce(null)                       // 1ª vez: livre
  .mockResolvedValueOnce({ id: 1, email: "a@a" });   // 2ª: existe
```

## Verificando chamadas

```ts
expect(repoMock.criar).toHaveBeenCalled();
expect(repoMock.criar).toHaveBeenCalledTimes(1);
expect(repoMock.criar).toHaveBeenCalledWith({ nome: "Ana" });
expect(repoMock.criar).toHaveBeenCalledWith(
  expect.objectContaining({ nome: expect.any(String) })
);
```

## O teste completo

```ts
describe("UsuarioService", () => {
  const repoMock = {
    buscarPorEmail: jest.fn(),
    criar: jest.fn(),
  };
  const service = new UsuarioService(repoMock as any);

  it("rejeita email duplicado", async () => {
    repoMock.buscarPorEmail.mockResolvedValue({ id: 1 });

    await expect(service.criar({ email: "a@a.com" }))
      .rejects.toThrow("Email já cadastrado");

    expect(repoMock.criar).not.toHaveBeenCalled();   // nunca chegou
  });
});
```

O mock prova **comportamento**: com email ocupado, o service não cria — sem tocar banco.

## jest.mock — módulo inteiro

```ts
jest.mock("../services/email", () => ({
  enviar: jest.fn().mockResolvedValue(true),
}));
```

Substitui o módulo — quando o service importar `enviar`, recebe o mock.

## clearMocks

```json
{ "clearMocks": true }
```

Reseta `mock.calls` e retornos entre testes — sem isso, chamadas acumulam e `toHaveBeenCalledTimes` mente.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `toHaveBeenCalledTimes` errado | Mock sem limpar — `clearMocks` ou `beforeEach` |
| Esperar Promise real do mock | `mockResolvedValue` não `mockReturnValue` |
| Mock com método que falta | O service chama `repo.metodo` que não existe → undefined |
| Verificar implementação em vez de comportamento | `toHaveBeenCalledWith` é sobre o contrato — ok; não sobre como internamente |

## Resumo

- `jest.fn()` + `mockResolvedValue`/`mockReturnValue` = dependência controlada
- `toHaveBeenCalledWith` verifica o que o service passou à dependência
- Mock troca a peça real — teste unitário sem banco, sem rede
- `clearMocks` mantém contadores zerados entre testes
