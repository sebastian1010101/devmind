# FE05-47 — Union Type

## O que é union type

Um valor que pode ser **um de vários tipos** — `|` separa as possibilidades.

```typescript
let id: string | number;
id = "abc123"; // ✅
id = 42;        // ✅
id = true;      // ❌ boolean não está na union
```

## Literal union — valores exatos

```typescript
type Status = "pendente" | "aprovado" | "rejeitado";
type Tema = "claro" | "escuro";
type Direcao = "norte" | "sul" | "leste" | "oeste";

let s: Status = "pendente"; // ✅
s = "banana";               // ❌
```

É como um `enum` mais leve — autocompleta e valida.

## Narrowing — estreitando o tipo

```typescript
function processar(valor: string | number) {
  // typeof estreita
  if (typeof valor === "string") {
    return valor.toUpperCase(); // valor é string aqui
  }
  return valor.toFixed(2);       // valor é number aqui
}
```

### Narrowing com instanceof

```typescript
if (valor instanceof Date) {
  valor.getFullYear();
}
```

### Narrowing com propriedade discriminante

```typescript
type Circulo = { tipo: "circulo"; raio: number };
type Quadrado = { tipo: "quadrado"; lado: number };
type Forma = Circulo | Quadrado;

function area(f: Forma): number {
  switch (f.tipo) {              // discrimina pelo campo
    case "circulo": return Math.PI * f.raio ** 2;
    case "quadrado": return f.lado ** 2;
  }
}
```

O `tipo` comum é a **propriedade discriminante** — o switch descobre qual é.

## null/undefined na union

```typescript
type Nome = string | null;

function exibir(nome: Nome) {
  // guard clause — sai cedo
  if (nome === null) return "Anônimo";
  return nome.toUpperCase(); // string aqui — narrowing
}
```

## Optional chaining vs narrowing

```typescript
interface Usuario {
  perfil?: { avatar?: string };
}

const avatar = usuario?.perfil?.avatar;
// tipo: string | undefined
```

`?.` cria union com `undefined` — trate antes de usar.

## Exhaustive check — o switch completo

```typescript
function area(f: Forma): number {
  switch (f.tipo) {
    case "circulo": return Math.PI * f.raio ** 2;
    case "quadrado": return f.lado ** 2;
    default:
      const _: never = f; // erro se faltar um caso
      return _;
  }
}
```

Se adicionar `"triangulo"` e esquecer de tratar → erro de compilação.

## Union em arrays e parâmetros

```typescript
let misto: (string | number)[] = ["a", 1, "b"];

function aceitar(input: string | string[]) {
  if (Array.isArray(input)) {
    return input.join(", "); // string[] aqui
  }
  return input;              // string aqui
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Acessar prop sem narrowing | `if (typeof)`, `in`, `instanceof` |
| `null` ignorado | `string \| null` — cheque antes |
| Switch sem default | `never` no default pega o que faltar |
| Union de objetos sem discriminante | Adicione campo `tipo`/`kind` comum |

## Resumo

- `A | B` = pode ser um ou outro
- Literal union `"a" | "b"` = valores exatos
- `typeof`, `instanceof`, discriminante → narrowing
- `?.` cria union com `undefined` — trate
- Exhaustive check com `never` pega casos faltando
