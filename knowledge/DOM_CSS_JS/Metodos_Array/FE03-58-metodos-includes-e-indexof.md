# FE03-58 — Métodos includes e indexOf

## O que são

Dois métodos de **busca** que respondem perguntas diferentes sobre a existência de um valor num array:

- `includes` → **"esse valor existe?"** — retorna `boolean`
- `indexOf` → **"onde esse valor está?"** — retorna a posição ou `-1`

```javascript
const frutas = ["maçã", "banana", "uva"];

frutas.includes("banana"); // true
frutas.includes("pera");   // false

frutas.indexOf("uva");   // 2
frutas.indexOf("pera");  // -1 (não encontrou)
```

## includes — teste de existência

```javascript
array.includes(valorBuscado, indiceInicial);
```

O segundo parâmetro opcional diz a partir de qual posição procurar:

```javascript
const letras = ["a", "b", "c", "a"];

letras.includes("a");    // true
letras.includes("a", 1); // true — existe "a" depois do índice 1
letras.includes("b", 2); // false — "b" está no índice 1, antes do corte
```

### Uso típico: validações e condicionais

```javascript
const permissoes = ["ler", "escrever"];

if (permissoes.includes("escrever")) {
  salvarArquivo();
}
```

Muito mais legível que a alternativa antiga com `indexOf`:

```javascript
// ❌ Estilo antigo — comparação com -1 é indireta
if (lista.indexOf("admin") !== -1) { ... }

// ✅ Moderno — lê-se como frase: "se a lista inclui admin"
if (lista.includes("admin")) { ... }
```

## indexOf — posição da primeira ocorrência

```javascript
array.indexOf(valorBuscado, indiceInicial);
```

Retorna o **índice da primeira** ocorrência, ou `-1` se não existir:

```javascript
const numeros = [10, 20, 30, 20];

numeros.indexOf(20);    // 1 — para na primeira
numeros.indexOf(20, 2); // 3 — procurando a partir do índice 2, acha a segunda
numeros.indexOf(99);    // -1
```

### Companheiro: lastIndexOf

Procura de trás para frente — útil para encontrar a última ocorrência:

```javascript
const numeros = [10, 20, 30, 20];

numeros.lastIndexOf(20); // 3
```

### Uso típico: remover item por valor (com splice)

```javascript
function remover(lista, valor) {
  const indice = lista.indexOf(valor);
  if (indice !== -1) {
    lista.splice(indice, 1);
  }
}
```

## Ambos usam comparação estrita

A busca usa `===` (SameValueZero, no caso do `includes`). Consequência importante: **objetos só são encontrados pela mesma referência**, não por conteúdo equivalente:

```javascript
const usuarios = [{ nome: "Ana" }, { nome: "Beto" }];

// ❌ Objetos literais novos nunca casam — referência diferente
usuarios.includes({ nome: "Ana" }); // false

// ❌ indexOf também falha com objetos
usuarios.indexOf({ nome: "Ana" }); // -1
```

Para buscar objetos por conteúdo, use `find`, `findIndex` ou `some`:

```javascript
// ✅ Buscar objeto por propriedade
usuarios.find(u => u.nome === "Ana");      // { nome: "Ana" }
usuarios.findIndex(u => u.nome === "Ana"); // 0
usuarios.some(u => u.nome === "Ana");      // true
```

## Mapa de decisão

| Pergunta | Valores primitivos | Objetos |
| --- | --- | --- |
| "Existe?" | `includes` | `some(x => x.id === id)` |
| "Onde está?" | `indexOf` | `findIndex(x => x.id === id)` |
| "Qual é?" | `find` | `find(x => x.id === id)` |
| "Quais são?" | `filter` | `filter` |

## Detalhes técnicos

- `includes` encontra `NaN` (`[NaN].includes(NaN)` → `true`); `indexOf` **não** (`[NaN].indexOf(NaN)` → `-1`) — diferença histórica entre os dois
- Também existem `String.prototype.includes` e `indexOf` para buscar dentro de textos: `"javascript".includes("script")` → `true`
- `includes` foi adicionado no ES2016 (ES7) — antes dele, `indexOf(...) !== -1` era o padrão
