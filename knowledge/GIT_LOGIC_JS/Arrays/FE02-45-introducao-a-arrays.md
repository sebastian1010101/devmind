# FE02-45 — Introdução a Arrays

## O que é um Array (Vetor)?

Um **Array** (vetor ou arranjo) é uma estrutura de dados fundamental utilizada para **armazenar uma coleção ordenada de múltiplos valores** sob um único nome de variável.

Em vez de criar variáveis soltas para cada item:
```javascript
// Ineficiente e difícil de manter:
const aluno1 = "Lucas";
const aluno2 = "Beatriz";
const aluno3 = "Mateus";
```

Utilizamos um array:
```javascript
// Estruturado e escalável:
const alunos = ["Lucas", "Beatriz", "Mateus"];
```

---

## Índices Baseados em Zero (Zero-Based Index)

Cada elemento em um array possui uma posição numérica chamada **índice** (*index*), que inicia obrigatoriamente em `0`:

```text
Array:   ["Lucas", "Beatriz", "Mateus", "Mariana"]
Índice:      0          1         2         3
```

### Acessando e Modificando Elementos:

```javascript
const linguagens = ["HTML", "CSS", "JavaScript"];

// Acesso por índice:
console.log(linguagens[0]); // "HTML"
console.log(linguagens[2]); // "JavaScript"

// Modificação de elemento existente:
linguagens[1] = "CSS3 Moderno";

// Leitura do comprimento total:
console.log(linguagens.length); // 3

// Acessar dinamicamente o último elemento:
console.log(linguagens[linguagens.length - 1]); // "JavaScript"
```

---

## Métodos Fundamentais de Inserção e Remoção

| Método | Operação | Onde Atua? | Retorno do Método |
| --- | --- | --- | --- |
| `.push(item)` | Adiciona um ou mais itens | **No final** do array | O novo `length` do array |
| `.pop()` | Remove o último elemento | **No final** do array | O elemento que foi removido |
| `.unshift(item)` | Adiciona um ou mais itens | **No início** do array | O novo `length` do array |
| `.shift()` | Remove o primeiro elemento | **No início** do array | O elemento que foi removido |

```javascript
const fila = ["Ana", "Carlos"];

fila.push("Daniel");      // ["Ana", "Carlos", "Daniel"]
fila.unshift("Amanda");   // ["Amanda", "Ana", "Carlos", "Daniel"]
const atendido = fila.shift(); // Remove "Amanda"
const desistente = fila.pop(); // Remove "Daniel"

console.log(fila); // ["Ana", "Carlos"]
```
