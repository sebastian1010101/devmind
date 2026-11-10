# FE02-15 — Operadores de Comparação

## O que são Operadores de Comparação?

Os **operadores de comparação** (também chamados de relacionais) comparam dois valores ou expressões e retornam obrigatoriamente um valor booleano: `true` (verdadeiro) ou `false` (falso).

Eles formam a base lógica para que o programa tome decisões e desvie caminhos em estruturas condicionais (`if/else`).

---

## Tabela de Operadores de Comparação

| Operador | Significado | Exemplo | Resultado |
| --- | --- | --- | --- |
| `===` | Igualdade Estrita (compara valor e tipo) | `5 === 5` | `true` |
| `!==` | Desigualdade Estrita (valor ou tipo diferente) | `5 !== "5"` | `true` |
| `>` | Maior que | `10 > 7` | `true` |
| `<` | Menor que | `3 < 2` | `false` |
| `>=` | Maior ou igual a | `10 >= 10` | `true` |
| `<=` | Menor ou igual a | `8 <= 5` | `false` |

---

## Igualdade Estrita (`===`) vs Igualdade Ampla (`==`)

Uma das fontes mais comuns de bugs em JavaScript iniciante é a diferença entre dois e três sinais de igual:

### 1. Igualdade Ampla (`==`) — Não Recomendada

Realiza **coerção implícita de tipos** antes de comparar. Se os tipos forem diferentes, o JavaScript tenta forçar a conversão de um para o outro:

```javascript
console.log(5 == "5");   // true (o JS converteu a string "5" em número!)
console.log(0 == false); // true
console.log("" == 0);    // true
```

### 2. Igualdade Estrita (`===`) — Padrão da Indústria

Compara o **valor** e o **tipo de dado** simultaneamente, sem realizar nenhuma conversão mágica:

```javascript
console.log(5 === "5");   // false (número !== string)
console.log(5 === 5);     // true
console.log(0 === false); // false
```

> **Regra de Ouro:** Utilize sempre `===` e `!==`. Nunca utilize `==` ou `!=` em projetos profissionais.
