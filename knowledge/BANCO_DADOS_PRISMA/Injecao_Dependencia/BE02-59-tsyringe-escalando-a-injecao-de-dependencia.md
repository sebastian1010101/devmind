# BE02-59 — Tsyringe: Escalando a Injeção de Dependência

## Quando o bootstrap manual não escala

```text
1 service   → 1 register — ok
10 services → 10+ registers, ordem importa, revisão fica difícil
```

Escalar DI = convenções + organização de registros + uso correto de tokens.

## Tokens — nomeando dependências

```ts
// tokens.ts — string ou symbol identificando a abstração
export const TOKENS = {
  UsuarioRepository: "UsuarioRepository",
  EmailService: "EmailService",
  Prisma: "Prisma",
} as const;
```

```ts
// registro
container.register(TOKENS.UsuarioRepository, {
  useClass: PrismaUsuarioRepository,
});

// injeção
@injectable()
class UsuarioService {
  constructor(
    @inject(TOKENS.UsuarioRepository) private repo: IUsuarioRepository,
  ) {}
}
```

`@inject(token)` resolve por nome — necessário quando o tipo é **interface** (interfaces não existem em runtime; o token é a ponte).

## Organizando os registros

```ts
// src/container.ts — um arquivo, todos os registros
import { container } from "tsyringe";
import { PrismaClient } from "@prisma/client";

container.registerInstance(TOKENS.Prisma, new PrismaClient());
container.registerSingleton(TOKENS.UsuarioRepository, PrismaUsuarioRepository);
container.registerSingleton(TOKENS.EmailService, SmtpEmailService);
```

```ts
// server.ts
import "reflect-metadata";
import "./container";     // registra tudo antes de subir
import { app } from "./app";
```

## Scopes — quantas instâncias

| Scope | tsyringe | Uso |
| --- | --- | --- |
| Transient | `useClass` | Stateless — o padrão |
| Singleton | `registerSingleton` | Client de banco, cache |
| Resolution-scoped | — | Uma por resolução |
| Container-scoped | `Lifecycle.ContainerScoped` | Uma por container filho |

```ts
container.register(PrismaClient, { useValue: prisma });  // mesmo que registerInstance
```

## Testando com o container

```ts
// trocando a dependência no teste
import { container } from "tsyringe";

container.registerInstance(TOKENS.UsuarioRepository, repoMock);
const service = container.resolve(UsuarioService);
// service usa o mock — sem banco
```

Ou isole com container filho:

```ts
const testContainer = container.createChildContainer();
testContainer.registerInstance(TOKENS.Prisma, prismaTest);
```

`createChildContainer()` — overrides locais sem sujar o global.

## Alternativa — injeção manual estruturada

Tsyringe não é obrigatório. Um `container.ts` manual funciona:

```ts
// factories.ts
export function makeUsuarioService() {
  return new UsuarioService(new PrismaUsuarioRepository(prisma));
}
```

Funciona para projetos pequenos — o tsyringe vale quando a árvore cresce e os testes precisam trocar peças.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Cannot inject "IUsuarioRepository"` | Interface não existe em runtime — use `@inject(token)` |
| Dependência errada injetada | O token resolve o registrado — confira o `container.ts` |
| Singleton de request | Singleton guarda estado compartilhado — dados de request não vão lá |
| Registros espalhados | Centralize no `container.ts` — importado no entrypoint |

## Resumo

- Tokens (`@inject`) resolvem interfaces — que não existem em runtime
- Centralize registros num `container.ts` importado no bootstrap
- `registerSingleton` para PrismaClient — um pool só
- `createChildContainer()` isola overrides em testes
