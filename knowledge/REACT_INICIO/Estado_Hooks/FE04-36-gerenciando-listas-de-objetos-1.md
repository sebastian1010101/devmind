# FE04-36 — Estado: Gerenciando Listas de Objetos — Parte 1

## O padrão lista de objetos

O estado mais comum em apps reais: um array de objetos (produtos, tarefas, usuários) que precisa ser adicionado, removido e atualizado — tudo de forma **imutável**.

```jsx
const [tarefas, setTarefas] = useState([
  { id: 1, texto: "Estudar", feita: false },
  { id: 2, texto: "Treinar", feita: true }
]);
```

## As quatro operações

### Adicionar — `[...lista, novo]`

```jsx
function adicionar(texto) {
  const nova = {
    id: Date.now(),
    texto,
    feita: false
  };
  setTarefas(prev => [...prev, nova]);
}
```

### Remover — `filter`

```jsx
function remover(id) {
  setTarefas(prev => prev.filter(t => t.id !== id));
}
```

### Atualizar — `map` com spread

```jsx
function alternar(id) {
  setTarefas(prev =>
    prev.map(t => t.id === id ? { ...t, feita: !t.feita } : t)
  );
}
```

O padrão `map + spread`: para cada item, se é o alvo → retorna cópia modificada; senão → retorna o mesmo objeto (referência intacta = React não re-renderiza essa parte).

### Atualizar campo específico

```jsx
function editarTexto(id, novoTexto) {
  setTarefas(prev =>
    prev.map(t => t.id === id ? { ...t, texto: novoTexto } : t)
  );
}
```

## Reordenando

```jsx
// Mover para cima
function subir(indice) {
  if (indice === 0) return;
  setTarefas(prev => {
    const nova = [...prev];
    [nova[indice - 1], nova[indice]] = [nova[indice], nova[indice - 1]];
    return nova;
  });
}
```

⚠️ Sempre copie (`[...prev]`) antes de usar métodos que mutam (`splice`, `sort`, troca por índice).

## Filtros de exibição — derive, não guarde

```jsx
const [filtro, setFiltro] = useState("todas"); // "todas" | "pendentes" | "feitas"

// Derivado — recalcula sozinho a cada render
const exibidas = tarefas.filter(t => {
  if (filtro === "pendentes") return !t.feita;
  if (filtro === "feitas") return t.feita;
  return true;
});
```

```jsx
<button onClick={() => setFiltro("todas")}>Todas</button>
<button onClick={() => setFiltro("pendentes")}>Pendentes</button>
<button onClick={() => setFiltro("feitas")}>Feitas</button>
```

O filtro é estado; a lista filtrada é **derivação** — calculada no render, não guardada.

## Busca combinada

```jsx
const [busca, setBusca] = useState("");

const filtradas = tarefas.filter(t =>
  t.texto.toLowerCase().includes(busca.toLowerCase())
);
```

## Estatísticas derivadas

```jsx
const total = tarefas.length;
const feitas = tarefas.filter(t => t.feita).length;
const pendentes = total - feitas;
const progresso = total ? Math.round((feitas / total) * 100) : 0;
```

Tudo derivado de `tarefas` — nada disso precisa de `useState` próprio.

## Resumo das operações imutáveis

| Operação | Método |
| --- | --- |
| Adicionar | `[...lista, novo]` |
| Remover | `lista.filter(x => x.id !== id)` |
| Atualizar | `lista.map(x => x.id === id ? {...x, campo} : x)` |
| Reordenar | Cópia + splice/swap |
| Filtrar exibição | Derive no render — não guarde |
| Limpar | `setLista([])` |
