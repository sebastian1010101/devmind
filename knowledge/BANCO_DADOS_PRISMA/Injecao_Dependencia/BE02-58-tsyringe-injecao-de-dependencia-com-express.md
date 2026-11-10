# BE02-58 — Tsyringe: Injeção de Dependência com Express

## O que é

**tsyringe** é o container de DI da Microsoft para TypeScript — registra classes e resolve a árvore de dependências automaticamente.

```bash
npm install tsyringe reflect-metadata
```

## Setup obrigatório

```json
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

```ts
// no topo do entrypoint — antes de tudo
import "reflect-metadata";
```

Sem `reflect-metadata` + os dois flags, o tsyringe não consegue ler os tipos dos parâmetros.

## A mecânica

```ts
import { injectable } from "tsyringe";

@injectable()
class UsuarioService {
  constructor(private repo: UsuarioRepository) {}
  // tsyringe resolve UsuarioRepository sozinho
}
```

```ts
// resolver manualmente
import { container } from "tsyringe";

const service = container.resolve(UsuarioService);
// o container: cria UsuarioRepository → injeta no UsuarioService
```

`container.resolve(X)` = "monte X com tudo que ele precisa" — recursivamente.

## Registrando

```ts
import { container } from "tsyringe";

// classe → classe
container.register("IUsuarioRepository", { useClass: PrismaUsuarioRepository });

// ou pelo próprio tipo
container.registerSingleton(UsuarioService);
container.registerInstance(PrismaClient, prisma);
```

| Registro | Efeito |
| --- | --- |
| `useClass` | Cada `resolve` cria nova instância (transient) |
| `registerSingleton` | Uma instância só para a app inteira |
| `registerInstance` | Objeto já criado vira a dependência |

## Com Express

```ts
// controllers/UsuarioController.ts
@injectable()
export class UsuarioController {
  constructor(private service: UsuarioService) {}

  criar = async (req: Request, res: Response) => {
    const usuario = await this.service.criar(req.body);
    return res.status(201).json(usuario);
  };
}
```

```ts
// routes/usuario.routes.ts
const controller = container.resolve(UsuarioController);

router.post("/usuarios", controller.criar);
```

O controller pede o service; o service pede o repo — `resolve` monta tudo de uma vez.

## Atenção com arrow functions

```ts
// ❌ método comum — this se perde no Express
criar(req: Request, res: Response) { ... }

// ✅ arrow property — this é léxico
criar = async (req: Request, res: Response) => { ... };
```

Express chama o handler sem contexto — arrow function preserva o `this` da classe.

## Por onde começar

```text
1. @injectable() em services e repositories
2. registros no bootstrap (container.register...)
3. controller resolvido via container.resolve()
4. testes: container.registerInstance com mocks
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Reflect.hasOwnMetadata` errors | Falta `import "reflect-metadata"` no entrypoint |
| Decorator syntax error | `experimentalDecorators` + `emitDecoratorMetadata` no tsconfig |
| `this` undefined na rota | Use arrow function (`criar = async () =>`) |
| Registro depois do resolve | Registre antes de resolver — bootstrap primeiro |

## Resumo

- `tsyringe` = container DI; `reflect-metadata` + decorators ligam os tipos
- `@injectable()` na classe + `container.resolve()` monta a árvore
- `useClass` (transient), `registerSingleton`, `registerInstance`
- No Express, handlers são arrow functions para preservar `this`
