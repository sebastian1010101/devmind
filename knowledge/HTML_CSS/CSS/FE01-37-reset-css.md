# FE01-37 — Reset CSS

## Por que Navegadores Têm Estilos Padrão Diferentes?

Todo navegador (Chrome, Firefox, Safari, Edge) possui uma folha de estilo embutida chamada **User Agent Stylesheet**. Esses estilos atribuem formatações básicas a tags como títulos, listas, botões e tabelas antes mesmo de qualquer CSS do desenvolvedor ser carregado.

O problema: **cada navegador adota margens, espaçamentos internos e tamanhos ligeiramente diferentes**. Sem uma padronização, a mesma página pode renderizar desalinhada em navegadores concorrentes.

---

## O Conceito de Reset CSS

Um arquivo de **Reset CSS** tem como objetivo "zerar" as inconsistências de margens e preenchimentos padrão, oferecendo uma tela em branco previsível e uniforme para o desenvolvimento.

---

## Reset Moderno Recomendado

Atualmente, não é necessário zerar todas as propriedades exaustivamente como se fazia antigamente. O reset moderno foca nas regras essenciais de usabilidade e previsibilidade:

```css
/* 1. Usar border-box em todos os elementos e seus pseudo-elementos */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 2. Suavização de rolagem e prevenção de inflação de fontes */
html {
  -webkit-text-size-adjust: 100%;
  scroll-behavior: smooth;
}

/* 3. Definir altura mínima e tipografia padrão confortável no body */
body {
  min-height: 100vh;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* 4. Imagens e vídeos responsivos que não transbordam */
img,
picture,
video,
canvas,
svg {
  display: block;
  max-width: 100%;
  height: auto;
}

/* 5. Herdar fontes em campos de formulário */
input,
button,
textarea,
select {
  font: inherit;
}

/* 6. Remover decorações de listas e links */
ul,
ol {
  list-style: none;
}

a {
  text-decoration: none;
  color: inherit;
}
```

---

## Como Carregar o Reset no Projeto

O reset deve ser o **primeiro arquivo CSS carregado** no `<head>`, antes de qualquer outro estilo personalizado:

```html
<head>
  <meta charset="UTF-8">
  <title>Meu Projeto</title>
  <!-- 1º: Carrega o reset -->
  <link rel="stylesheet" href="reset.css">
  <!-- 2º: Carrega seus estilos próprios -->
  <link rel="stylesheet" href="style.css">
</head>
```
