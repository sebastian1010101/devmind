# FE02-07 — Introdução ao JavaScript

## O que é JavaScript?

**JavaScript** (frequentemente abreviado como **JS**) é uma linguagem de programação de alto nível, interpretada, multiparadigma, dinamicamente tipada e com suporte a funções de primeira classe.

Criada originalmente por Brendan Eich em 1995 para a Netscape com a finalidade de adicionar scripts interativos leves a páginas web, o JavaScript evoluiu para se tornar a **linguagem oficial e universal da web**, padronizada sob a especificação **ECMAScript (ES)**.

---

## Onde o JavaScript Executa?

- **No Navegador (Client-Side):** todos os navegadores modernos possuem um motor (*engine*) integrado de JavaScript (ex: **V8** no Chrome e Edge, **SpiderMonkey** no Firefox, **JavaScriptCore** no Safari). Ele manipula a página (DOM), reage a cliques do usuário e consome APIs externas.
- **No Servidor (Server-Side):** através de ambientes de execução como **Node.js**, Deno e Bun, permitindo criar servidores backend, rotas de API, automações e acessar bancos de dados usando a mesma linguagem.

---

## Como Incluir JavaScript no HTML

### 1. Script Externo (Recomendado)

O código JS fica isolado em um arquivo próprio com extensão `.js` (ex: `script.js`) e é importado no HTML via tag `<script>` com atributo `src`:

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <title>Minha Aplicação</title>
  </head>
  <body>
    <h1>Olá!</h1>

    <!-- Importado preferencialmente no final do body -->
    <script src="script.js"></script>
  </body>
</html>
```

### 2. Script Interno

Escrito diretamente entre as tags `<script>` e `</script>` dentro do documento HTML:

```html
<script>
  console.log("Olá diretamente do JavaScript interno!");
</script>
```

---

## A Ferramenta de Saída Universal: `console.log()`

O `console.log()` é o comando mais utilizado para imprimir mensagens, valores e dados inspecionáveis no painel de ferramentas do desenvolvedor (*DevTools > Console*):

```javascript
console.log("Olá, mundo! Meu primeiro código em JS.");
console.log(2026);
```
