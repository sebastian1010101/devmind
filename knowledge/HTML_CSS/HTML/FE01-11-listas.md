# FE01-11 — Listas

## Tipos de Listas em HTML

O HTML disponibiliza três tipos fundamentais de listas para estruturar conjuntos de informações agrupadas:

---

## 1. Listas Não Ordenadas (`<ul>`)

Utilizadas quando a ordem dos elementos não altera o sentido da informação (ex: lista de compras, recursos, menus de navegação). Cada item é definido pela tag `<li>` (*list item*).

```html
<ul>
  <li>HTML5</li>
  <li>CSS3</li>
  <li>JavaScript</li>
</ul>
```

- **Marcador padrão do navegador:** marcadores circulares (*bullets* pretos).

---

## 2. Listas Ordenadas (`<ol>`)

Utilizadas quando a sequência dos passos ou itens tem relevância direta (ex: passo a passo de uma receita, rankings, procedimentos).

```html
<ol>
  <li>Abrir o editor VS Code</li>
  <li>Criar o arquivo index.html</li>
  <li>Digitar a estrutura base do documento</li>
</ol>
```

- **Marcador padrão do navegador:** numeração decimal (`1, 2, 3...`).

### Atributos Úteis em `<ol>`

- `type`: altera o padrão de numeração (`1`, `a`, `A`, `i`, `I`).
- `start`: define o número de início da lista (ex: `<ol start="5">`).
- `reversed`: inverte a contagem de forma decrescente (ex: `<ol reversed>`).

---

## 3. Listas de Descrição / Definição (`<dl>`)

Projetadas para pares de termos e descrições (ex: glossários, especificações técnicas, metadados de produtos).

Composta por três tags coordenadas:
- `<dl>`: *Description List* (o container da lista).
- `<dt>`: *Description Term* (o termo ou palavra sendo definida).
- `<dd>`: *Description Details* (a definição ou detalhamento do termo).

```html
<dl>
  <dt>HTML</dt>
  <dd>Linguagem de marcação para criação da estrutura de páginas web.</dd>

  <dt>CSS</dt>
  <dd>Linguagem de estilos utilizada para controlar a apresentação visual.</dd>
</dl>
```

---

## Aninhamento de Listas

É permitido criar listas aninhadas (uma lista dentro de outra), contanto que a lista interna esteja contida dentro de um `<li>`:

```html
<ul>
  <li>Front-End
    <ul>
      <li>HTML</li>
      <li>CSS</li>
    </ul>
  </li>
  <li>Back-End</li>
</ul>
```
