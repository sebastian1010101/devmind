# FE03-61 — Spread Operator

## O que é

O operador `...` (três pontos) **espalha** os elementos de um iterável ou as propriedades de um objeto no lugar onde é usado. É o oposto da desestruturação: em vez de *extrair*, ele *expande*.

```javascript
const numeros = [1, 2, 3];
console.log(...numeros); // equivale a console.log(1, 2, 3)
```

## Spread em arrays

### Copiar um array

```javascript
const original = [1, 2, 3];
const copia = [...original];

copia.push(4);
console.log(original); // [1, 2, 3] — não foi afetado
console.log(copia);    // [1, 2, 3, 4]
```

Diferente de `const copia = original` — que cria apenas uma **referência** ao mesmo array:

```javascript
const referencia = original;
referencia.push(4);
console.log(original); // [1, 2, 3, 4] — o original mudou!
```

### Concatenar arrays

```javascript
const a = [1, 2];
const b = [3, 4];

const juntos = [...a, ...b]; // [1, 2, 3, 4]
// Substitui a.concat(b)
```

### Inserir no meio

```javascript
const meio = [1, 4];
const completo = [...meio.slice(0, 1), 2, 3, ...meio.slice(1)];
// ou mais simples:
const outro = [1, ...[2, 3], 4];
```

### Passar array como argumentos

```javascript
const numeros = [5, 12, 3, 8];

Math.max(...numeros); // 12 — espalha como Math.max(5, 12, 3, 8)
// Antes: Math.max.apply(null, numeros)
```

## Spread em objetos

### Copiar e estender objetos

```javascript
const usuario = { nome: "Ana", idade: 28 };

const copia = { ...usuario };                    // cópia rasa
const atualizado = { ...usuario, idade: 29 };    // cópia + sobrescrita
const completo = { ...usuario, cidade: "SP" };   // cópia + nova propriedade
```

### Mesclar objetos — a direita vence

```javascript
const padrao = { tema: "claro", fonte: 16 };
const custom = { tema: "escuro" };

const config = { ...padrao, ...custom };
// { tema: "escuro", fonte: 16 } — 'tema' de custom sobrescreve
```

A ordem importa: propriedades à **direita** sobrescrevem as da esquerda.

## A pegadinha da cópia rasa (shallow copy)

Spread copia apenas o **primeiro nível**. Objetos e arrays aninhados continuam sendo referências:

```javascript
const pessoa = { nome: "Ana", endereco: { cidade: "SP" } };
const copia = { ...pessoa };

copia.endereco.cidade = "RJ";
console.log(pessoa.endereco.cidade); // "RJ" — o original mudou!
```

Para cópia profunda, use `structuredClone` ou JSON:

```javascript
const profunda = structuredClone(pessoa);       // nativo e completo
const viaJson = JSON.parse(JSON.stringify(pessoa)); // perde functions/dates
```

## Spread vs Rest — mesmo símbolo, papéis opostos

| Contexto | Nome | Função |
| --- | --- | --- |
| `f(...array)` | Spread | **Expande** o array em argumentos |
| `[...a, ...b]` | Spread | **Expande** elementos no novo array |
| `{...obj}` | Spread | **Espalha** propriedades no novo objeto |
| `function f(...args)` | Rest | **Agrupa** argumentos num array |
| `const [a, ...resto]` | Rest | **Agrupa** o que sobrou |

Regra: `...` **do lado direito** do `=` espalha (spread); **do lado esquerdo** ou em parâmetros agrupa (rest).

```javascript
// Rest — agrupa
function somar(...numeros) {
  return numeros.reduce((a, n) => a + n, 0);
}
somar(1, 2, 3); // numeros = [1, 2, 3]

// Spread — espalha
const nums = [1, 2, 3];
somar(...nums); // equivale a somar(1, 2, 3)
```

## Casos de uso profissionais

### Estado imutável (React)

```javascript
// Adicionar item sem mutar
setLista([...lista, novoItem]);

// Atualizar objeto sem mutar
setUsuario({ ...usuario, nome: "Novo Nome" });
```

### Converter iteráveis em array

```javascript
const array = [...document.querySelectorAll("li")]; // NodeList → Array
const unicos = [...new Set([1, 1, 2, 2, 3])];       // Set → [1, 2, 3]
const caracteres = [..."abc"];                       // "abc" → ["a","b","c"]
```

### Argumentos de função variáveis

```javascript
function criarUsuario(nome, ...dadosExtras) {
  return { nome, ...dadosExtras };
}
criarUsuario("Ana", { idade: 28 }, { cidade: "SP" });
```

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `[...obj]` em objeto | `TypeError` — objetos não são iteráveis; use `{...obj}` ou `Object.entries` |
| Spread em `null`/`undefined` em array | `TypeError` — proteja com `[...(lista \|\| [])]` |
| Copiar objeto aninhado com `...` | Só o 1º nível é novo — aninhados compartilham referência |
| `const copia = original` | Não é cópia — é a mesma referência |
