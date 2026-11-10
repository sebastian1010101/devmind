# FE02-12 — Tipo String

## O que é uma String?

No JavaScript, uma **String** é uma sequência ordenada de caracteres utilizada para representar e manipular dados textuais. Cada caractere possui um índice numérico de posição iniciado em zero (`0`).

---

## Formas de Delimitar Strings

O JavaScript oferece três sintaxes para criar strings literais:

```javascript
// 1. Aspas Duplas
const sobrenome = "Silva";

// 2. Aspas Simples
const nome = 'Maria';

// 3. Crases (Template Literals / Template Strings) — Padrão Moderno
const apresentacao = `Meu nome é ${nome} ${sobrenome}`;
```

---

## O Poder dos Template Literals (Crases \`\`)

Introduzidos no ECMAScript 6, os Template Literals são a forma mais legível e poderosa de trabalhar com textos em JavaScript:

### 1. Interpolação de Expressões (`${...}`)

Elimina a necessidade de concatenar textos longos com múltiplos operadores `+`:

```javascript
const produto = "Monitor Ultrawide";
const preco = 1200;
const desconto = 150;

// Modo antigo cansativo (concatenação com +):
console.log("O " + produto + " custa R$" + (preco - desconto) + " na promoção.");

// Modo moderno com Template Literal (interpolação limpa):
console.log(`O ${produto} custa R$${preco - desconto} na promoção.`);
```

### 2. Suporte Nativo a Múltiplas Linhas

Com aspas tradicionais, quebrar linhas exigia caracteres de escape `\n`. Com crases, as quebras de linha são preservadas naturalmente no texto:

```javascript
const emailBoasVindas = `Olá, João!

Seja muito bem-vindo à nossa plataforma.
Seus estudos começam hoje!

Atenciosamente,
Equipe Kenzie.`;
```

---

## A Propriedade `.length` e Acesso por Índice

Toda string possui a propriedade `.length`, que retorna a quantidade exata de caracteres contida no texto:

```javascript
const linguagem = "JavaScript";

console.log(linguagem.length); // 10 caracteres
console.log(linguagem[0]);      // "J" (primeiro caractere no índice 0)
console.log(linguagem[4]);      // "S"
console.log(linguagem[linguagem.length - 1]); // "t" (último caractere dinâmico)
```
