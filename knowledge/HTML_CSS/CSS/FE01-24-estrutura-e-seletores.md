# FE01-24 — Estrutura e Seletores

## Anatomia de uma Regra CSS

Uma regra CSS é composta por um **seletor** e um **bloco de declaração** delimitado por chaves `{}`:

```css
seletor {
  propriedade: valor;
}
```

- **Seletor:** identifica quais elementos HTML receberão a estilização.
- **Propriedade:** a característica visual que será modificada (ex: `color`, `font-size`).
- **Valor:** a definição atribuída à propriedade (ex: `blue`, `16px`).
- **Declaração:** o conjunto `propriedade: valor;` finalizado com ponto e vírgula.

---

## Seletores Básicos

### 1. Seletor de Tipo / Tag

Aplica o estilo a todos os elementos HTML daquela tag:

```css
p {
  color: #333333;
  line-height: 1.5;
}
```

### 2. Seletor de Classe (`.`)

Identifica elementos que possuem a classe correspondente. Pode ser compartilhado por vários elementos:

```html
<button class="btn btn-primario">Salvar</button>
<button class="btn btn-secundario">Cancelar</button>
```

```css
.btn {
  padding: 10px 20px;
  border-radius: 4px;
}

.btn-primario {
  background-color: #0070f3;
  color: #ffffff;
}
```

### 3. Seletor de ID (`#`)

Identifica um único elemento exclusivo com aquele `id`. Possui peso de especificidade maior que classes:

```html
<header id="cabecalho-principal"></header>
```

```css
#cabecalho-principal {
  background-color: #1a1a1a;
}
```

### 4. Seletor Universal (`*`)

Seleciona todos os elementos do documento simultaneamente. Muito utilizado em resets:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
```

---

## Agrupamento de Seletores

Para aplicar as mesmas propriedades a múltiplos seletores sem duplicar código, separam-se os seletores por vírgula:

```css
h1, h2, h3 {
  font-family: 'Poppins', sans-serif;
  color: #111111;
}
```
