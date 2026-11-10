# BE01-09 — Tipos Básicos

## Primitivos

```typescript
let nome: string = "Maria";       // texto
let idade: number = 30;            // inteiros E decimais (não existe int/float separado)
let ativo: boolean = true;
let nada: null = null;
let indefinido: undefined = undefined;
let id: bigint = 9007199254740991n;
let simbolo: symbol = Symbol("chave");
```

## Arrays

```typescript
let frutas: string[] = ["maçã", "banana"];
let notas: number[] = [8, 9.5, 10];
let matriz: number[][] = [[1, 2], [3, 4]];

// Sintaxe genérica equivalente
let nomes: Array<string> = ["Ana", "Bia"];
```

## Tuplas — array com tipos fixos por posição

```typescript
let par: [string, number] = ["idade", 30];
// par = [30, "idade"];  // ❌ ordem importa

// Útil para retornos múltiplos
function dividir(a: number, b: number): [number, number] {
  return [Math.floor(a / b), a % b];
}
const [quociente, resto] = dividir(10, 3);
```

## Objetos inline

```typescript
let usuario: { nome: string; idade: number; admin?: boolean } = {
  nome: "Ana",
  idade: 28,
};
// admin? — opcional, pode não existir
```

## Funções

```typescript
// Anotação nos parâmetros e no retorno
function soma(a: number, b: number): number {
  return a + b;
}

// void — não retorna nada
function log(msg: string): void {
  console.log(msg);
}

// Parâmetro opcional e padrão
function saudar(nome: string, pontuacao: string = "!"): string {
  return `Olá, ${nome}${pontuacao}`;
}
```

## Inferência — não anote o óbvio

```typescript
let nome = "Ana";          // TS já sabe: string
const numeros = [1, 2, 3]; // number[]

// Anotar é redundante:
let nome2: string = "Ana"; // funciona, mas desnecessário
```

Anote: parâmetros de função, retornos não óbvios, objetos complexos. Deixe a inferência cobrir o resto.

## Resumo

- `string`, `number`, `boolean` cobrem a maioria dos casos
- `T[]` para arrays, `[A, B]` para tuplas, `?` para opcionais
- `void` = função sem retorno
- Inferência cuida do óbvio — anote parâmetros e fronteiras
