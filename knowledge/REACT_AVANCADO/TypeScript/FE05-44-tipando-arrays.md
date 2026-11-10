# FE05-44 — Tipando Arrays

## As duas sintaxes

```typescript
// Sintaxe [] — mais comum
let numeros: number[] = [1, 2, 3];
let nomes: string[] = ["Ana", "Bruno"];

// Sintaxe Array<T> — equivalente
let numeros: Array<number> = [1, 2, 3];
let nomes: Array<string> = ["Ana", "Bruno"];
```

## Array de objetos — o padrão React

```typescript
type Produto = {
  id: number;
  nome: string;
  preco: number;
  emEstoque: boolean;
};

let produtos: Produto[] = [
  { id: 1, nome: "Mouse", preco: 89.9, emEstoque: true },
  { id: 2, nome: "Teclado", preco: 199.9, emEstoque: false }
];

// métodos herdam a tipagem
produtos.map(p => p.nome);        // string[]
produtos.filter(p => p.emEstoque); // Produto[]
produtos.find(p => p.id === 1);    // Produto | undefined
```

## O `undefined` do find/findIndex

```typescript
const produto = produtos.find(p => p.id === 99);
// tipo: Produto | undefined

produto.nome; // ❌ pode ser undefined

if (produto) {
  produto.nome; // ✅ narrowing
}

produto?.nome; // ✅ encadeamento opcional
```

## Readonly arrays — sem mutação

```typescript
let lista: readonly string[] = ["a", "b"];

lista.push("c"); // ❌ erro — readonly

// útil para props ou constantes
const CORES: readonly string[] = ["#fff", "#000"];
```

## Tuplas — posições tipadas

```typescript
type Resultado = [number, string]; // [status, mensagem]

function buscar(): Resultado {
  return [200, "OK"];
}

const [status, msg] = buscar(); // desestrutura tipado
```

## Arrays multidimensionais

```typescript
let matriz: number[][] = [
  [1, 2],
  [3, 4]
];

let tabuleiro: ("X" | "O" | "")[][] = [
  ["X", "O", ""],
  ["", "X", "O"]
];
```

## Métodos tipados

```typescript
const numeros: number[] = [1, 2, 3, 4, 5];

numeros.map(n => n * 2);              // number[]
numeros.filter(n => n > 2);           // number[]
numeros.reduce((s, n) => s + n, 0);   // number
numeros.every(n => n > 0);            // boolean
numeros.some(n => n > 4);             // boolean
numeros.find(n => n === 3);           // number | undefined
numeros.flat();                       // achata
numeros.flatMap(n => [n, n * 2]);     // number[]
```

## Spread e desestruturação tipados

```typescript
const novos: number[] = [...numeros, 6];
const [primeiro, ...resto]: number[] = numeros;

// rest em funções
function somar(...nums: number[]): number {
  return nums.reduce((s, n) => s + n, 0);
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `array[0]` sem checar tamanho | Pode ser undefined — `array[0]?` |
| `find` sem tratar `undefined` | `find(...)?.propriedade` ou `if` |
| `map` retornando tipo errado | Anote o callback: `(p): string => p.nome` |
| `push` em readonly | `readonly` bloqueia — crie um novo array |

## Resumo

- `T[]` ou `Array<T>` — equivalentes
- `T | undefined` em `find`, `[0]`, etc.
- `readonly T[]` para imutabilidade
- Tuplas `[T1, T2]` para posições fixas
