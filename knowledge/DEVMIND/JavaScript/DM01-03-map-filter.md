# DM01-03 — Transformar e selecionar itens com JavaScript

## Escolher entre map e filter

Use `map` quando cada item precisa se transformar em outro valor, como trocar produtos pelos respectivos nomes. Use `filter` quando precisa selecionar os itens que passam em um teste. Ambos retornam outro array, mas uma função de callback ainda pode causar efeitos colaterais. Mantenha a callback pura quando possível.

```js
const products = [{ name: "Café", available: true }, { name: "Chá", available: false }];
const labels = products.filter(product => product.available).map(product => product.name);
// ["Café"]
```

Referência [ECMAScript Indexed Collections](https://tc39.es/ecma262/multipage/indexed-collections.html#sec-array.prototype.map).
