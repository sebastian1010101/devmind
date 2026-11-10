# FE01-52 — Seletores Avançados

## Combinadores no CSS

Os combinadores explicam como múltiplos seletores se relacionam entre si na árvore do DOM:

---

## 1. Seletor Descendente (Espaço em Branco)

Seleciona **qualquer elemento filho, neto ou descendente em qualquer nível de profundidade**:

```css
/* Qualquer link dentro do menu, não importa quão aninhado */
.menu a {
  color: #ffffff;
}
```

---

## 2. Seletor Filho Direto (`>`)

Seleciona apenas os elementos que são **filhos imediatos de primeiro nível**, ignorando netos:

```html
<ul class="lista-pai">
  <li>Filho Direto 1</li>
  <li>
    Filho Direto 2
    <ul>
      <li>Neto (não afetado)</li>
    </ul>
  </li>
</ul>
```

```css
.lista-pai > li {
  font-weight: bold; /* Aplica-se apenas aos <li> do primeiro nível */
}
```

---

## 3. Seletor de Irmão Adjacente / Próximo (`+`)

Seleciona o elemento que vem **imediatamente após** o elemento de referência, compartilhando o mesmo pai:

```css
/* Estiliza apenas o primeiro parágrafo logo após o título h2 */
h2 + p {
  font-size: 1.25rem;
  color: #475569;
}
```

---

## 4. Seletor de Irmãos Gerais (`~`)

Seleciona **todos os irmãos posteriores** que compartilham o mesmo pai, mesmo que não estejam imediatamente colados:

```css
/* Todos os parágrafos que aparecem depois de um h2 naquele container */
h2 ~ p {
  line-height: 1.8;
}
```

---

## 5. Seletores por Atributo

Permitem estilizar tags com base na presença e valor dos seus atributos HTML:

| Sintaxe | Critério de Seleção | Exemplo Prático |
| --- | --- | --- |
| `[atributo]` | Elemento possui o atributo presente | `input[required]` |
| `[atributo="valor"]` | Valor exato idêntico | `input[type="password"]` |
| `[atributo^="valor"]` | Valor **começa com** o prefixo | `a[href^="https://"]` (links externos seguros) |
| `[atributo$="valor"]` | Valor **termina com** o sufixo | `a[href$=".pdf"]` (links de arquivos PDF) |
| `[atributo*="valor"]` | Valor **contém** o termo em qualquer parte | `img[src*="avatar"]` |
