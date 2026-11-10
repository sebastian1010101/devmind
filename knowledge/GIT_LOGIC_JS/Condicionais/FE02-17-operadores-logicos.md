# FE02-17 — Operadores Lógicos

## O que são Operadores Lógicos?

Os **operadores lógicos** permitem combinar duas ou mais expressões booleanas ou inverter o valor lógico de uma condição.

Eles são a base para construir regras de negócio refinadas (ex: *"usuário logado E com assinatura ativa"*).

---

## Os Três Operadores Fundamentais

| Operador | Nome Lógico | Significado | Exemplo |
| --- | --- | --- | --- |
| `&&` | E Lógico (AND) | Retorna `true` **apenas se todas** as condições forem verdadeiras | `true && true` &rarr; `true` |
| `\|\|` | OU Lógico (OR) | Retorna `true` **se pelo menos uma** das condições for verdadeira | `true \|\| false` &rarr; `true` |
| `!` | NÃO Lógico (NOT) | Inverte o valor booleano (`true` vira `false`, e vice-versa) | `!false` &rarr; `true` |

---

## 1. O Operador AND (`&&`)

Exige que ambas as partes sejam verdadeiras:

```javascript
const usuarioLogado = true;
const possuiAssinaturaAtiva = true;

if (usuarioLogado && possuiAssinaturaAtiva) {
  console.log("Reproduzir vídeo em alta resolução.");
} else {
  console.log("Faça login e assine um plano para assistir.");
}
```

---

## 2. O Operador OR (`||`)

Basta uma única condição ser verdadeira para o bloco executar:

```javascript
const ehEstudante = false;
const temMaisDe60Anos = true;

// Meia-entrada concedida para estudantes OU idosos
if (ehEstudante || temMaisDe60Anos) {
  console.log("Direito a 50% de desconto no ingresso.");
} else {
  console.log("Valor integral do ingresso.");
}
```

---

## 3. O Operador NOT (`!`)

Inverte a lógica:

```javascript
const formularioPreenchido = false;

if (!formularioPreenchido) {
  console.log("Por favor, preencha todos os campos obrigatórios.");
}
```

---

## Valores Falsy e Truthy

No JavaScript, todo valor em um contexto condicional pode ser avaliado como equivalente a falso (*Falsy*) ou verdadeiro (*Truthy*).

### Os 6 Valores Falsy Únicos do JavaScript

1. `false`
2. `0` (e `-0`)
3. `""` (string vazia)
4. `null`
5. `undefined`
6. `NaN` (Not a Number)

*Todos os outros valores existentes na linguagem (inclusive strings com texto `"abc"`, números diferentes de zero `42`, arrays `[]` e objetos `{}`) são **Truthy**.*
