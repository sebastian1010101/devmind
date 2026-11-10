# FE03-51 — Método forEach

## O que é

`forEach` executa uma função callback **uma vez para cada elemento** do array. É a substituição direta do laço `for` quando o objetivo é apenas *fazer algo* com cada item — sem transformar, sem filtrar, sem acumular.

```javascript
const frutas = ["maçã", "banana", "uva"];

frutas.forEach(function(fruta) {
  console.log(fruta);
});
// maçã
// banana
// uva
```

## Sintaxe completa

```javascript
array.forEach((elemento, indice, arrayOriginal) => {
  // corpo da callback
});
```

- **elemento** — o item atual da iteração
- **indice** — posição do item (opcional)
- **arrayOriginal** — o array sendo percorrido (raramente usado)

```javascript
const letras = ["a", "b", "c"];

letras.forEach((letra, i) => {
  console.log(`Posição ${i}: ${letra}`);
});
// Posição 0: a
// Posição 1: b
// Posição 2: c
```

## O retorno: sempre `undefined`

`forEach` **não retorna nada útil**. Ele existe apenas para produzir *efeitos colaterais* — exibir, salvar, modificar algo externo:

```javascript
const numeros = [1, 2, 3];

const resultado = numeros.forEach(n => n * 2);

console.log(resultado); // undefined — o forEach não devolve o dobro!
```

Se você precisa de um **novo array** com os valores transformados, o método certo é `map`, não `forEach`. Esse é o erro mais comum de quem está aprendendo.

## Quando usar

- Renderizar elementos no DOM
- Executar efeitos colaterais (logs, chamadas, salvamentos)
- Somar/acumular em variáveis externas (embora `reduce` seja mais idiomático)

### Exemplo com DOM

```javascript
const itens = ["Estudar JS", "Fazer exercícios", "Revisar código"];
const lista = document.querySelector("#lista-tarefas");

itens.forEach(tarefa => {
  const li = document.createElement("li");
  li.innerText = tarefa;
  lista.appendChild(li);
});
```

### Acumulando em variável externa

```javascript
const precos = [10, 20, 30];
let total = 0;

precos.forEach(preco => {
  total += preco;
});

console.log(total); // 60
```

## Limitações importantes

### Não existe `break` nem `continue`

O `forEach` percorre **todos** os elementos — não há como interromper o laço no meio (fora lançar uma exceção, o que é uma péssima prática). Se você precisa parar ao encontrar algo, use `for...of`, `find` ou `some`.

```javascript
// ❌ Não funciona — forEach ignora break
numeros.forEach(n => {
  if (n === 2) break; // SyntaxError!
});
```

### Não funciona com `async/await` como esperado

```javascript
// ❌ As promises não são aguardadas em sequência
urls.forEach(async url => {
  await fetch(url); // todas disparam em paralelo, forEach não espera
});

// ✅ Para esperar cada uma, use for...of
for (const url of urls) {
  await fetch(url);
}
```

## forEach vs map vs for...of

| Característica | `forEach` | `map` | `for...of` |
| --- | --- | --- | --- |
| Retorna novo array | Não | Sim | Não |
| Pode interromper | Não | Não | Sim (`break`) |
| Suporta `await` sequencial | Não | Não | Sim |
| Uso típico | Efeitos colaterais | Transformação | Controle de fluxo |

Regra prática: precisa do resultado como array? `map`. Precisa parar no meio ou usar `await`? `for...of`. Só precisa executar algo para cada item? `forEach`.
