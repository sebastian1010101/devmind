# FE02-26 — Escopos

## O que é Escopo?

**Escopo** é o contexto delimitado que determina a **visibilidade e a acessibilidade** de variáveis, funções e objetos em diferentes partes do código durante a execução do programa.

Uma variável só pode ser lida ou alterada onde o seu escopo permitir.

---

## Os Três Tipos de Escopo no JavaScript

```text
+-------------------------------------------------------------+
|  ESCOPO GLOBAL                                              |
|  const site = "kenzie.com.br";                              |
|                                                             |
|  +-------------------------------------------------------+  |
|  |  ESCOPO DE FUNÇÃO                                     |  |
|  |  function autenticar() {                              |  |
|  |    const token = "xyz123";                            |  |
|  |                                                       |  |
|  |    +-----------------------------------------------+  |  |
|  |    |  ESCOPO DE BLOCO                              |  |  |
|  |    |  if (true) {                                  |  |  |
|  |    |    const expiraEm = 3600;                     |  |  |
|  |    |  }                                            |  |  |
|  |    +-----------------------------------------------+  |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
```

---

## 1. Escopo Global

Variáveis declaradas fora de qualquer função ou bloco `{}` pertencem ao escopo global. Elas são acessíveis a partir de qualquer linha de código em todo o arquivo.

```javascript
const versaoApp = "1.0.0"; // Variável Global

function exibirVersao() {
  console.log(versaoApp); // Acessa com sucesso!
}
```

> **Atenção:** Evite poluir o escopo global com dezenas de variáveis para prevenir colisões de nomes e bugs imprevistos.

---

## 2. Escopo de Função (Local Scope)

Variáveis declaradas dentro do corpo de uma função só existem e só podem ser acessadas **dentro dessa própria função**:

```javascript
function calcularImposto() {
  const aliquota = 0.15; // Local da função
  return aliquota;
}

calcularImposto();
console.log(aliquota); // ReferenceError: aliquota is not defined!
```

---

## 3. Escopo de Bloco (Block Scope com `let` e `const`)

Qualquer estrutura delimitada por um par de chaves `{}` (como blocos de `if`, `else`, `for`, `while`) cria um escopo de bloco próprio para variáveis declaradas com `let` ou `const`:

```javascript
if (true) {
  const mensagemSecreta = "12345";
  let contador = 10;
}

console.log(mensagemSecreta); // ReferenceError!
```

*(Nota histórica: variáveis criadas com `var` ignoram o escopo de bloco e vazam para fora do `if` ou `for`, razão pela qual seu uso foi abolido).*

---

## Escopo Léxico e Cadeia de Escopos (Scope Chain)

O JavaScript utiliza **escopo léxico**: funções internas têm acesso às variáveis declaradas em seus escopos pais externos, mas o inverso nunca é verdadeiro (o pai nunca enxerga variáveis criadas dentro do filho).
