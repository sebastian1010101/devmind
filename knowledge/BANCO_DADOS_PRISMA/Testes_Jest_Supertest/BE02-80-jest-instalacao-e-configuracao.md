# BE02-80 — Jest: Instalação e Configuração

## Setup em projeto TypeScript

```bash
npm install -D jest ts-jest @types/jest
npx ts-jest config:init
```

Gera `jest.config.ts` (ou `.js`):

```ts
// jest.config.ts
export default {
  preset: "ts-jest",
  testEnvironment: "node",
};
```

- `ts-jest` — transpila TS na hora de rodar
- `testEnvironment: "node"` — backend (jsdom seria pra browser)

## Script

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Estrutura de testes

```text
src/
├─ services/
│  ├─ usuario.service.ts
│  └─ __tests__/
│      └─ usuario.service.test.ts     ← colado no módulo
└─ __tests__/                          ← ou pasta central
```

Convenções que o Jest acha sozinho:

- `*.test.ts` / `*.spec.ts`
- arquivos em `__tests__/`

## Configurações úteis

```ts
export default {
  preset: "ts-jest",
  testEnvironment: "node",
  testMatch: ["**/__tests__/**/*.test.ts"],   // só .test.ts em __tests__
  clearMocks: true,                          // limpa mocks entre testes
  setupFilesAfterEach: ... ,                 // (arquivo de setup pós-framework)
};
```

## dotenv nos testes

```bash
npm install -D dotenv-cli
```

```json
"test": "dotenv -e .env.test -- jest --runInBand"
```

- `.env.test` — `DATABASE_URL` apontando para banco de teste
- `--runInBand` — testes em série (importante quando usam o mesmo banco)

## ts-jest vs o resto

| Opção | Quando |
| --- | --- |
| `ts-jest` | Simples, tipado — o da aula |
| `@swc/jest` | Muito mais rápido em projetos grandes |
| `esbuild-jest` | Idem — speed |

## Rodando

```bash
npm test                 # toda a suite
npx jest usuario         # só arquivos com "usuario" no nome
npx jest --watch         # re-roda ao salvar
npx jest --coverage      # relatório de cobertura
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `Cannot use import statement` | Falta `ts-jest`/preset — configure |
| Testes não encontrados | `testMatch` ou nomes fora do padrão |
| `.env` errado no teste | `dotenv-cli` + `.env.test` |
| Testes paralelos pisando no banco | `--runInBand` serializa |

## Resumo

- `jest` + `ts-jest` + `@types/jest`; `preset: ts-jest`, `testEnvironment: node`
- `*.test.ts` em `__tests__/` ou colado no módulo
- `dotenv -e .env.test -- jest --runInBand` — env de teste + serial
- `--watch` para dev, `--coverage` para relatório
