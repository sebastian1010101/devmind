# FE04-11 — Fragment

## O problema que o Fragment resolve

Componentes React devem retornar **um único elemento raiz**. Quando a estrutura precisa de elementos irmãos no topo, a solução ingênua é envolver numa `<div>` — mas isso adiciona um nó extra ao DOM:

```jsx
// ❌ Div desnecessária — polui o DOM e pode quebrar CSS
function Lista() {
  return (
    <div>          {/* wrapper artificial só para satisfazer a regra */}
      <li>Item 1</li>
      <li>Item 2</li>
    </div>
  );
}
```

`Fragment` resolve isso: agrupa os elementos **sem criar nó extra no DOM**.

## Sintaxe

### Longa — `React.Fragment`

```jsx
import { Fragment } from "react";

function Lista() {
  return (
    <Fragment>
      <li>Item 1</li>
      <li>Item 2</li>
    </Fragment>
  );
}
```

### Curta — `<>` (a mais usada)

```jsx
function Lista() {
  return (
    <>
      <li>Item 1</li>
      <li>Item 2</li>
    </>
  );
}
```

`<>...</>` é açúcar sintático para `<Fragment>...</Fragment>` — mesmo resultado, menos código.

## Quando importa de verdade

O Fragment não é só estética — em alguns contextos, uma `<div>` extra **quebra** a estrutura:

### Tabelas

```jsx
// ❌ Inválido — <div> dentro de <tr> não é HTML válido
<tr>
  <div>
    <td>Nome</td>
    <td>Idade</td>
  </div>
</tr>

// ✅ Fragment não gera nó — HTML válido
<tr>
  <>
    <td>Nome</td>
    <td>Idade</td>
  </>
</tr>
```

### CSS com seletores diretos

```css
/* Seletor de filho direto — <div> extra quebraria o layout */
.pai > .item { }
```

```jsx
// ❌ Div extra quebra o seletor >
function Itens() {
  return (
    <div>
      <span className="item">A</span>
      <span className="item">B</span>
    </div>
  );
}

// ✅ Fragment mantém os itens como filhos diretos
function Itens() {
  return (
    <>
      <span className="item">A</span>
      <span className="item">B</span>
    </>
  );
}
```

## Fragment com key — o caso do map

A sintaxe curta `<>` **não aceita atributos** — nem `key`. Quando você itera e precisa de `key`, use a forma longa:

```jsx
// ❌ Erro — <> não aceita key
{itens.map(item => (
  <>
    <dt>{item.termo}</dt>
    <dd>{item.definicao}</dd>
  </>
))}

// ✅ React.Fragment aceita key
{itens.map(item => (
  <React.Fragment key={item.id}>
    <dt>{item.termo}</dt>
    <dd>{item.definicao}</dd>
  </React.Fragment>
))}
```

### Exemplo real — lista de definições

```jsx
const glossario = [
  { termo: "HTML", definicao: "Linguagem de marcação" },
  { termo: "CSS", definicao: "Linguagem de estilo" }
];

function ListaDefinicoes() {
  return (
    <dl>
      {glossario.map((item, i) => (
        <React.Fragment key={i}>
          <dt>{item.termo}</dt>
          <dd>{item.definicao}</dd>
        </React.Fragment>
      ))}
    </dl>
  );
}
```

Sem Fragment, `<dt>` + `<dd>` precisariam de um wrapper — e `<div>` dentro de `<dl>` é HTML inválido.

## Fragment vs div — quando usar cada

| Situação | Solução |
| --- | --- |
| Só precisa agrupar, sem propósito semântico | `<>...</>` |
| Precisa de classe/estilo no wrapper | `<div className="...">` |
| Lista iterada precisa de `key` | `<React.Fragment key={id}>` |
| Wrapper semântico (section, article) | Tag semântica real |
| Layout com flex/grid no pai | Pode precisar do nó — teste |

## Retornando array de elementos

Alternativa ao Fragment — um array de elementos (cada um com `key`):

```jsx
function Itens() {
  return [
    <li key="1">Item 1</li>,
    <li key="2">Item 2</li>
  ];
}
```

Funciona, mas é menos legível que `<>` — e exige `key` em cada elemento.

## Resumo

- `<>...</>` agrupa sem criar nó no DOM — resposta padrão ao "um elemento raiz"
- `React.Fragment` (forma longa) aceita `key` — necessário em `.map()`
- Importa em tabelas, listas de definição e qualquer lugar onde um wrapper quebraria HTML/CSS
- Se precisa de classe ou semântica, use `<div>` real — Fragment é invisível por design
