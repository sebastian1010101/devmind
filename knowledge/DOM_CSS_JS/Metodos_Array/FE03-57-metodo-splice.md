# FE03-57 — Método splice

## O que é

`splice` é a canivete suíço de edição de arrays: **remove, insere e substitui** elementos em qualquer posição. Diferente de `map` e `filter`, ele é um método **mutável** — altera o array original diretamente.

```javascript
const frutas = ["maçã", "banana", "uva", "pera"];

const removidas = frutas.splice(1, 2);

console.log(removidas); // ["banana", "uva"] — o que saiu
console.log(frutas);    // ["maçã", "pera"]  — o original mudou!
```

## Sintaxe

```javascript
array.splice(indiceInicial, quantidadeARemover, ...itensAInserir);
```

- **indiceInicial** — posição onde a operação começa (negativo conta do fim)
- **quantidadeARemover** — quantos elementos remover (0 = só inserir)
- **itensAInserir** — elementos opcionais a inserir no lugar

O retorno é um **array com os elementos removidos** — ou `[]` se nada foi removido.

## As três operações

### 1. Remover elementos

```javascript
const cores = ["azul", "verde", "vermelho", "amarelo"];

cores.splice(1, 2); // remove a partir do índice 1, 2 elementos
// ["azul", "amarelo"]
```

### 2. Inserir elementos (removendo 0)

```javascript
const letras = ["a", "d"];

letras.splice(1, 0, "b", "c"); // no índice 1, remove 0, insere "b" e "c"
// ["a", "b", "c", "d"]
```

### 3. Substituir elementos

```javascript
const itens = ["lápis", "caneta", "borracha"];

itens.splice(1, 1, "marcador"); // troca "caneta" por "marcador"
// ["lápis", "marcador", "borracha"]
```

## Índices negativos

```javascript
const fila = ["Ana", "Beto", "Carla", "Diego"];

fila.splice(-1, 1); // remove o último (Diego)
fila.splice(-2, 1); // remove o penúltimo (Carla)
// ["Ana", "Beto"]
```

## splice vs slice — a confusão eterna

| | `splice` | `slice` |
| --- | --- | --- |
| Altera o original? | **Sim** (mutável) | Não (imutável) |
| Parâmetros | `(início, quantidade, ...insersão)` | `(início, fim)` |
| Retorna | Elementos **removidos** | **Cópia** do trecho |
| Uso | Editar o array | Extrair/copiar trecho |

```javascript
const numeros = [1, 2, 3, 4, 5];

numeros.slice(1, 3);  // [2, 3] — cópia, numeros intacto
numeros.splice(1, 3); // remove [2, 3, 4] — numeros vira [1, 5]
```

Mnemônico: `sPlice` tem P de **P**ermanente (muda o array).

## Caso de uso real: remover item de uma lista

Padrão clássico de todo CRUD — achar a posição com `findIndex` e remover com `splice`:

```javascript
const tarefas = [
  { id: 1, texto: "Estudar" },
  { id: 2, texto: "Treinar" },
  { id: 3, texto: "Ler" }
];

function removerTarefa(id) {
  const indice = tarefas.findIndex(t => t.id === id);
  if (indice !== -1) {
    tarefas.splice(indice, 1);
  }
}

removerTarefa(2);
// [{ id: 1 }, { id: 3 }]
```

## O jeito imutável (preferido em código moderno)

Em React e arquiteturas reativas, mutar arrays diretamente causa bugs de renderização. O equivalente imutável usa `filter` ou `slice`+spread:

```javascript
// ❌ Mutável
lista.splice(indice, 1);

// ✅ Imutável — cria um novo array
const novaLista = lista.filter((_, i) => i !== indice);

// ou
const novaLista = [...lista.slice(0, indice), ...lista.slice(indice + 1)];
```

## Cuidados

- `splice(1)` sem segundo argumento remove **do índice até o fim** — `splice(1)` em `[1,2,3,4]` deixa só `[1]`
- Por ser mutável, evite `splice` dentro de iterações sobre o mesmo array — índices mudam durante o laço e elementos são pulados
- `splice` retorna os removidos, **não** o array editado — `lista.splice(0,1)` não é "a lista sem o primeiro item"

## Mapa rápido de edição de arrays

| Quero... | Mutável | Imutável |
| --- | --- | --- |
| Remover por posição | `splice(i, 1)` | `filter((_, j) => j !== i)` |
| Remover por valor | `splice(indexOf(v), 1)` | `filter(x => x !== v)` |
| Inserir no meio | `splice(i, 0, v)` | `[...a.slice(0,i), v, ...a.slice(i)]` |
| Adicionar no fim | `push(v)` | `[...a, v]` |
| Remover do fim | `pop()` | `a.slice(0, -1)` |
