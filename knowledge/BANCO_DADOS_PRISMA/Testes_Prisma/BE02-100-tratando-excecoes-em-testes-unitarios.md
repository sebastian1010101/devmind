# BE02-100 — Tratando Exceções em Testes Unitários

## Por que testar o erro

O caminho feliz é o que já funciona. Os **erros** são onde a qualidade mora — validação, 404, 409, regras de negócio.

```text
teste de exceção = prova que o service LANÇA o erro certo
                   e NÃO executa o efeito colateral
```

## Asserts de erro

```ts
// async — sempre rejects
await expect(service.criar(dadosRuins)).rejects.toThrow("Email inválido");
await expect(service.criar(dadosRuins)).rejects.toThrow(AppError);
await expect(service.criar(dadosRuins)).rejects.toMatchObject({
  statusCode: 409,
  message: "Email já cadastrado",
});

// síncrono — arrow function
expect(() => fn()).toThrow("mensagem");
expect(() => fn()).toThrow(AppError);
```

`rejects` em Promise; `() =>` em síncrono — confundir é o erro mais comum.

## O que verificar além do erro

```ts
it("email duplicado impede o create", async () => {
  prismaMock.usuario.findUnique.mockResolvedValue({ id: 1 });

  await expect(service.criar(dados)).rejects.toThrow("Email já cadastrado");

  // o efeito NÃO aconteceu
  expect(prismaMock.usuario.create).not.toHaveBeenCalled();
});
```

A exceção é só metade — o outro lado é provar que **nada aconteceu** depois.

## Hierarquia de erros customizados

```ts
export class AppError extends Error {
  constructor(message: string, public statusCode: number) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(msg = "Não encontrado") { super(msg, 404); }
}
```

```ts
await expect(service.buscar(99)).rejects.toThrow(NotFoundError);
await expect(service.buscar(99)).rejects.toMatchObject({ statusCode: 404 });
```

Teste por tipo **e** por código — uma rota pode trocar a mensagem sem quebrar a API.

## Erros do Prisma nos testes

```ts
const p2002 = new Prisma.PrismaClientKnownRequestError("Unique failed", {
  code: "P2002",
  clientVersion: "5.0.0",
  meta: { target: ["email"] },
});

prismaMock.usuario.create.mockRejectedValue(p2002);

await expect(service.criar(dados))
  .rejects.toMatchObject({ statusCode: 409 });
```

O service deve **traduzir** o erro técnico (P2002) em semântico (409) — esse é o comportamento testado.

## try/catch no teste — alternativa

```ts
it("lança o erro certo", async () => {
  try {
    await service.criar(dadosRuins);
    fail("deveria ter lançado");   // se passar, força falha
  } catch (e) {
    expect(e).toBeInstanceOf(AppError);
    expect(e.statusCode).toBe(409);
  }
});
```

`rejects` é mais limpo; try/catch dá acesso ao objeto de erro inteiro.

## Matriz de erros a cobrir

| Service faz | Teste |
| --- | --- |
| findUnique → null → throw | 404 |
| findUnique → acha → throw | 409 duplicata |
| create → P2002 do banco | 409 traduzido |
| validação → throw | 400 + `not.toHaveBeenCalled` |
| dependência down | erro propaga? é tratado? |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `expect(promise).toThrow` | Promise usa `rejects.toThrow` — não `toThrow` |
| Testar mensagem e não status | `toMatchObject({ statusCode })` — mensagem muda, código não |
| Só o erro, sem o efeito | `not.toHaveBeenCalled` prova que parou antes |
| Erro genérico passa | `toThrow(AppError)` distingue de TypeError inesperado |

## Resumo

- `rejects.toThrow`/`toMatchObject` para async; `() =>` para síncrono
- Exceção + efeito-ausente = o teste completo
- `AppError` tipado com `statusCode` testa o contrato, não o texto
- P2002 → 409 é tradução de erro — um dos testes mais valiosos
