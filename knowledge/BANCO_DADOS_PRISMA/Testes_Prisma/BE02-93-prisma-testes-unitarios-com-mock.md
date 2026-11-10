# BE02-93 — Prisma: Testes Unitários com Mock

## jest-mock-extended — mock tipado

Mock manual (`{ usuario: { create: jest.fn() } }`) não é tipado e repete estrutura. `jest-mock-extended` gera o mock completo do `PrismaClient`:

```bash
npm install -D jest-mock-extended
```

```ts
import { mockDeep, mockReset, DeepMockProxy } from "jest-mock-extended";
import { PrismaClient } from "@prisma/client";

const prismaMock = mockDeep<PrismaClient>();
// prismaMock.usuario.create — já é jest.fn tipado
```

Todo método existe e é tipado — `mockResolvedValue` aceita só o tipo certo.

## Injetando o mock

```ts
// o service recebe PrismaClient — o mock implementa
const service = new UsuarioService(prismaMock as unknown as PrismaClient);

// ou pelo tsyringe/DI
container.registerInstance(PrismaClient, prismaMock as unknown as PrismaClient);
const service = container.resolve(UsuarioService);
```

## O padrão com jest.mock

Quando o service **importa** o `prisma` singleton em vez de receber:

```ts
// __tests__/usuario.test.ts
jest.mock("../src/database/prisma", () => ({
  __esModule: true,
  prisma: mockDeep<PrismaClient>(),
}));

import { prisma } from "../src/database/prisma";
const prismaMock = prisma as unknown as DeepMockProxy<PrismaClient>;
```

O módulo inteiro é trocado — quem importa `prisma` recebe o deep mock.

## Uso

```ts
beforeEach(() => mockReset(prismaMock));

it("retorna usuário", async () => {
  prismaMock.usuario.findUnique.mockResolvedValue({
    id: 1, nome: "Ana", email: "a@a.com",
  } as any);

  const usuario = await service.buscar(1);
  expect(usuario?.nome).toBe("Ana");
});

it("propaga erro do client", async () => {
  prismaMock.usuario.findUnique.mockRejectedValue(new Error("db down"));
  await expect(service.buscar(1)).rejects.toThrow();
});
```

## mockReset vs clearMocks

| | Limpa |
| --- | --- |
| `mockReset` | Calls **e** implementações (`mockResolvedValue`) |
| `clearMocks` (config) | Só calls |

`mockReset` por teste — retornos antigos não vazam.

## Verificando args

```ts
expect(prismaMock.usuario.create).toHaveBeenCalledWith({
  data: { email: "a@a.com", senha: expect.any(String) },
});
```

`expect.any`, `expect.objectContaining`, `expect.stringContaining` fazem match parcial — o hash do bcrypt é diferente toda vez.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `prismaMock.usuario.X` undefined | `mockDeep` cobre todos — se falha, confira o nome do model (`minúsculo`) |
| Mock sem tipar | `DeepMockProxy<PrismaClient>` — autocomplete completo |
| Retornos de teste anterior vazando | `mockReset` no `beforeEach` |
| `as any` excessivo | `as unknown as PrismaClient` é mais explícito |

## Resumo

- `mockDeep<PrismaClient>()` = client inteiro mockado e tipado
- `jest.mock` troca o singleton importado; DI injeta o mock
- `mockReset` entre testes — retornos não vazam
- `expect.any`/`objectContaining` resolvem valores dinâmicos (hash, datas)
