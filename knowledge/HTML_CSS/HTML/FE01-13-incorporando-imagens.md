# FE01-13 — Incorporando Imagens

## A Tag `<img>`

A tag `<img>` é um elemento autocontido (*void element*) usado para incorporar imagens em uma página web.

```html
<img src="caminho/para/imagem.jpg" alt="Descrição clara da imagem">
```

---

## Atributos Essenciais

### 1. `src` (Source)
O caminho para o arquivo da imagem. Pode ser:
- **Relativo local:** `src="imagens/logo.png"` ou `src="./avatar.webp"`.
- **Absoluto web:** `src="https://exemplo.com/foto.jpg"`.

### 2. `alt` (Alternative Text) — Obrigatório para Acessibilidade e SEO
Fornece um texto alternativo caso a imagem falhe ao carregar e serve como leitura principal para pessoas que utilizam **leitores de tela**.

- **Bom texto alternativo:** descreve a informação ou intenção da imagem no contexto.
  - *Exemplo:* `alt="Logotipo da Kenzie Academy com texto em azul e fundo transparente"`
- **Evite:** `alt="imagem"`, `alt="foto"` ou deixar sem o atributo.
- **Imagens meramente decorativas:** utilize `alt=""` vazio para que tecnologias assistivas ignorem a imagem.

---

## Atributos de Dimensões e Performance

Para evitar o salto de layout (*Cumulative Layout Shift - CLS*) enquanto a página carrega, é recomendável informar a largura e a altura nativas da imagem:

```html
<img src="banner.jpg" alt="Equipe reunida em sala de reunião" width="800" height="400" loading="lazy">
```

- `width` e `height`: dimensões em pixels (sem colocar a unidade `px` no atributo HTML).
- `loading="lazy"`: adia o carregamento de imagens fora da tela inicial (*viewport*) até que o usuário role a página até perto delas, economizando banda e acelerando o carregamento inicial.

---

## A Tag `<figure>` e `<figcaption>`

Quando a imagem precisa de uma legenda semântica associada:

```html
<figure>
  <img src="grafico-vendas.png" alt="Gráfico de barras mostrando crescimento de 30% em 2026">
  <figcaption>Figura 1 — Evolução trimestral das vendas no ano de 2026.</figcaption>
</figure>
```
