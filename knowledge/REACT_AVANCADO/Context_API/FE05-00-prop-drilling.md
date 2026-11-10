# FE05-00 — Prop Drilling

## O que é prop drilling

O problema de **passar props por vários níveis de componentes** que não usam o dado — só repassam para baixo.

```jsx
function App() {
  const [usuario, setUsuario] = useState({ nome: "Ana" });

  return <Layout usuario={usuario} />; // App tem o dado
}

function Layout({ usuario }) {
  // Layout NÃO usa usuario — só repassa
  return <Sidebar usuario={usuario} />;
}

function Sidebar({ usuario }) {
  // Sidebar também não usa — só repassa
  return <Avatar usuario={usuario} />;
}

function Avatar({ usuario }) {
  return <img src={usuario.foto} />; // só aqui usa
}
```

O dado "perfurou" 3 níveis — drilling = perfuração.

## Por que é um problema

```text
App (tem o estado)
  └── Layout (repassa)
        └── Sidebar (repassa)
              └── Avatar (usa)

- Layout e Sidebar recebem props que não usam
- Mudança no topo re-renderiza toda a cadeia
- Refatorar o meio da cadeia é trabalhoso
- Código acoplado — difícil mover componentes
```

## Quando drilling é aceitável

| Situação | Veredicto |
| --- | --- |
| 1-2 níveis | Normal — não complique |
| 3+ níveis | Considere Context |
| Muitos componentes no meio | Context quase sempre |
| Componente reutilizável no meio | Context (props estragam a reusabilidade) |

## Solução 1 — Composition (sem Context)

Muitas vezes o drilling é evitável com **composição** — passar o componente como `children`:

```jsx
// ❌ Drilling
function App() {
  return <Layout usuario={usuario} />;
}

// ✅ Composição — Layout recebe o resultado montado
function App() {
  const [usuario] = useState({ nome: "Ana" });

  return (
    <Layout>
      <Avatar usuario={usuario} /> {/* App usa direto */}
    </Layout>
  );
}

function Layout({ children }) {
  return <div className="layout">{children}</div>;
}
```

Layout não precisa conhecer `usuario` — recebe o JSX pronto.

## Solução 2 — Context API

```jsx
const UsuarioContext = createContext(null);

function App() {
  const [usuario] = useState({ nome: "Ana" });

  return (
    <UsuarioContext.Provider value={usuario}>
      <Layout /> {/* sem props — Sidebar e Avatar consomem direto */}
    </UsuarioContext.Provider>
  );
}

function Avatar() {
  const usuario = useContext(UsuarioContext); // consome direto
  return <img src={usuario.foto} />;
}
```

## Solução 3 — Estado global (Zustand, Redux)

Para dados que muitos componentes usam — temas, autenticação, carrinho:

```jsx
const useStore = create(set => ({
  usuario: null,
  setUsuario: u => set({ usuario: u })
}));

function Avatar() {
  const usuario = useStore(s => s.usuario); // qualquer nível
}
```

## Comparação das soluções

| Abordagem | Quando usar |
| --- | --- |
| Props normais | 1-2 níveis, dado local |
| Composição (`children`) | Layout/wrapper — dado não precisa circular |
| Context | 3+ níveis, tema/auth/idioma |
| Estado global | Muitos consumidores, atualizações frequentes |

## Erros comuns

| Erro | Correção |
| --- | --- |
| Context para tudo | Overhead e re-renders — drilling leve é ok |
| Props com nome genérico | `dados={dados}` esconde o que é — nomeie `usuario` |
| Repassar spread `{...props}` | Esconde dependências — liste as props |
| Context sem memo | Valor novo a cada render → re-render de todos os consumidores |

## Resumo

- Prop drilling = passar props por níveis que não usam
- 1-2 níveis é normal; 3+ sugere Context ou composição
- `children` resolve muitos casos sem Context
- Context = consumo direto em qualquer profundidade
