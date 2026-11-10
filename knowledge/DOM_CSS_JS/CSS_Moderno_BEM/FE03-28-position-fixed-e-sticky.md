# FE03-28 — Position: Fixed e Sticky

## 1. `position: fixed` (Fixação Absoluta na Viewport)

O elemento é completamente removido do fluxo normal e ancorado diretamente nas coordenadas da **janela visível do navegador** (*viewport*). Ele permanece imóvel exatamente no mesmo lugar da tela mesmo quando o usuário rola a página:

```css
/* Cabeçalho fixo no topo permanente */
.header-fixo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  background-color: #0f172a;
  z-index: 1000; /* Garante que fique na frente do restante do conteúdo */
}

/* Compensação obrigatória no body para o conteúdo não sumir atrás do header */
body {
  padding-top: 70px;
}
```

### Casos de Uso Comuns:
- Barras de navegação superiores fixas.
- Botões flutuantes de WhatsApp ou chat no canto inferior direito (`bottom: 20px; right: 20px;`).
- Modais e telas de sobreposição escurecida (*overlay*).

---

## 2. `position: sticky` (Fixação Híbrida Inteligente)

O elemento se comporta como `position: relative` no início, rolando naturalmente junto com a página. No entanto, no momento em que a rolagem atinge a distância definida na propriedade de offset (ex: `top: 0` ou `top: 20px`), ele passa a se comportar como `fixed` (*grudando* na tela) enquanto o seu container pai estiver visível.

```css
.tabela__cabecalho-sticky {
  position: sticky;
  top: 0;
  background-color: #f8fafc;
  z-index: 10;
}
```

### Regras para o `position: sticky` Funcionar:
- É **obrigatório declarar pelo menos uma propriedade direcional** (geralmente `top: 0`).
- Nenhum elemento pai pode ter a propriedade `overflow: hidden`, `overflow: auto` ou `overflow: scroll`, caso contrário a rolagem do sticky é desativada pelo navegador.
