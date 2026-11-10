# FE04-14 — O que são Children?

## O conceito

`children` é a prop especial que recebe **tudo que fica entre as tags de abertura e fechamento** de um componente — o conteúdo "filho" passado na invocação:

```jsx
<Card>
  <h2>Título</h2>     {/* isso é children */}
  <p>Conteúdo</p>     {/* isso também */}
</Card>
```

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}
```

O conteúdo entre `<Card>` e `</Card>` chega como `children` — um prop como qualquer outro, mas capturado automaticamente pelo React.

## Por que children existe

Props normais carregam dados — `children` carrega **estrutura**. É o mecanismo que torna componentes "molduras" flexíveis:

```jsx
// ❌ Sem children — o componente precisa de uma prop para cada pedaço
function Card({ titulo, texto, botao }) {
  return (
    <div>
      <h2>{titulo}</h2>
      <p>{texto}</p>
      {botao}
    </div>
  );
}

// ✅ Com children — quem usa decide o que vai dentro
function Card({ titulo, children }) {
  return (
    <div className="card">
      <h2>{titulo}</h2>
      {children}
    </div>
  );
}

// Uso — conteúdo arbitrário, não limitado a strings
<Card titulo="Promoção">
  <img src="produto.jpg" />
  <p>Descrição qualquer</p>
  <ul><li>Item</li></ul>
  <BotaoComprar />
</Card>
```

## O tipo de children

`children` aceita qualquer coisa renderizável — inclusive nada:

```jsx
<Card>texto</Card>                    // string
<Card><p>JSX</p></Card>               // um elemento
<Card><p>A</p><p>B</p></Card>         // múltiplos elementos
<Card>{lista.map(...)}</Card>         // resultado de expressão
<Card />                              // children = undefined
<Card>{condicao && <p>Sim</p>}</Card> // condicional
```

## Componentes de layout — o caso clássico

`children` é a base dos componentes "moldura" — wrappers de layout e padrões visuais:

```jsx
function Container({ children }) {
  return <div className="container">{children}</div>;
}

function Modal({ aberto, children }) {
  if (!aberto) return null;
  return (
    <div className="overlay">
      <div className="modal">{children}</div>
    </div>
  );
}

function Secao({ titulo, children }) {
  return (
    <section>
      <h2>{titulo}</h2>
      {children}
    </section>
  );
}
```

```jsx
// Uso — a moldura é fixa, o recheio é livre
<Modal aberto={true}>
  <h2>Confirmar exclusão?</h2>
  <p>Esta ação não pode ser desfeita.</p>
  <button>Cancelar</button>
  <button>Confirmar</button>
</Modal>
```

## Children como função (render props)

Padrão avançado — `children` recebe uma **função** que o componente chama com dados:

```jsx
function Lista({ dados, children }) {
  return (
    <ul>
      {dados.map(item => (
        <li key={item.id}>{children(item)}</li>
      ))}
    </ul>
  );
}

// Quem usa decide COMO renderizar cada item
<Lista dados={usuarios}>
  {usuario => <strong>{usuario.nome}</strong>}
</Lista>
```

## children vs props nomeadas

| | `children` | Prop nomeada |
| --- | --- | --- |
| O que carrega | Conteúdo entre tags | Dados/atributos |
| Quantidade | Uma só | Quantas quiser |
| Uso típico | Molduras, layouts, wrappers | Dados, callbacks, config |

## Slots com props nomeadas

Quando a moldura precisa de **várias** áreas de conteúdo, props nomeadas funcionam como "slots":

```jsx
function Card({ cabecalho, children, rodape }) {
  return (
    <div className="card">
      <header>{cabecalho}</header>
      <main>{children}</main>
      <footer>{rodape}</footer>
    </div>
  );
}

<Card
  cabecalho={<h2>Título</h2>}
  rodape={<button>Ação</button>}
>
  <p>Conteúdo principal</p>
</Card>
```

## Resumo

- `children` = o que está entre as tags do componente — capturado automaticamente
- Transforma componentes em molduras reutilizáveis
- Aceita qualquer JSX: texto, elementos, listas, até funções
- É o padrão de composição que faz React escalar — `Modal`, `Card`, `Layout` são todos children-powered
