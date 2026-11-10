# FE05-10 — Aula Extra: Composição no React

## O que é composição

Construir componentes **combinando outros** em vez de herança ou props gigantes — o modelo mental fundamental do React.

> "O React favorece composição sobre herança." — Documentação oficial

## children — a composição mais simples

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

<Card>
  <h2>Título</h2>
  <p>Qualquer conteúdo — imagem, lista, outro componente</p>
</Card>
```

`Card` é uma **moldura** — o conteúdo vem de fora.

## Slots — múltiplas áreas de composição

```jsx
function Layout({ header, sidebar, children }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{children}</main>
    </div>
  );
}

<Layout
  header={<TopBar />}
  sidebar={<Nav />}
>
  <Conteudo />
</Layout>
```

## Composição resolvendo prop drilling

```jsx
// ❌ Drilling
<App>
  <Layout usuario={usuario}>
    <Sidebar usuario={usuario} />
  </Layout>
</App>

// ✅ Composição — App monta direto
function App() {
  const { usuario } = useAuth();
  return (
    <Layout>
      <Sidebar usuario={usuario} />
    </Layout>
  );
}
```

`Layout` não precisa conhecer `usuario` — recebe o JSX montado.

## Componentes especializados — a generalização

```jsx
// Genérico
function Modal({ titulo, children }) {
  return (
    <div className="modal">
      <h2>{titulo}</h2>
      {children}
    </div>
  );
}

// Especializado por composição
function ModalConfirmacao({ confirmar, cancelar }) {
  return (
    <Modal titulo="Confirmar exclusão">
      <p>Tem certeza?</p>
      <button onClick={confirmar}>Sim</button>
      <button onClick={cancelar}>Não</button>
    </Modal>
  );
}
```

`ModalConfirmacao` **compõe** `Modal` — não herda.

## Inversão de controle — o pai decide

```jsx
// O item da lista não sabe que é clicável
function Lista({ itens, renderItem }) {
  return <ul>{itens.map(renderItem)}</ul>;
}

// O pai controla como cada item aparece
<Lista
  itens={produtos}
  renderItem={p => <li key={p.id}>{p.nome}</li>}
/>
```

**Render props** — a prop recebe uma função que retorna JSX.

## Composição vs configuração por props

```jsx
// ❌ Props de configuração demais
<Card
  temImagem
  imagemSrc="..."
  temBotao
  textoBotao="Comprar"
  temBadge
  corBadge="verde"
/>

// ✅ Composição — monta o que precisa
<Card>
  <img src="..." />
  <Badge cor="verde">Novo</Badge>
  <h3>Produto</h3>
  <Botao>Comprar</Botao>
</Card>
```

Props de configuração explodem — composição dá liberdade total.

## O padrão Provider + children

```jsx
// Context é composição pura
<AuthProvider>
  <TemaProvider>
    <CarrinhoProvider>
      <App /> {/* tudo embaixo é children */}
    </CarrinhoProvider>
  </TemaProvider>
</AuthProvider>
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Props de configuração infinitas | Composição com children/slots |
| Herança de componentes | React não tem herança — componha |
| `children` tipado errado | `React.ReactNode` — qualquer JSX |
| Moldura que conhece o conteúdo | Inverta — moldura recebe, não cria |

## Resumo

- Composição = montar UI combinando componentes, não herdando
- `children` e slots (`header`, `sidebar`) criam molduras flexíveis
- Render props invertem o controle — o pai decide como renderizar
- Composição resolve drilling e elimina props de configuração
