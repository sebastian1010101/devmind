# FE04-10 — Componentes: Dicas de Arquitetura

## A pergunta central: quando quebrar?

A habilidade que separa código React legível de caos é saber **quando extrair um componente**. Não existe regra absoluta, mas há sinais claros:

## Sinais de que um componente precisa ser dividido

### 1. O arquivo passa de ~150-200 linhas

Componente gigante concentra lógica, JSX e estado demais — um sinal de que faz várias coisas:

```jsx
// ❌ Componente fazendo tudo — 200+ linhas
function PaginaProduto() {
  const [produto, setProduto] = useState(null);
  const [carrinho, setCarrinho] = useState([]);
  const [comentarios, setComentarios] = useState([]);
  const [modal, setModal] = useState(false);
  // ... 50 linhas de lógica
  // ... 150 linhas de JSX
}

// ✅ Quebrado em responsabilidades
function PaginaProduto() {
  return (
    <>
      <InfoProduto produto={produto} />
      <AcoesCarrinho carrinho={carrinho} />
      <ListaComentarios comentarios={comentarios} />
      <ModalCompra aberto={modal} />
    </>
  );
}
```

### 2. O mesmo JSX se repete

Se você copia e cola um bloco de markup, é um componente esperando nascer:

```jsx
// ❌ Repetição
<div className="card">...</div>
<div className="card">...</div>
<div className="card">...</div>

// ✅ Componente
{cards.map(c => <Card key={c.id} {...c} />)}
```

### 3. Você nomeou um bloco mentalmente

Quando seu código tem "a parte do header", "a lista de itens", "o painel de filtros" — esses são componentes.

## Estruturas de diretório

### Pequeno projeto — plano

```text
src/
├── components/
│   ├── Header.jsx
│   ├── Button.jsx
│   ├── Card.jsx
│   └── Modal.jsx
├── App.jsx
└── main.jsx
```

### Médio — por domínio/feature

```text
src/
├── components/           ← componentes genéricos
│   ├── ui/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   └── Modal.jsx
│   └── layout/
│       ├── Header.jsx
│       └── Footer.jsx
├── features/             ← componentes por funcionalidade
│   ├── auth/
│   │   ├── LoginForm.jsx
│   │   └── RegisterForm.jsx
│   ├── cart/
│   │   ├── CartItem.jsx
│   │   └── CartSummary.jsx
│   └── products/
│       ├── ProductCard.jsx
│       └── ProductGrid.jsx
└── pages/
    ├── HomePage.jsx
    └── CheckoutPage.jsx
```

### A regra de ouro

Componente usado em **um lugar só** → fica na pasta da feature. Componente usado em **vários lugares** → sobe para `components/`.

## Container vs Presentational

Padrão clássico de separação:

### Presentational — só sabe renderizar

```jsx
// Não tem estado, não sabe de onde vêm os dados — só exibe
function ListaProdutos({ produtos, onComprar }) {
  return (
    <ul>
      {produtos.map(p => (
        <li key={p.id}>
          {p.nome} — R$ {p.preco}
          <button onClick={() => onComprar(p)}>Comprar</button>
        </li>
      ))}
    </ul>
  );
}
```

### Container — gerencia dados e lógica

```jsx
function PaginaProdutos() {
  const [produtos, setProdutos] = useState([]);

  useEffect(() => {
    fetch("/api/produtos")
      .then(r => r.json())
      .then(setProdutos);
  }, []);

  return <ListaProdutos produtos={produtos} onComprar={adicionar} />;
}
```

O container busca dados; o presentational renderiza. Facilita testes e reutilização.

## Colocation — arquivos que vivem juntos

Coloque o que pertence ao componente perto dele:

```text
components/Card/
├── Card.jsx            ← componente
├── Card.module.css     ← estilos do componente
├── Card.test.jsx       ← testes
├── Card.stories.jsx    ← Storybook (opcional)
└── index.js            ← re-export
```

Alternativa — "tudo num lugar":

```jsx
// Card.jsx — componente, estilos e helpers juntos
import styles from "./Card.module.css";

function Card({ titulo, children }) {
  return <div className={styles.card}>{children}</div>;
}
```

## Nomeação

| Padrão | Exemplo |
| --- | --- |
| PascalCase | `BotaoPrimario`, `ListaProdutos` |
| Verbo para ações | `handleClick`, `handleSubmit` |
| Substantivo para dados | `produto`, `usuarioAtual` |
| Pasta = componente | `components/Card/Card.jsx` |
| Prefixo de contexto | `CartItem`, `CartSummary`, `CartTotal` |

## Composição > Herança

React recomenda composição — nunca herança entre componentes:

```jsx
// ❌ Herança — não existe em React
class Card extends BaseCard { }

// ✅ Composição — componentes recebem componentes
function Card({ titulo, children }) {
  return (
    <div className="card">
      <h3>{titulo}</h3>
      {children}
    </div>
  );
}

// Uso
<Card titulo="Promoção">
  <ImagemProduto />
  <PrecoComDesconto />
</Card>
```

## Checklist de boa arquitetura

- Um componente = uma responsabilidade clara
- JSX repetido = componente esperando nascer
- Lógica de dados separada da apresentação
- Pasta de componente agrupa componente + estilo + teste
- Componentes genéricos em `components/`, específicos na feature
- Composição e props em vez de herança
- Arquivos com 150+ linhas pedem divisão
