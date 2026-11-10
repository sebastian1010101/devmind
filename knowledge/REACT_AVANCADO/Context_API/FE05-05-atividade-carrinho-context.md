# FE05-05 — Atividade: Carrinho de Compras com Context

## Objetivo

Aplicar Context num caso real: carrinho de compras com adicionar, remover, alterar quantidade e calcular total — acessível por qualquer componente.

## O contexto do carrinho

```jsx
// contexts/CarrinhoContext.jsx
import { createContext, useState, useContext, useMemo } from "react";

export const CarrinhoContext = createContext(null);

export function CarrinhoProvider({ children }) {
  const [itens, setItens] = useState([]);

  function adicionar(produto) {
    setItens(atual => {
      const existente = atual.find(i => i.id === produto.id);
      if (existente) {
        return atual.map(i =>
          i.id === produto.id ? { ...i, qtd: i.qtd + 1 } : i
        );
      }
      return [...atual, { ...produto, qtd: 1 }];
    });
  }

  function remover(id) {
    setItens(atual => atual.filter(i => i.id !== id));
  }

  function alterarQtd(id, delta) {
    setItens(atual =>
      atual
        .map(i => i.id === id ? { ...i, qtd: i.qtd + delta } : i)
        .filter(i => i.qtd > 0) // remove se zerar
    );
  }

  const total = useMemo(
    () => itens.reduce((s, i) => s + i.preco * i.qtd, 0),
    [itens]
  );

  const qtdTotal = useMemo(
    () => itens.reduce((s, i) => s + i.qtd, 0),
    [itens]
  );

  const valor = useMemo(
    () => ({ itens, adicionar, remover, alterarQtd, total, qtdTotal }),
    [itens, total, qtdTotal]
  );

  return (
    <CarrinhoContext.Provider value={valor}>
      {children}
    </CarrinhoContext.Provider>
  );
}

export function useCarrinho() {
  const ctx = useContext(CarrinhoContext);
  if (!ctx) throw new Error("useCarrinho deve estar dentro de CarrinhoProvider");
  return ctx;
}
```

## Os componentes

### Lista de produtos

```jsx
function ListaProdutos({ produtos }) {
  const { adicionar } = useCarrinho();

  return (
    <ul>
      {produtos.map(p => (
        <li key={p.id}>
          {p.nome} — R$ {p.preco.toFixed(2)}
          <button onClick={() => adicionar(p)}>+ Carrinho</button>
        </li>
      ))}
    </ul>
  );
}
```

### Ícone do carrinho (header)

```jsx
function IconeCarrinho() {
  const { qtdTotal } = useCarrinho();
  return <span>🛒 {qtdTotal}</span>;
}
```

### Drawer/modal do carrinho

```jsx
function CarrinhoDrawer({ aberto, fechar }) {
  const { itens, remover, alterarQtd, total } = useCarrinho();

  if (!aberto) return null;

  return (
    <aside className="carrinho">
      <button onClick={fechar}>×</button>
      {itens.length === 0 && <p>Carrinho vazio</p>}
      {itens.map(i => (
        <div key={i.id}>
          <span>{i.nome}</span>
          <button onClick={() => alterarQtd(i.id, -1)}>-</button>
          <span>{i.qtd}</span>
          <button onClick={() => alterarQtd(i.id, 1)}>+</button>
          <button onClick={() => remover(i.id)}>Remover</button>
        </div>
      ))}
      <p>Total: R$ {total.toFixed(2)}</p>
    </aside>
  );
}
```

## A estrutura

```jsx
function App() {
  const [aberto, setAberto] = useState(false);

  return (
    <CarrinhoProvider>
      <Header abrirCarrinho={() => setAberto(true)} />
      <ListaProdutos produtos={produtos} />
      <CarrinhoDrawer aberto={aberto} fechar={() => setAberto(false)} />
    </CarrinhoProvider>
  );
}
```

```text
CarrinhoProvider
├── Header → IconeCarrinho usa qtdTotal
├── ListaProdutos → adicionar()
└── CarrinhoDrawer → itens, remover, alterarQtd, total
```

## Por que Context aqui

- **Header** precisa do `qtdTotal` — está em outro ramo da árvore
- **Drawer** precisa de `itens` e `total` — sem drilling
- **ListaProdutos** só chama `adicionar` — não precisa do array

Sem Context: estado no App, props descendo por 3+ níveis.

## Desafios extras

### Desafio A — persistir o carrinho

```jsx
// no Provider
const [itens, setItens] = useState(() => {
  try {
    const salvo = localStorage.getItem("carrinho");
    return salvo ? JSON.parse(salvo) : [];
  } catch {
    return [];
  }
});

useEffect(() => {
  localStorage.setItem("carrinho", JSON.stringify(itens));
}, [itens]);
```

### Desafio B — cupom de desconto

```jsx
const [cupom, setCupom] = useState(null);
const totalComDesconto = cupom ? total * 0.9 : total;
```

### Desafio C — estoque

```jsx
function adicionar(produto) {
  if (produto.estoque <= quantidadeNoCarrinho(produto.id)) {
    alert("Sem estoque");
    return;
  }
  // ...
}
```

## Critérios de verificação

- Actions encapsuladas (`adicionar`, `remover`, `alterarQtd`)
- `total` e `qtdTotal` com `useMemo` — derivados, não estado duplicado
- `valor` do Provider memoizado
- Quantidade > 0 filtra remoção automática
- `useCarrinho` com validação

## Erros comuns

| Erro | Correção |
| --- | --- |
| `total` em useState separado | Derive com `useMemo` — evita dessincronia |
| Adicionar sem checar existente | Incrementa `qtd` se já está no carrinho |
| `value={{...}}` sem useMemo | Re-renders a cada render do Provider |
| `alterarQtd` sem filtro de zero | `.filter(i => i.qtd > 0)` remove zerados |
