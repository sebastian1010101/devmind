# FE02-08 — Variáveis

## O que é uma Variável?

Uma **variável** é um espaço reservado e rotulado na memória do computador destinado a armazenar temporariamente dados que podem ser lidos, utilizados ou atualizados durante a execução de um programa.

Pense em uma variável como uma caixa etiquetada: a etiqueta é o **nome da variável** (*identificador*) e o que está guardado dentro é o seu **valor**.

---

## Como Declarar Variáveis no JavaScript Moderno

No JavaScript moderno (padrão ES6+), utilizamos `let` e `const`. A declaração clássica `var` é considerada legada e deve ser evitada:

```javascript
// 1. const: valor constante que não pode ser reatribuído
const pi = 3.14159;
const nome = "Sebastián";

// 2. let: valor variável que pode mudar ao longo do programa
let idade = 25;
idade = 26; // Reatribuição permitida!
```

---

## Comparação entre `const`, `let` e `var`

| Palavra-Chave | Permite Reatribuição? | Permite Redeclaração? | Escopo |
| --- | --- | --- | --- |
| `const` | Não | Não | Bloco `{}` |
| `let` | Sim | Não | Bloco `{}` |
| `var` (Legado) | Sim | Sim (perigoso) | Função ou Global |

> **Regra de Ouro:** Por padrão, declare sempre tudo como `const`. Utilize `let` apenas quando você souber com certeza que aquele valor precisará mudar ao longo do código (ex: contadores em loops). Nunca use `var`.

---

## Tipos de Dados Primitivos Básicos

O JavaScript infere automaticamente o tipo de dado de acordo com o valor atribuído (*tipagem dinâmica*):

```javascript
// String (Textos delimitados por aspas duplas, simples ou crases)
const cidade = "Curitiba";

// Number (Inteiros e decimais de ponto flutuante)
const ano = 2026;
const temperatura = 23.5;

// Boolean (Valores lógicos binários)
const estaChovendo = false;
const matriculado = true;

// Undefined (Variável declarada, mas sem valor atribuído ainda)
let saldo;
console.log(saldo); // undefined

// Null (Ausência intencional e explícita de qualquer valor)
const resposta = null;
```

---

## Regras de Nomenclatura de Variáveis

- Utiliza-se a convenção **camelCase** (primeira palavra em minúscula e as seguintes com inicial maiúscula): `nomeCompleto`, `totalDePontos`.
- Não pode começar com números (ex: `1numero` é inválido; use `numero1`).
- Não pode conter hifens nem espaços.
- Não pode utilizar palavras reservadas da linguagem (ex: `let`, `class`, `function`).
