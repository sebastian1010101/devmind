# DM01-06 — Atualizar listas no estado do React

## Adicionar ou atualizar sem mutar

Uma lista armazenada no estado deve ser tratada como somente leitura. Para adicionar um item, chame o setter com uma função que recebe o estado anterior e retorna uma nova lista, como `setItems(previous => [...previous, item])`. Assim atualizações enfileiradas usam o estado anterior correspondente.

Para alterar um objeto dentro da lista, use `map` e copie o objeto alterado. Copiar apenas o array deixa os objetos internos compartilhados.

```js
setItems(previous =>
  previous.map(item => item.id === selectedId ? { ...item, done: true } : item)
);
```

Referência [React — Updating Arrays in State](https://react.dev/learn/updating-arrays-in-state).
