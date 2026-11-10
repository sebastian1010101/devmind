# FE05-48 — TypeScript Generics

## O que são generics

**Tipos parametrizados** — uma função, classe ou tipo que funciona com **qualquer tipo**, mantendo a segurança.

```typescript
// ❌ any — perde o tipo
function primeiro(arr: any[]): any {
  return arr[0];
}

// ✅ generic — preserva o tipo
function primeiro<T>(arr: T[]): T {
  return arr[0];
}

const n = primeiro([1, 2, 3]);     // T infere number
const s = primeiro(["a", "b"]);    // T infere string
const p = primeiro(produtos);      // T infere Produto
```

## A sintaxe `<T>`

```typescript
function identidade<T>(valor: T): T {
  return valor;
}

identidade<string>("oi");   // T = string explícito
identidade("oi");            // T = string inferido
```

`T` é convenção — pode ser `K`, `V`, `TItem`, `TResponse`.

## Generics em funções — o poder real

```typescript
// array de qualquer tipo → primeiro elemento
function primeiro<T>(arr: T[]): T | undefined {
  return arr[0];
}

// mapear com tipo de retorno diferente
function mapear<T, R>(arr: T[], fn: (item: T) => R): R[] {
  return arr.map(fn);
}

mapear([1, 2, 3], n => n.toString()); // R = string
mapear(produtos, p => p.preco);        // R = number
```

## Generics em tipos e interfaces

```typescript
interface Resposta<T> {
  dados: T;
  status: number;
  erro?: string;
}

const res: Resposta<Usuario[]> = {
  dados: [{ id: 1, nome: "Ana" }],
  status: 200
};
```

## Generics com constraints — `<T extends ...>`

```typescript
// T deve ter a propriedade 'id'
function salvar<T extends { id: number }>(item: T): T {
  console.log(item.id); // ✅ garantido
  return item;
}

salvar({ id: 1, nome: "A" }); // ✅
salvar({ nome: "B" });         // ❌ sem id
```

```typescript
// keyof — T deve ter a chave
function pegar<T, K extends keyof T>(obj: T, chave: K): T[K] {
  return obj[chave];
}

pegar({ nome: "Ana", idade: 28 }, "nome"); // retorna string
pegar({ nome: "Ana" }, "email");           // ❌ não existe
```

## Generics em classes

```typescript
class Pilha<T> {
  private itens: T[] = [];

  push(item: T) { this.itens.push(item); }
  pop(): T | undefined { return this.itens.pop(); }
}

const numeros = new Pilha<number>();
numeros.push(1);

const strings = new Pilha<string>();
strings.push("a");
```

## O padrão — hook genérico

```typescript
// useFetch<T> — o tipo de dados vem de fora
function useFetch<T>(url: string) {
  const [dados, setDados] = useState<T | null>(null);
  const [carregando, setCarregando] = useState(true);
  // ...
  return { dados, carregando };
}

const { dados } = useFetch<Produto[]>("/api/produtos");
// dados: Produto[] | null — tipado!
```

## Generics padrão — `T = X`

```typescript
interface Config<T = string> {
  chave: string;
  valor: T;
}

const a: Config = { chave: "x", valor: "y" };        // T = string
const b: Config<number> = { chave: "x", valor: 42 }; // T = number
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `any` em vez de `<T>` | Generics preservam — `any` apaga |
| Tipo sem constraint | `T extends X` limita o aceitável |
| Generic de mais | Se só um tipo existe, não precisa de T |
| `T` inferido errado | `useFetch<MeuTipo>` explícito |

## Resumo

- `<T>` = parâmetro de tipo — a função aceita qualquer tipo, tipada
- `T extends X` limita; `keyof` lê chaves; `T[K]` indexa
- Generics em hooks (`useFetch<T>`) tornam o tipo configurável
- Use quando o tipo é variável mas deve ser rastreado
