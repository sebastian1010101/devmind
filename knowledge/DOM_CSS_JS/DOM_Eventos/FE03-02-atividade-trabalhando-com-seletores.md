# FE03-02 — Atividade: Trabalhando com Seletores

## Objetivo da Atividade

Praticar a captura de elementos no DOM utilizando `querySelector` e `querySelectorAll`, lendo e alterando conteúdos com as propriedades `.innerText` e `.innerHTML`.

---

## `.innerText` vs `.innerHTML`

- **`.innerText`:** lê ou atribui **texto puro e visível**. Qualquer caractere HTML inserido será tratado literalmente como texto seguro (sem renderizar tags).
- **`.innerHTML`:** lê ou atribui **marcação HTML completa**. Permite criar e injetar novas tags dentro do elemento, mas deve ser usado com cautela contra vulnerabilidades de injeção (*XSS*).

---

## Enunciado do Desafio

Dada uma página com um título principal (`#titulo-boas-vindas`), um parágrafo descritivo (`.descricao`) e uma lista de notificações (`ul.notificacoes`):

1. Selecione o título pelo seu ID e altere seu texto para `"Painel de Controle — Kenzie"`.
2. Selecione o parágrafo pela classe e altere sua cor de texto diretamente via `.style.color = "#2563eb"`.
3. Selecione todos os itens da lista de notificações (`li`) e exiba a quantidade total encontrada no console.
4. Adicione um novo item na lista de notificações utilizando `.innerHTML`.

---

## Solução de Referência

```javascript
// 1. Seleção por ID e alteração de texto puro
const tituloPrincipal = document.querySelector("#titulo-boas-vindas");
if (tituloPrincipal) {
  tituloPrincipal.innerText = "Painel de Controle — Kenzie";
}

// 2. Seleção por classe e alteração de estilo inline
const descricaoParagrafo = document.querySelector(".descricao");
if (descricaoParagrafo) {
  descricaoParagrafo.style.color = "#2563eb";
  descricaoParagrafo.style.fontWeight = "600";
}

// 3. Seleção de múltiplos elementos
const listaNotificacoes = document.querySelectorAll("ul.notificacoes li");
console.log(`Total de notificações registradas: ${listaNotificacoes.length}`);

// 4. Injeção de marcação HTML
const containerLista = document.querySelector("ul.notificacoes");
if (containerLista) {
  containerLista.innerHTML += `
    <li class="item-urgente">
      <strong>[URGENTE]</strong> Novo relatório disponível para download.
    </li>
  `;
}
```
