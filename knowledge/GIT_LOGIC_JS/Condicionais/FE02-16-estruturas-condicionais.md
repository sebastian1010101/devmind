# FE02-16 — Estruturas Condicionais

## O que são Estruturas Condicionais?

Estruturas condicionais permitem que o código tome **caminhos alternativos de execução** com base na avaliação de expressões lógicas (verdadeiro ou falso).

---

## 1. A Estrutura Básica: `if` e `else`

```javascript
const idade = 18;

if (idade >= 18) {
  console.log("Acesso autorizado: maior de idade.");
} else {
  console.log("Acesso bloqueado: menor de idade.");
}
```

- **`if (condicao)`:** executa o bloco interno entre chaves `{}` apenas se a condição for avaliada como `true`.
- **`else`:** bloco opcional executado quando a condição do `if` resultar em `false`.

---

## 2. Múltiplas Condições com `else if`

Quando existem mais de dois cenários possíveis:

```javascript
const nota = 8.5;

if (nota >= 9.0) {
  console.log("Excelente! Conceito A.");
} else if (nota >= 7.0) {
  console.log("Bom desempenho! Conceito B.");
} else if (nota >= 5.0) {
  console.log("Atenção! Conceito C (Recuperação).");
} else {
  console.log("Reprovado! Conceito D.");
}
```

- O motor do JavaScript avalia as condições de cima para baixo em sequência. Assim que a primeira condição verdadeira for encontrada, o respectivo bloco é executado e todas as seguintes são ignoradas.

---

## 3. Operador Ternário (`condicao ? valor1 : valor2`)

Uma forma compacta e elegante para expressar um `if/else` simples de uma única linha:

```javascript
const velocidade = 90;
const limite = 80;

// Sintaxe: condicao ? retornoSeVerdadeiro : retornoSeFalso
const statusTransito = velocidade > limite ? "Multado por excesso" : "Velocidade permitida";

console.log(statusTransito);
```

---

## 4. Estrutura de Escolha: `switch / case`

Indicada quando uma única variável precisa ser comparada pontualmente contra uma lista de múltiplos valores fixos:

```javascript
const plano = "premium";

switch (plano) {
  case "basico":
    console.log("Acesso a 1 tela em HD.");
    break;
  case "padrao":
    console.log("Acesso a 2 telas em Full HD.");
    break;
  case "premium":
    console.log("Acesso a 4 telas simultâneas em 4K Ultra HD.");
    break;
  default:
    console.log("Plano inválido ou não selecionado.");
}
```

- A palavra-chave `break` é obrigatória ao final de cada bloco `case` para impedir que a execução continue caindo nos casos seguintes (*fall-through*).
