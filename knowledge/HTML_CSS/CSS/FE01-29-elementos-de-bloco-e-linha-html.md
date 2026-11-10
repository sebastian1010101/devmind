# FE01-29 — Elementos de Bloco e Linha (HTML)

## Comportamento Visual Padrão no Fluxo do Documento

Todo elemento HTML possui um valor padrão de comportamento de exibição no fluxo normal da página: **nível de bloco** (*block-level*) ou **em linha** (*inline*).

---

## 1. Elementos de Bloco (`display: block`)

### Características Principais:
- Iniciam obrigatoriamente em uma **nova linha**.
- Ocupam **100% da largura** disponível do elemento pai por padrão (a menos que uma largura específica seja definida).
- Aceitam configuração completa de dimensões: `width`, `height`, `margin` e `padding` em todas as quatro direções.

### Exemplos Comuns de Tags de Bloco:
- `<div>`, `<p>`, `<h1>` até `<h6>`
- `<ul>`, `<ol>`, `<li>`
- `<header>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- `<form>`

---

## 2. Elementos em Linha (`display: inline`)

### Características Principais:
- Não quebram linha; posicionam-se lado a lado horizontalmente com o conteúdo vizinho.
- Ocupam apenas a **largura estritamente necessária** para envolver o seu próprio conteúdo.
- **Não aceitam propriedades `width` e `height`** (o navegador ignora essas declarações).
- Margens e preenchimentos verticais (`margin-top`, `margin-bottom`) não empurram os elementos vizinhos para cima ou para baixo.

### Exemplos Comuns de Tags Inline:
- `<span>`, `<a>`, `<strong>`, `<em>`
- `<code>`, `<mark>`, `<small>`

---

## 3. Elemento em Linha com Bloco (`display: inline-block`)

Combina o melhor dos dois mundos:
- Fica na mesma linha que os elementos vizinhos (comportamento de elemento inline).
- Permite definir `width`, `height`, `margin` e `padding` verticais com precisão (comportamento de elemento de bloco).
- Muito utilizado para botões personalizados, chips de tags e ícones dimensionáveis.

---

## Tabela Comparativa de Comportamento

| Propriedade / Ação | Block | Inline | Inline-Block |
| --- | --- | --- | --- |
| Inicia em nova linha? | Sim | Não | Não |
| Ocupa 100% da largura por padrão? | Sim | Não | Não |
| Respeita `width` e `height`? | Sim | Não | Sim |
| Respeita margens verticais? | Sim | Não | Sim |
