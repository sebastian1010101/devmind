# FE01-27 — Trabalhando com Textos

## Principais Propriedades Tipográficas no CSS

A tipografia é um dos pilares mais importantes do design de interfaces. O CSS oferece controle detalhado sobre o comportamento e a aparência de textos:

---

## 1. Famílias de Fontes (`font-family`)

Define as fontes que serão aplicadas, em ordem de prioridade (*font stack*). Sempre finalize com uma família genérica de segurança:

```css
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

Famílias genéricas padrão:
- `sans-serif`: fontes sem serifa, limpas e modernas para telas (ex: Arial, Helvetica).
- `serif`: fontes com serifa, tradicionais e formais (ex: Times New Roman, Georgia).
- `monospace`: fontes monoespaçadas, onde cada caractere possui a mesma largura (ideal para códigos).

---

## 2. Tamanho da Fonte (`font-size`)

Determina o tamanho das letras:

```css
h1 {
  font-size: 32px;
}

p {
  font-size: 1.125rem; /* 18px quando a base é 16px */
}
```

---

## 3. Peso da Fonte (`font-weight`)

Controla a espessura dos traços da fonte. Pode ser declarado por palavras-chave ou números de 100 a 900:

| Valor Numérico | Palavra-chave | Aparência |
| --- | --- | --- |
| `400` | `normal` | Espessura padrão de texto |
| `600` | `semi-bold` | Seminegrito |
| `700` | `bold` | Negrito |

---

## 4. Alinhamento de Texto (`text-align`)

Controla o alinhamento horizontal do texto dentro de seu container:

```css
.texto-esquerda  { text-align: left; }
.texto-central   { text-align: center; }
.texto-direita   { text-align: right; }
.texto-justo     { text-align: justify; }
```

---

## 5. Espaçamento entre Linhas (`line-height`)

Define a altura da linha de texto. Fundamental para garantir legibilidade confortável:

```css
p {
  font-size: 16px;
  line-height: 1.6; /* Proporção ideal para blocos de texto: entre 1.5 e 1.7 */
}
```

---

## 6. Decoração e Transformação

```css
/* text-decoration: remove ou adiciona linhas decorativas */
a {
  text-decoration: none; /* Remove o sublinhado padrão dos links */
}

/* text-transform: manipulação de maiúsculas e minúsculas */
.titulo-caps {
  text-transform: uppercase;   /* TODAS EM MAIÚSCULAS */
  letter-spacing: 1px;         /* Espaço entre letras */
}
```
