# FE02-60 — Array Aninhado

## O que é um Array Aninhado (Matriz)?

Um **Array Aninhado** (frequentemente chamado de matriz bidimensional ou array multidimensional) é um array cujos elementos internos são, por sua vez, **outros arrays**.

Essa estrutura é ideal para representar dados em formato de **linhas e colunas** (como tabelas de Excel, tabuleiros de xadrez, pixels de imagens ou coordenadas cartesianas).

```javascript
// Representação de uma Matriz 3x3:
const tabuleiro = [
  ["X", "O", "X"], // Linha 0
  ["O", "X", "O"], // Linha 1
  ["O", "O", "X"]  // Linha 2
];
```

---

## Como Acessar Elementos em Matrizes

O acesso exige dois pares consecutivos de colchetes:
- O primeiro colchete seleciona a **linha** (o array interno).
- O segundo colchete seleciona a **coluna** (o elemento dentro do array interno).

```javascript
// Sintaxe: matriz[linha][coluna]
console.log(tabuleiro[0][0]); // "X" (linha 0, coluna 0)
console.log(tabuleiro[1][2]); // "O" (linha 1, coluna 2)
console.log(tabuleiro[2][1]); // "O" (linha 2, coluna 1)
```

---

## Percorrendo Matrizes com Laços Aninhados

Para visitar cada posição de uma matriz bidimensional, utiliza-se um laço `for` dentro de outro:

```javascript
const matriz = [
  [10, 20, 30],
  [40, 50, 60],
  [70, 80, 90]
];

for (let linha = 0; linha < matriz.length; linha++) {
  for (let coluna = 0; coluna < matriz[linha].length; coluna++) {
    console.log(`Posição [${linha}][${coluna}] = ${matriz[linha][coluna]}`);
  }
}
```
