# FE01-51 — Seletores de Pseudo-Elementos

## O que é um Pseudo-Elemento?

Enquanto as pseudo-classes (`:`) selecionam elementos existentes em estados específicos, os **pseudo-elementos** (identificados por dois pontos duplos `::`) permitem estilizar **partes específicas de um elemento** ou **inserir conteúdo puramente cosmético no DOM via CSS** sem poluir o código HTML com tags desnecessárias.

---

## 1. `::before` e `::after` (Inserção de Conteúdo)

Criam pseudo-elementos virtuais que se comportam como o **primeiro filho** (`::before`) ou o **último filho** (`::after`) do elemento selecionado.

### Regra Obrigatória — Propriedade `content`

Para que `::before` e `::after` sejam renderizados, a propriedade `content` é estritamente obrigatória, mesmo que com valor vazio (`content: "";`):

```css
/* Adicionando aspas decorativas antes de uma citação */
blockquote::before {
  content: "“";
  font-size: 3rem;
  color: #3b82f6;
  line-height: 0;
  vertical-align: -0.4em;
  margin-right: 8px;
}
```

### Criando Barras Decorativas e Sublinhados Dinâmicos

```css
.titulo-secao {
  position: relative;
  display: inline-block;
}

/* Cria uma linha colorida embaixo do título */
.titulo-secao::after {
  content: "";
  position: absolute;
  bottom: -6px;
  left: 0;
  width: 50%;
  height: 3px;
  background-color: #2563eb;
  border-radius: 2px;
}
```

---

## 2. `::placeholder`

Permite modificar a aparência visual (cor, opacidade, estilo) do texto de dica de campos de entrada:

```css
input::placeholder {
  color: #94a3b8;
  font-style: italic;
  opacity: 0.8;
}
```

---

## 3. `::selection`

Altera as cores de fundo e texto quando o usuário destaca e seleciona trechos da página com o mouse:

```css
::selection {
  background-color: #2563eb;
  color: #ffffff;
}
```

---

## 4. `::first-letter` e `::first-line`

- `::first-letter`: estiliza apenas a primeiríssima letra de um parágrafo (técnica editorial de *capitular* / *drop cap*).
- `::first-line`: estiliza toda a primeira linha de um parágrafo conforme ela quebra na tela.

```css
p.capitular::first-letter {
  font-size: 3rem;
  font-weight: bold;
  float: left;
  line-height: 1;
  padding-right: 8px;
  color: #0f172a;
}
```
