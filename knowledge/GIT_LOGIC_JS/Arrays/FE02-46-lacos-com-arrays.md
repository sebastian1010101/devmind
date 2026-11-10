# FE02-46 — Laços com Arrays

## Percorrendo Arrays com Estruturas de Repetição

A combinação de laços de repetição com arrays é um dos pilares mais frequentes no desenvolvimento de software: percorrer listas de produtos, renderizar mensagens de chat ou somar notas de avaliações.

---

## 1. O Laço `for` Tradicional com Índices

A abordagem clássica conecta o contador `i` do loop aos índices do array (indo de `0` até `array.length - 1`):

```javascript
const frutas = ["Maçã", "Banana", "Morango", "Uva"];

for (let i = 0; i < frutas.length; i++) {
  console.log(`Índice ${i}: ${frutas[i]}`);
}
```

- **Vantagem:** permite controle absoluto sobre o índice, possibilitando saltos, contagens regressivas ou alteração do elemento em sua posição original (`frutas[i] = ...`).

---

## 2. O Laço Moderno `for...of` (ES6+)

Quando você precisa apenas ler o valor de cada elemento do array sequencialmente, sem se preocupar com os números dos índices:

```javascript
const tecnologias = ["Git", "HTML", "CSS", "JavaScript"];

for (const tech of tecnologias) {
  console.log(`Estudando: ${tech}`);
}
```

- **Vantagem:** sintaxe muito mais limpa, legível e livre de erros de índice (*off-by-one errors*).

---

## 3. O Método `.forEach()`

Um método funcional nativo de arrays que recebe uma função de retorno (*callback*) executada para cada item:

```javascript
const precos = [100, 250, 400];

precos.forEach((preco, indice) => {
  console.log(`Produto ${indice + 1} custa R$ ${preco}`);
});
```

---

## Padrão Comum: Acumulação e Busca em Laços

```javascript
const notas = [8.5, 7.0, 9.5, 6.0];
let somaTotal = 0;

for (const nota of notas) {
  somaTotal += nota;
}

const media = somaTotal / notas.length;
console.log(`Média final da turma: ${media.toFixed(2)}`); // 7.75
```
