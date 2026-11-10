# BE01-11 — Notações de Tipos

## As formas de anotar

```typescript
// Variável
let nome: string = "Ana";

// Parâmetro e retorno de função
function soma(a: number, b: number): number {
  return a + b;
}

// Arrow function
const dobro = (n: number): number => n * 2;

// Objeto
const usuario: { nome: string; idade: number } = { nome: "Ana", idade: 28 };
```

## Type annotation vs type assertion

```typescript
// Annotation — declara o tipo que a variável DEVE ter
let valor: number = 10;

// Assertion — diz ao TS "confie em mim, é esse tipo"
const input = document.getElementById("x") as HTMLInputElement;
const dados = JSON.parse(texto) as Usuario;
```

`as` não muda nada em runtime — só desliga a verificação. Use com parcimônia: cada `as` é um ponto cego.

## Optional chaining e nullish

```typescript
interface Usuario {
  nome: string;
  endereco?: { cidade: string };
}

const u: Usuario = { nome: "Ana" };

u.endereco?.cidade;          // string | undefined — não quebra se undefined
u.endereco?.cidade ?? "N/I"; // fallback com ?? (só para null/undefined)
```

`??` vs `||`: `??` só considera `null`/`undefined`; `||` também rejeita `0`, `""`, `false`.

## Satisfies — validar sem perder o tipo literal

```typescript
const config = {
  porta: 3000,
  ambiente: "dev",
} satisfies Record<string, string | number>;

config.porta;  // number (não string|number — tipo literal preservado)
```

## Anotações em estruturas comuns

```typescript
// Array de objetos
const produtos: { id: number; nome: string }[] = [];

// Map / Record
const cache: Record<string, number> = {};
cache["Ana"] = 95;

// Função como tipo
type Operacao = (a: number, b: number) => number;
const multiplicar: Operacao = (a, b) => a * b;
```

## Quando o TS reclama de notação

| Erro | Significado |
| --- | --- |
| `Type X is not assignable to Y` | Valor incompatível com a anotação |
| `Property does not exist` | Objeto tem mais/menos campos que o tipo |
| `Argument of type X` | Parâmetro errado na chamada |

## Resumo

- `:` anota, `as` afirma, `satisfies` valida preservando
- `?.` evita crash em opcionais; `??` dá fallback só pra null/undefined
- Anote fronteiras (params, retornos, API); deixe inferência no resto
