# BE01-06 — Arquivo tsconfig.json

## O que é

O arquivo de configuração do compilador TypeScript — diz **como** transformar `.ts` em `.js` e **quais verificações** fazer.

```bash
npx tsc --init   # gera um tsconfig.json comentado
```

## Configuração típica para backend Node

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "moduleResolution": "node",
    "lib": ["ES2020"],

    "rootDir": "./src",
    "outDir": "./dist",

    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,

    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## As opções importantes

| Opção | O que faz |
| --- | --- |
| `target` | Versão do JS gerado — `ES2020` cobre Node 14+ |
| `module` | Sistema de módulos — `commonjs` (`require`) ou `esnext` (`import`) |
| `rootDir` | Onde estão os `.ts` fonte |
| `outDir` | Onde sai o `.js` compilado |
| `strict` | Liga TODAS as verificações rigorosas — sempre `true` |
| `esModuleInterop` | Permite `import express from "express"` em módulos CommonJS |
| `skipLibCheck` | Pula checagem de tipos de libs terceiras — compila muito mais rápido |
| `resolveJsonModule` | Permite `import dados from "./dados.json"` |
| `include`/`exclude` | Quais arquivos o compilador considera |

## `strict` — o que ele liga

```typescript
// strictNullChecks — null/undefined são tipos separados
let nome: string = null;        // ❌ com strict
let nome: string | null = null; // ✅ explícito

// noImplicitAny — parâmetro sem tipo é proibido
function soma(a, b) {}  // ❌ a e b são any implícito

// strictBindCallApply, noImplicitThis, useUnknownInCatchVariables...
```

Sem `strict`, o TS vira um "JS com anotações opcionais" — você perde o principal benefício.

## `include` e `exclude`

```json
"include": ["src/**/*"],     // só compila o que está em src/
"exclude": ["node_modules"]  // nunca compile dependências
```

Arquivos fora do `include` não geram saída nem são verificados.

## Erros comuns

| Sintoma | Causa |
| --- | --- |
| `Cannot use import statement` | `module: commonjs` com `import` sem `esModuleInterop`, ou rodando `.ts` direto no node |
| Import de JSON falha | Falta `resolveJsonModule` |
| Compilação lenta | Falta `skipLibCheck: true` |
| Erros em `node_modules` | `exclude` não configurado |

## Resumo

- `tsconfig.json` controla compilação e verificação de tipos
- Essenciais: `strict`, `outDir`, `rootDir`, `esModuleInterop`, `skipLibCheck`
- `include`/`exclude` delimitam o que o compilador vê
- `tsc --init` gera um template comentado de referência
