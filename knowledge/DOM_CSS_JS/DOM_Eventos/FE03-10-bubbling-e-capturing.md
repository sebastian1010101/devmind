# FE03-10 — Bubbling e Capturing

## As Fases de Propagação de Eventos no DOM

Quando um evento acontece em um elemento que está aninhado dentro de outros elementos (por exemplo, um `<button>` dentro de uma `<section>` dentro do `<body>`), o evento não atinge apenas o botão: ele viaja por toda a árvore do DOM em **três fases consecutivas**:

```text
               1. CAPTURING PHASE (Descida da raiz até o alvo)
               DOCUMENT
                  ↓
                BODY
                  ↓
               SECTION
                  ↓
               BUTTON  <-- 2. TARGET PHASE (O elemento alvo que sofreu o clique)
                  ↑
               SECTION
                  ↑
                BODY
                  ↑
               DOCUMENT
               3. BUBBLING PHASE (Subida borbulhante do alvo até a raiz)
```

---

## 1. Event Bubbling (Borbulhamento — Comportamento Padrão)

Na fase de **Bubbling**, o evento dispara primeiro no elemento mais interno que recebeu o clique (o *Target*) e depois **"borbulha" subindo de pai em pai** até o topo do documento.

Todos os ouvintes registrados nos elementos ancestrais serão acionados em cascata a menos que o fluxo seja interrompido.

---

## Interrompendo o Borbulhamento: `event.stopPropagation()`

Caso você queira que um clique em um botão interno **não dispare** os eventos do cartão pai ou da página que o envolve:

```javascript
const botaoInterno = document.querySelector(".btn-favorito");

botaoInterno.addEventListener("click", (event) => {
  // Impede que o clique suba para o card pai:
  event.stopPropagation();
  console.log("Item favoritado com sucesso!");
});
```

---

## Padrão Poderoso: Delegação de Eventos (Event Delegation)

Aproveitando o borbulhamento natural dos eventos, em vez de registrar um ouvinte para cada um de centenas de botões de uma lista, registramos **um único ouvinte no elemento pai**:

```javascript
const listaContainer = document.querySelector("#lista-produtos");

listaContainer.addEventListener("click", (event) => {
  // event.target identifica exatamente qual elemento foi tocado:
  if (event.target.classList.contains("btn-excluir")) {
    const itemLi = event.target.closest("li");
    itemLi.remove();
    console.log("Item excluído com sucesso via delegação!");
  }
});
```

- **Vantagem:** consome muito menos memória e funciona automaticamente até para novos itens que forem inseridos no DOM dinamicamente no futuro.
