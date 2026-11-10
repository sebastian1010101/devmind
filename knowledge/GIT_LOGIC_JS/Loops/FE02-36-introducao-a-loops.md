# FE02-36 — Introdução a Loops

## O que é um Loop (Laço de Repetição)?

Um **loop** (laço ou estrutura de repetição) é um recurso de linguagens de programação que permite **executar o mesmo bloco de código repetidas vezes**, de forma automatizada, enquanto uma determinada condição permanecer verdadeira.

Sem laços de repetição, para imprimir os números de 1 a 1000 você precisaria digitar manualmente mil linhas de `console.log()`. Com um loop, isso é resolvido em apenas três linhas de código.

---

## Os Três Elementos Fundamentais de Qualquer Loop

Para que um laço de repetição funcione de forma controlada e segura, três componentes são indispensáveis:

1. **Inicialização:** o estado ou valor de partida do contador (ex: `let contador = 1;`).
2. **Condição de Continuação:** a expressão lógica testada a cada iteração; se for `true`, o loop continua; se virar `false`, o loop é encerrado (ex: `contador <= 1000;`).
3. **Passo / Incremento:** a modificação do contador ao final de cada volta, garantindo que ele caminhe em direção ao encerramento (ex: `contador++;`).

---

## O Risco Crítico: Loop Infinito

Um **loop infinito** ocorre quando a condição de parada nunca se torna falsa (geralmente por esquecimento de incrementar o contador ou por uma lógica com condição sempre verdadeira).

```javascript
// CUIDADO: Loop infinito (trava o navegador ou o processo Node.js!)
let i = 1;

while (i <= 5) {
  console.log(i);
  // Faltou o 'i++', o valor de 'i' nunca muda e fica preso no 1 para sempre!
}
```

Caso isso ocorra no navegador, a aba congelará consumindo 100% de uso de CPU, exigindo forçar o encerramento do processo.

---

## Principais Estruturas no JavaScript

- **`for` tradicional:** ideal quando você sabe previamente quantas iterações exatas devem ocorrer (ex: percorrer um intervalo de 1 a 50 ou o tamanho de uma lista).
- **`while`:** ideal quando o número de repetições é imprevisível e depende de um evento ou condição externa (ex: *"repita enquanto o usuário não digitar 'sair'"*).
