# FE01-23 — Utilizando CSS no HTML

## As Três Formas de Aplicar CSS

O CSS pode ser vinculado a uma página HTML de três maneiras diferentes:

---

## 1. CSS Externo (External CSS) — Recomendado

As regras são salvas em um arquivo separado com extensão `.css` (por exemplo, `style.css`) e vinculadas dentro do elemento `<head>` do HTML através da tag `<link>`.

```html
<head>
  <meta charset="UTF-8">
  <title>Minha Página</title>
  <link rel="stylesheet" href="style.css">
</head>
```

```css
/* style.css */
body {
  background-color: #f4f4f4;
  font-family: Arial, sans-serif;
}
```

- **Vantagens:** separação total de responsabilidades, cache eficiente no navegador e reaproveitamento em dezenas de páginas HTML simultaneamente.

---

## 2. CSS Interno (Internal CSS)

As regras são escritas dentro da tag `<style>` localizada no `<head>` do próprio documento HTML.

```html
<head>
  <meta charset="UTF-8">
  <title>Página com CSS Interno</title>
  <style>
    h1 {
      color: #0066cc;
      text-align: center;
    }
  </style>
</head>
```

- **Uso comum:** páginas de pouso (*landing pages*) exclusivas de um único arquivo ou testes rápidos de prototipação.

---

## 3. CSS Inline (Inline CSS) — Não Recomendado

As regras são declaradas diretamente na tag de abertura do elemento HTML através do atributo `style`.

```html
<h1 style="color: red; font-size: 28px;">Título em Vermelho</h1>
```

- **Desvantagens:** mistura estrutura com apresentação, dificulta a manutenção, possui altíssima especificidade (difícil de sobrescrever) e impede o reaproveitamento de código.
