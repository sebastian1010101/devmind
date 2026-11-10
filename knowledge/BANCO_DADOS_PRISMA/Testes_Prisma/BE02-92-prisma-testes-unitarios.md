# BE02-92 — Prisma: Testes Unitários

## Mockando o PrismaClient

O service chama `prisma.usuario.create(...)` — no teste unitário, o client inteiro é fake:

```ts
const prismaMock = {
  usuario: {
    create: jest.fn(),
    findUnique: jest.fn(),
    findMany: jest.fn(),
  },
};

const service = new UsuarioService(prismaMock as any);
```

```ts
it("cria usuário", async () => {
  prismaMock.usuario.findUnique.mockResolvedValue(null);
  prismaMock.usuario.create.mockResolvedValue({ id: 1, email: "a@a.com" });

  const usuario = await service.criar({ nome: "Ana", email: "a@a.com" });

  expect(usuario.email).toBe("a@a.com");
  expect(prismaMock.usuario.create).toHaveBeenCalledWith(
    expect.objectContaining({
      data: expect.objectContaining({ email: "a@a.com" }),
    })
  );
});
```

## Aplicando as regras de negócio

```ts
it("rejeita email duplicado", async () => {
  prismaMock.usuario.findUnique.mockResolvedValue({ id: 5 });

  await expect(service.criar({ email: "x@x.com" }))
    .rejects.toThrow("Email já cadastrado");

  expect(prismaMock.usuario.create).not.toHaveBeenCalled();
});

it("hash de senha antes de salvar", async () => {
  prismaMock.usuario.findUnique.mockResolvedValue(null);
  prismaMock.usuario.create.mockResolvedValue({});

  await service.criar({ email: "a@a.com", senha: "12345678" });

  const call = prismaMock.usuario.create.mock.calls[0][0];
  expect(call.data.senha).not.toBe("12345678");   // hash, não a senha
});
```

## Mock de erro do Prisma

```ts
import { Prisma } from "@prisma/client";

it("P2002 do banco vira 409", async () => {
  prismaMock.usuario.findUnique.mockResolvedValue(null);
  prismaMock.usuario.create.mockRejectedValue(
    new Prisma.PrismaClientKnownRequestError("Unique", {
      code: "P2002",
      clientVersion: "5.0.0",
    })
  );

  await expect(service.criar({ email: "a@a.com" }))
    .rejects.toMatchObject({ statusCode: 409 });
});
```

`mockRejectedValue` simula o erro do banco — prova que o service traduz `P2002` corretamente.

## Verificando a query — include/select

```ts
it("include traz livros", async () => {
  prismaMock.autor.findUnique.mockResolvedValue({ id: 1, livros: [] });

  await service.buscarAutor(1);

  expect(prismaMock.autor.findUnique).toHaveBeenCalledWith(
    expect.objectContaining({
      include: expect.objectContaining({ livros: true }),
    })
  );
});
```

Testa o **contrato** — o service pede a relação certa ao Prisma.

## O que mock não prova

```text
mockResolvedValue aceita qualquer coisa — o Prisma real pode rejeitar
```

O mock prova que o service chama certo; **integração** prova que o Prisma executa. Os dois se complementam.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `usuario` no mock com typo | Objeto do mock precisa espelhar `prisma.usuario` |
| Mock retorna não-Promise | `mockResolvedValue` — não `mockReturnValue` |
| Erro Prisma inventado como Error genérico | Use `PrismaClientKnownRequestError` com `code` |
| Verificar detalhe de implementação demais | Teste comportamento — o que o service decide/faz |

## Resumo

- `jest.fn()` por método do client — service usa sem saber
- `mockResolvedValue`/`mockRejectedValue` dirigem os caminhos
- Erros do Prisma (`P2002`) simulados testam a tradução para `AppError`
- `toHaveBeenCalledWith` prova a query pedida — mas só integração prova que roda
