# FE04-32 — Estado: Reatividade além da Estrutura

## Reatividade = estado dirigindo a UI

A interface é uma **função do estado** — `UI = f(state)`. Quando o estado muda, a UI reflete automaticamente. Isso é o que torna React reativo: você não toca o DOM, descreve o que a UI deve ser para cada estado.

```jsx
function Exemplo() {
  const [logado, setLogado] = useState(false);

  // A UI é uma função do estado 'logado'
  return (
    <div>
      {logado ? <Dashboard /> : <Login />}
      <button onClick={() => setLigado(!logado)}>
        {logado ? "Sair" : "Entrar"}
      </button>
    </div>
  );
}
```

## Estado dirigindo classes e estilos

```jsx
function Botao({ ativo }) {
  return (
    <button
      className={ativo ? "botao ativo" : "botao"}
      style={{ opacity: ativo ? 1 : 0.6 }}
    >
      {ativo ? "Ativo" : "Inativo"}
    </button>
  );
}
```

O visual inteiro muda com o estado — sem tocar o DOM.

## Estado dirigindo renderização condicional

```jsx
{isLoading && <Spinner />}
{erro && <p className="erro">{erro}</p>}
{dados && <Lista dados={dados} />}
{!dados && !isLoading && <p>Sem dados</p>}
```

Quatro estados visuais diferentes — todos derivados de três variáveis de estado.

## Estado compartilhado entre componentes

Quando dois componentes precisam reagir ao mesmo estado, o estado sobe para o ancestral comum — **lifting state up**:

```jsx
function App() {
  const [tema, setTema] = useState("claro");

  return (
    <>
      <Header tema={tema} />               {/* recebe para exibir */}
      <BotaoTema tema={tema} set={setTema} /> {/* recebe para alterar */}
      <Main tema={tema} />                  {/* recebe para estilizar */}
    </>
  );
}
```

Todos os três reagem à mesma mudança — uma fonte de verdade.

## Reatividade com dados derivados

```jsx
function Carrinho() {
  const [itens, setItens] = useState([]);

  // Derivados — recalculam automaticamente a cada render
  const total = itens.reduce((acc, i) => acc + i.preco * i.qtd, 0);
  const quantidade = itens.reduce((acc, i) => acc + i.qtd, 0);
  const temDesconto = total > 100;

  return (
    <div>
      <p>{quantidade} itens — Total: R$ {total.toFixed(2)}</p>
      {temDesconto && <p>🎉 Frete grátis!</p>}
    </div>
  );
}
```

Nenhum `useEffect` para "atualizar o total" — ele é uma expressão do estado e re-renderiza junto.

## O modelo mental

```text
┌─────────────┐     setX()      ┌──────────┐     re-render    ┌─────┐
│   Evento    │ ──────────────► │  Estado  │ ───────────────► │ UI  │
│ (clique,    │                 │  muda    │                  │nova │
│  input,     │                 │          │                  │     │
│  fetch)     │                 │          │                  │     │
└─────────────┘                 └──────────┘                  └─────┘
```

Você programa o **meio** (o estado e suas transições) — a UI é a consequência.

## Padrões de reatividade

| Padrão | Como |
| --- | --- |
| Toggle visual | `className` condicional por estado |
| Mostrar/esconder | `{condicao && <Elemento />}` |
| Estados de carga | `isLoading` + `erro` + `dados` |
| Derivados | Calcule no corpo — não em `useEffect` |
| Compartilhado | Lifting state up ao ancestral comum |

## Resumo

- UI é uma função do estado — descreva a UI para cada estado
- Estado dirige classes, estilos e renderização condicional
- Dados derivados são calculados no render — não precisam de estado próprio
- Lifting state up para estado compartilhado entre componentes
