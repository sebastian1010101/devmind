# FE03-32 — Responsividade: Primeiros Passos

## O que é Design Responsivo?

**Responsive Web Design (RWD)** é a abordagem de desenvolvimento em que uma aplicação web é construída para se adaptar automaticamente ao tamanho da tela e ao dispositivo do usuário — desde pequenos smartphones de 360px até monitores ultrawide de 4K —, oferecendo uma experiência de leitura e navegação otimizada em qualquer cenário.

---

## O Elemento Obrigatório: A Meta Viewport

Para que o design responsivo funcione em smartphones, a tag `<meta name="viewport">` **deve obrigatoriamente** estar presente dentro do `<head>` do HTML:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

- **`width=device-width`:** instrui o navegador do celular a ajustar a largura da página para acompanhar a largura física real da tela do aparelho em pixels CSS.
- **`initial-scale=1.0`:** define o nível de zoom inicial quando a página é carregada pela primeira vez.

> Sem essa tag, os navegadores móveis assumem que o site foi feito para computadores antigos e renderizam a página em uma tela virtual de 980px, encolhendo os textos até ficarem ilegíveis.

---

## Filosofia Mobile-First vs Desktop-First

Existem duas abordagens para projetar páginas responsivas:

### 1. Mobile-First (Padrão Recomendado da Indústria)
- O CSS base inicial é escrito pensando na tela menor (smartphones).
- Conforme a tela cresce, adicionam-se regras com `@media (min-width: ...)` para expandir colunas e tamanhos.
- **Vantagens:** código mais enxuto, performance aprimorada em redes móveis e alinhamento com a indexação do Google (*Mobile-First Indexing*).

### 2. Desktop-First
- O CSS base inicial é projetado para computadores grandes.
- As media queries usam `@media (max-width: ...)` para comprimir e esconder elementos em telas menores.
