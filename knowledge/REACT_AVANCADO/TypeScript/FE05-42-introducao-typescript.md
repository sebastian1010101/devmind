# FE05-42 — Introdução ao TypeScript

## O que é o TypeScript

JavaScript **com tipos estáticos** — um superset que adiciona verificação de tipos em tempo de desenvolvimento e compila para JS puro.

```typescript
// JavaScript — o erro só aparece rodando
function soma(a, b) {
  return a + b;
}
soma("2", 3); // "23" — bug silencioso

// TypeScript — o erro aparece ANTES de rodar
function soma(a: number, b: number): number {
  return a + b;
}
soma("2", 3); // ❌ Erro no editor: 'string' não é 'number'
```

## Por que usar

| Problema JS | TS resolve |
| --- | --- |
| `undefined is not a function` | Tipo `null`/`undefined` checado |
| Erro só em runtime | Erro no editor/compilação |
| Refatorar sem saber o que quebra | Renomear tipo → erros em todo lugar |
| Props/componentes sem contrato | Interface define o que é obrigatório |
| Autocomplete fraco | IntelliSense completo |

## Compilação

```text
arquivo.ts  →  tsc (TypeScript Compiler)  →  arquivo.js
               │
               └── verifica tipos ANTES de gerar o JS
```

O navegador não roda `.ts` — o TS compila pra JS antes.

## Instalação

```bash
# Global (compilador)
npm install -g typescript

# No projeto
npm install --save-dev typescript
npx tsc --init  # cria tsconfig.json

# Compilar
npx tsc arquivo.ts          # → arquivo.js
npx tsc --watch             # compila a cada save
```

## O tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "strict": true,           // todas as verificações rigorosas
    "outDir": "./dist",        // onde o JS compilado sai
    "rootDir": "./src",
    "moduleResolution": "bundler",
    "esModuleInterop": true
  },
  "include": ["src"]
}
```

`strict: true` — o modo recomendado; pega a maioria dos bugs.

## Anotação de tipos — a sintaxe

```typescript
let nome: string = "Ana";
let idade: number = 28;
let ativo: boolean = true;
let lista: string[] = ["a", "b"];
let obj: { nome: string } = { nome: "Ana" };

function saudacao(nome: string): string {
  return `Olá, ${nome}`;
}
```

## Type inference — TS deduz

```typescript
let nome = "Ana";      // TS infere: string
let idade = 28;        // TS infere: number
let lista = [1, 2];    // TS infere: number[]

nome = 42; // ❌ erro — já sabe que é string
```

Você não precisa anotar tudo — o TS infere quando é óbvio.

## Type vs Interface (prévia)

```typescript
type Usuario = {
  nome: string;
  idade: number;
};

interface Usuario {
  nome: string;
  idade: number;
}
```

Ambos funcionam — `interface` é mais comum para objetos, `type` é mais flexível.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `any` para "fazer funcionar" | Perde o benefício — tipifique ou use `unknown` |
| Sem `strict` | `"strict": true` no tsconfig |
| `.ts` no navegador | Compile pra `.js` primeiro |
| Anotar o que o TS infere | Deixe a inferência trabalhar |

## Resumo

- TS = JS + tipos estáticos — pega erros antes de rodar
- `strict: true` no tsconfig — modo rigoroso recomendado
- Inferência cobre o óbvio — anote só quando necessário
- Compila pra JS — navegador não entende `.ts`
