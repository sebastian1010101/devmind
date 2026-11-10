# FE03-48 — Default Parameters

## O Problema dos Parâmetros Ausentes no JavaScript Legado

No JavaScript antes do ES6, quando um argumento não era enviado pelo chamador da função, seu parâmetro assumia o valor `undefined`. Para contornar isso, os desenvolvedores precisavam escrever checagens manuais verbosas:

```javascript
// Modo antigo cansativo antes do ES6:
function calcularFreteAntigo(peso, taxa) {
  taxa = (typeof taxa !== "undefined") ? taxa : 10.0;
  return peso * taxa;
}
```

---

## A Solução Elegante do ES6: Default Parameters

No ES6+, você pode definir valores padrão diretamente na lista de parâmetros com o operador `=`:

```javascript
function calcularFrete(peso, taxa = 10.0) {
  return peso * taxa;
}

console.log(calcularFrete(5, 15.0)); // 75 (usou o valor enviado: 15.0)
console.log(calcularFrete(5));       // 50 (usou o valor padrão: 10.0)
```

---

## Comportamento com `undefined` vs `null`

Um detalhe importante de comportamento: o valor padrão só é ativado se o argumento for **omitido** ou explicitamente passado como **`undefined`**. O valor `null` é considerado um valor válido preenchido e não dispara o default:

```javascript
function saudar(nome = "Visitante") {
  console.log(`Olá, ${nome}!`);
}

saudar();          // "Olá, Visitante!" (ativou default)
saudar(undefined); // "Olá, Visitante!" (ativou default)
saudar(null);      // "Olá, null!" (não ativou default!)
```

---

## Expressões e Outros Parâmetros como Default

O valor padrão pode ser o resultado de uma expressão matemática, chamada de outra função ou até mesmo o valor de um parâmetro anterior:

```javascript
function criarDimensao(largura, altura = largura) {
  // Se a altura não for enviada, assume a mesma medida da largura (quadrado perfeito)
  return { largura, altura, area: largura * altura };
}

console.log(criarDimensao(10)); // { largura: 10, altura: 10, area: 100 }
```
