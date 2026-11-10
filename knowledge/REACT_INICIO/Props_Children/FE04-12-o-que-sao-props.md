# FE04-12 — O que são Props?

## A ideia central

**Props** (abreviação de *properties*) são os **parâmetros de um componente** — a forma de passar dados de um componente pai para um filho. São o que torna componentes reutilizáveis: a mesma estrutura, dados diferentes.

```jsx
// O componente define o "contrato" — o que aceita
function Saudacao({ nome, idade }) {
  return <p>Olá, {nome}! Você tem {idade} anos.</p>;
}

// O pai passa os valores — como argumentos de função
<Saudacao nome="Ana" idade={28} />
<Saudacao nome="Beto" idade={30} />
```

## Como funciona

O componente recebe **um objeto** com todas as props. Duas formas de ler:

```jsx
// Forma 1 — o objeto 'props' inteiro
function Saudacao(props) {
  return <p>Olá, {props.nome}!</p>;
}

// Forma 2 — desestruturação (a mais usada)
function Saudacao({ nome, idade }) {
  return <p>Olá, {nome}! {idade} anos.</p>;
}
```

## Passando diferentes tipos

Qualquer valor JavaScript pode ser prop:

```jsx
<Card
  titulo="Produto"                    // string
  preco={99.90}                       // número
  disponivel={true}                   // booleano
  tags={["novo", "promoção"]}         // array
  produto={{ id: 1, nome: "X" }}      // objeto
  onComprar={handleCompra}            // função
  icone={<IconeCarrinho />}           // JSX/componente
/>
```

### Strings literais vs expressões

```jsx
<Saudacao nome="Ana" />          // ✅ string literal — sem {}
<Saudacao nome={"Ana"} />        // ✅ também funciona, mas desnecessário
<Saudacao idade={28} />          // ✅ número precisa de {}
<Saudacao idade="28" />          // ⚠️ string "28", não número — cuidado
<Saudacao ativo />               // ✅ shorthand — equivale a ativo={true}
```

## Props são somente leitura (imutáveis)

Regra fundamental: um componente **nunca modifica suas próprias props**. Elas chegam de cima — quem decide o valor é o pai:

```jsx
// ❌ Nunca faça isso
function Contador({ valor }) {
  valor = valor + 1; // muta a prop — proibido
  return <p>{valor}</p>;
}
```

Se o componente precisa de um valor que muda, use **estado** (`useState`) — props são entrada, estado é a memória.

## Fluxo unidirecional (one-way data flow)

Dados descem, eventos sobem:

```text
App (tem os dados)
  │
  ▼ passa props
Lista
  │
  ▼ passa props
Item
  │
  ▲ chama função recebida por prop (evento sobe)
```

```jsx
function App() {
  function excluir(id) {
    console.log("Excluir", id);
  }

  return <Item nome="Produto" onExcluir={excluir} />;
}

function Item({ nome, onExcluir }) {
  // O filho não modifica dados — avisa o pai via função
  return <button onClick={() => onExcluir(1)}>Excluir {nome}</button>;
}
```

## Valores padrão

### Com desestruturação (moderno)

```jsx
function Botao({ texto = "Clique", tipo = "button" }) {
  return <button type={tipo}>{texto}</button>;
}
```

### Com defaultProps (legado)

```jsx
Botao.defaultProps = { texto: "Clique" }; // obsoleto em funções modernas
```

## Prop drilling — a dor do fluxo

Quando um dado precisa descer muitos níveis, componentes intermediários recebem props só para repassar:

```jsx
<App tema={tema}>           // App tem o tema
  <Header tema={tema}>      // Header repassa
    <Nav tema={tema}>       // Nav repassa
      <Link tema={tema} />  // finalmente usa
```

Isso é **prop drilling** — funcional, mas verboso. As soluções (Context API, Zustand, Redux) aparecem no módulo avançado.

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| Modificar props | Estado inconsistente — props são read-only |
| `idade="28"` quando quer número | `Number("28")` para converter, ou `{28}` |
| Esquecer `{}` em expressões | `nome=variavel` passa a string "variavel" |
| Spread excessivo `{...obj}` | Props implícitas — difícil rastrear o que o componente usa |
| Prop drilling profundo | Sinal para considerar Context ou composição |
