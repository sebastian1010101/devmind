# FE03-46 — Template Literals e Operador Ternário

## 1. Template Literals (Template Strings)

As Template Literals utilizam caracteres de crase (\`\`) e revolucionaram a manipulação textual no JavaScript moderno:

### Interpolação de Expressões e Cálculos Dinâmicos:

Dentro de `${...}`, você pode executar qualquer expressão válida de JavaScript, desde variáveis simples até chamadas de métodos, operações matemáticas e operadores ternários:

```javascript
const usuario = "Carlos";
const pontos = 450;

console.log(`O jogador ${usuario} está no nível ${pontos > 300 ? "Avançado" : "Iniciante"}.`);
```

### Preservação Nativa de Quebras de Linha e HTML Multilinha:

```javascript
const cardHtml = `
  <article class="card">
    <h3>${usuario}</h3>
    <p>Pontuação: <strong>${pontos}</strong></p>
  </article>
`;
```

---

## 2. O Operador Ternário (`condicao ? expr1 : expr2`)

O operador ternário é o único operador do JavaScript que recebe três operandos. Ele funciona como uma expressão compacta de tomada de decisão que **retorna um valor diretamente**:

```javascript
const idade = 20;

// Sintaxe: condicao ? valorSeTrue : valorSeFalse
const categoria = idade >= 18 ? "Adulto" : "Menor";
```

### Por que Ele é Tão Utilizado no ES6 e em Frameworks como React?
Diferente de um bloco `if (...) { ... }` convencional (que é uma *declaração/statement* e não pode ser atribuído a variáveis), o operador ternário é uma **expressão** (*expression*):

```javascript
// Atribuição direta e elegante em uma linha:
const statusConexao = estaConectado ? "Online" : "Offline";

// Uso direto dentro de Template Literals:
console.log(`Status do servidor: ${ativo ? "Ativo" : "Em Manutenção"}`);
```
