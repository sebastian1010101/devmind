# FE05-43 — Tipos Básicos (Primitivos)

## Os primitivos do TypeScript

```typescript
let nome: string = "Ana";
let idade: number = 28;
let ativo: boolean = true;
let nada: null = null;
let indefinido: undefined = undefined;
let simbolo: symbol = Symbol("id");
let grande: bigint = 9007199254740991n;
```

## string

```typescript
let nome: string = "Ana";
let sobrenome: string = 'Silva';
let template: string = `Olá, ${nome}`;

// métodos do JS são tipados
nome.toUpperCase();  // ✅
nome.toFixed(2);     // ❌ erro — toFixed é de number
```

## number

```typescript
let inteiro: number = 42;
let decimal: number = 3.14;
let negativo: number = -10;
let hex: number = 0xff;
let nan: number = NaN; // NaN é number!

idade.toFixed(2);    // "28.00"
idade.toString(16);  // "1c"
```

## boolean

```typescript
let ativo: boolean = true;
let maior: boolean = idade > 18;

// truthy/falsy continuam — mas o tipo é boolean
const resultado = ativo && maior; // boolean
```

## null e undefined

```typescript
let semValor: null = null;
let naoDefinido: undefined = undefined;

// strictNullChecks (strict) — null não é atribuível a outros tipos
let nome: string = null; // ❌ erro com strict

// para permitir: union
let nome: string | null = localStorage.getItem("nome");
```

## Union types — um ou outro

```typescript
let id: string | number = "abc123";
id = 42; // ✅

let status: "ativo" | "inativo" | "pendente"; // literal union
status = "ativo";    // ✅
status = "banana";   // ❌
```

## Arrays

```typescript
let numeros: number[] = [1, 2, 3];
let nomes: Array<string> = ["a", "b"];  // equivalente

let misto: (string | number)[] = ["a", 1];
let qualquer: any[] = [1, "a", true]; // evite
```

## Tuplas — array com posições fixas

```typescript
let coordenada: [number, number] = [10, 20];
let registro: [string, number, boolean] = ["Ana", 28, true];

coordenada[0].toFixed(2); // ✅ number
coordenada[1].toUpperCase(); // ❌ é number
```

## any vs unknown vs never

```typescript
// any — desliga o type-checking (evite)
let x: any = 5;
x.toUpperCase(); // sem erro — bug silencioso

// unknown — aceita qualquer valor, mas exige verificação
let y: unknown = 5;
y.toUpperCase();           // ❌ erro — tem que estreitar
if (typeof y === "string") {
  y.toUpperCase();         // ✅ agora sim
}

// never — nunca acontece (função que lança/loop infinito)
function erro(msg: string): never {
  throw new Error(msg);
}
```

## Funções — parâmetros e retorno

```typescript
function soma(a: number, b: number): number {
  return a + b;
}

// retorno inferido — mas anote para clareza
function dobro(n: number) { return n * 2; } // infere number

// void — sem retorno
function log(msg: string): void {
  console.log(msg);
}

// parâmetro opcional
function saudacao(nome: string, titulo?: string): string {
  return `${titulo || ""} ${nome}`;
}

// valor padrão
function cumprimentar(nome: string, pontuacao = "!"): string {
  return `Olá, ${nome}${pontuacao}`;
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `any` para resolver rápido | `unknown` — força verificação |
| `let x` sem tipo e sem valor | Infere `any` — anote ou inicialize |
| `null` atribuído sem union | `string \| null` ou `?` |
| `number[]` vs `Array<number>` | Equivalentes — consistência é o que conta |

## Resumo

- Primitivos: `string`, `number`, `boolean`, `null`, `undefined`
- Union `|` permite múltiplos tipos; literal union limita a valores exatos
- `any` desliga type-checking; `unknown` mantém com verificação
- Funções: parâmetros tipados, retorno anotado, `void` para sem retorno
