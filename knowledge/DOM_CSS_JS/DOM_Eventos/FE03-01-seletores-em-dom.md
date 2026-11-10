# FE03-01 — Seletores em DOM

## Métodos Modernos de Seleção de Elementos

Para alterar qualquer elemento da página, primeiro precisamos **selecioná-lo**. No desenvolvimento moderno, utilizamos prioritariamente a API de Seletores CSS:

---

## 1. `document.querySelector(seletorCSS)`

Retorna o **primeiro elemento** que corresponder ao seletor CSS informado (ou `null` caso não encontre nenhum):

```javascript
// Seleciona pela tag:
const titulo = document.querySelector("h1");

// Seleciona por classe (usa ponto .):
const primeiroCard = document.querySelector(".card");

// Seleciona por ID (usa cerquilha #):
const botaoSalvar = document.querySelector("#btn-salvar");

// Seleciona por seletor composto complexo:
const linkMenu = document.querySelector("nav.menu-principal ul > li a");
```

---

## 2. `document.querySelectorAll(seletorCSS)`

Retorna uma **NodeList** (coleção estática semelhante a um array) contendo **todos os elementos** que correspondem ao seletor CSS:

```javascript
const todosOsCards = document.querySelectorAll(".card");

console.log(`Total de cards encontrados: ${todosOsCards.length}`);

// É possível percorrer com forEach ou for...of:
todosOsCards.forEach((card, index) => {
  console.log(`Card ${index}:`, card);
});
```

---

## Métodos Legados Tradicionais

Métodos antigos que ainda existem no navegador para compatibilidade:

| Método Antigo | Como Funciona | Tipo de Retorno |
| --- | --- | --- |
| `document.getElementById("id")` | Busca por ID sem a `#` | Um único elemento HTML |
| `document.getElementsByClassName("classe")` | Busca por classe sem o `.` | HTMLCollection viva (*Live*) |
| `document.getElementsByTagName("tag")` | Busca por nome da tag | HTMLCollection viva (*Live*) |

> **Boas Práticas:** Prefira `querySelector` e `querySelectorAll`. Eles utilizam a mesma sintaxe flexível que você já domina no CSS e retornam coleções previsíveis.
