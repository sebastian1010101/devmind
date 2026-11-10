# FE04-37 — Estado: Gerenciando Listas de Objetos — Parte 2

## Padrões avançados

Continuação com operações mais complexas sobre listas de objetos no estado.

## Atualização aninhada

Quando o objeto tem objetos internos, o spread precisa descer os níveis:

```jsx
const [pedidos, setPedidos] = useState([
  {
    id: 1,
    cliente: { nome: "Ana", endereco: { cidade: "SP" } },
    itens: [{ id: 10, nome: "Pizza", qtd: 2 }]
  }
]);

// Atualizar campo aninhado
function mudarCidade(pedidoId, novaCidade) {
  setPedidos(prev =>
    prev.map(p =>
      p.id === pedidoId
        ? {
            ...p,
            cliente: {
              ...p.cliente,
              endereco: { ...p.cliente.endereco, cidade: novaCidade }
            }
          }
        : p
    )
  );
}
```

Cada nível precisa de seu próprio spread — imutabilidade em profundidade.

## Atualizar item dentro de lista interna

```jsx
// Marcar um item específico dentro do pedido
function marcarItem(pedidoId, itemId) {
  setPedidos(prev =>
    prev.map(p =>
      p.id === pedidoId
        ? {
            ...p,
            itens: p.itens.map(i =>
              i.id === itemId ? { ...i, feito: true } : i
            )
          }
        : p
    )
  );
}
```

## Operações em massa

```jsx
// Marcar todos como feitos
setTarefas(prev => prev.map(t => ({ ...t, feita: true })));

// Remover todos os feitos
setTarefas(prev => prev.filter(t => !t.feita));

// Duplicar um item
setTarefas(prev => [
  ...prev.slice(0, indice + 1),
  { ...prev[indice], id: Date.now() },
  ...prev.slice(indice + 1)
]);
```

## Ordenação imutável

```jsx
// ⚠️ sort muta — sempre copie antes
const ordenadas = [...tarefas].sort((a, b) => a.texto.localeCompare(b.texto));

// Ou via estado para reordenar a lista em si
function ordenarPorNome() {
  setTarefas(prev => [...prev].sort((a, b) => a.texto.localeCompare(b.texto)));
}
```

## Estado de edição inline

Padrão de edição de item na própria lista:

```jsx
const [editandoId, setEditandoId] = useState(null);
const [textoEdicao, setTextoEdicao] = useState("");

function iniciarEdicao(tarefa) {
  setEditandoId(tarefa.id);
  setTextoEdicao(tarefa.texto);
}

function salvarEdicao() {
  setTarefas(prev =>
    prev.map(t => t.id === editandoId ? { ...t, texto: textoEdicao } : t)
  );
  setEditandoId(null);
  setTextoEdicao("");
}
```

```jsx
{tarefas.map(t => (
  <li key={t.id}>
    {editandoId === t.id ? (
      <>
        <input value={textoEdicao} onChange={e => setTextoEdicao(e.target.value)} />
        <button onClick={salvarEdicao}>Salvar</button>
      </>
    ) : (
      <>
        <span>{t.texto}</span>
        <button onClick={() => iniciarEdicao(t)}>Editar</button>
      </>
    )}
  </li>
))}
```

## Quando a lista vira complexa: useReducer

Muitas operações sobre a mesma lista pedem `useReducer` — centraliza as transições:

```jsx
function reducer(tarefas, acao) {
  switch (acao.type) {
    case "adicionar":
      return [...tarefas, acao.tarefa];
    case "remover":
      return tarefas.filter(t => t.id !== acao.id);
    case "alternar":
      return tarefas.map(t => t.id === acao.id ? { ...t, feita: !t.feita } : t);
    default:
      return tarefas;
  }
}

const [tarefas, dispatch] = useReducer(reducer, []);
dispatch({ type: "adicionar", tarefa: nova });
```

Use quando: mais de ~4 operações, lógica condicional complexa, ou o próximo estado depende de múltiplos campos.

## Resumo

- Aninhado → spread em cada nível
- `[...arr].sort()` — nunca `sort` direto no estado
- Edição inline via `editandoId` + estado temporário
- `useReducer` quando a lista tem muitas operações
