# FE03-11 — Propriedades do Objeto Evento

## O Objeto `event` (ou `e`)

Sempre que um evento é disparado, o navegador cria e passa automaticamente um **objeto de evento** contendo todos os detalhes técnicos da ação como o primeiro argumento da função de callback:

```javascript
elemento.addEventListener("click", (event) => {
  console.log(event);
});
```

---

## Principais Propriedades do Objeto Evento

### 1. `event.target` vs `event.currentTarget`

- **`event.target`:** o elemento mais profundo e específico que **originou o evento** (onde o clique físico realmente aconteceu).
- **`event.currentTarget`:** o elemento que **está ouvindo o evento** (onde o `addEventListener` foi registrado).

### 2. Propriedades de Eventos de Teclado (`keydown`, `keyup`)

- **`event.key`:** o nome do caractere da tecla pressionada (ex: `"Enter"`, `"Escape"`, `"a"`, `"ArrowUp"`).
- **`event.code`:** o código físico da tecla no teclado (ex: `"KeyA"`, `"Digit1"`).

```javascript
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    console.log("Tecla ESC pressionada: fechar modal!");
  }
});
```

### 3. Propriedades de Eventos de Mouse (`click`, `mousemove`)

- **`event.clientX` / `event.clientY`:** coordenadas X e Y do cursor do mouse em relação à área visível da janela (*viewport*).
- **`event.pageX` / `event.pageY`:** coordenadas em relação ao documento inteiro (incluindo a rolagem).
- **`event.button`:** qual botão do mouse foi clicado (0 = esquerdo, 1 = meio/scroll, 2 = direito).
