# FE02-34 — Plataforma Codewars

## O que é o Codewars?

O **Codewars** é uma plataforma educacional interativa online amplamente utilizada no mercado global de programação e adotada na grade curricular da Kenzie Academy para desenvolver resolução de problemas e fluência em algoritmos.

No Codewars, os desafios são chamados de **Kata** (termo das artes marciais) e os níveis de dificuldade dos programadores são medidos em **Kyu** (do 8º Kyu mais fácil até o 1º Kyu mais avançado).

---

## O Formato dos Desafios (Katas)

Diferente de escrever programas que usam `prompt()` ou `alert()`, no Codewars todo desafio exige **escrever uma função pura com `return`**.

O sistema roda testes unitários automatizados enviando argumentos para a sua função e comparando o valor retornado com o resultado esperado.

```javascript
// Exemplo clássico no Codewars:
// "Crie uma função que receba um número inteiro e retorne 'Even' se for par ou 'Odd' se for ímpar."

function evenOrOdd(number) {
  if (number % 2 === 0) {
    return "Even";
  }
  return "Odd";
}
```

---

## Dicas Essenciais para Resolver Katas

1. **Leia os Testes de Exemplo (*Sample Tests*):** examine quais entradas serão passadas e qual formato exato de saída é esperado (atenção a maiúsculas, minúsculas e pontuações).
2. **Utilize `return`, nunca `console.log()` para o resultado:** o sistema só avalia o que é devolvido pelo `return`. O `console.log()` serve apenas para inspecionar variáveis enquanto você tenta descobrir a solução.
3. **Pressione `Test` antes de `Attempt`:** o botão *Test* roda os casos públicos de exemplo; o botão *Attempt* submete sua solução contra dezenas de casos de teste ocultos (incluindo números negativos, strings vazias e valores extremos).
4. **Analise as Soluções da Comunidade:** após resolver um Kata, examine as soluções de outros desenvolvedores para aprender novos métodos e abordagens idiomáticas da linguagem.
