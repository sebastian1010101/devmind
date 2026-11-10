# FE02-20 — Introdução a Funções

## O que é uma Função?

Uma **função** é um bloco isolado e reutilizável de código projetado para executar uma tarefa ou cálculo específico. Ela só é executada quando é explicitamente invocada (*chamada*) pelo programa.

Sem funções, qualquer trecho de lógica precisaria ser copiado e colado repetidamente em vários lugares do arquivo, gerando código duplicado e de difícil manutenção.

---

## Os Três Pilares das Funções

1. **Reutilização de Código:** escreva a regra uma única vez e invoque-a dezenas ou centenas de vezes em pontos diferentes da aplicação.
2. **Modularização e Organização:** divide um problema grande e complexo em pequenas partes compreensíveis e fáceis de testar.
3. **Princípio DRY (*Don't Repeat Yourself*):** uma diretriz central da engenharia de software para evitar redundâncias no código-fonte.

---

## Anatomia Geral de uma Função

```javascript
// 1. Declaração da função
function saudarVisitante() {
  console.log("Olá! Seja muito bem-vindo ao curso de JavaScript da Kenzie!");
}

// 2. Invocação / Chamada da função
saudarVisitante();
saudarVisitante(); // Pode ser chamada quantas vezes forem necessárias
```

- A palavra-chave `function` informa ao interpretador que estamos definindo uma função.
- O nome da função (`saudarVisitante`) deve seguir a convenção **camelCase** e ser um verbo que descreve a ação.
- Os parênteses `()` contêm parâmetros opcionais.
- O corpo da função fica delimitado entre chaves `{}`.
