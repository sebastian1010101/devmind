# FE05-24 — Atividade: Criando um Todo List com Zustand

## Objetivo

Todo list completo com Zustand — adicionar, alternar, remover, filtrar — sem Context, sem props drilling.

## A store

```jsx
// store/useTodoStore.js
import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useTodoStore = create(
  persist(
    (set) => ({
      todos: [],

      adicionar: (texto) =>
        set(s => ({
          todos: [
            ...s.todos,
            {
              id: crypto.randomUUID(),
              texto,
              concluida: false,
              criadaEm: Date.now()
            }
          ]
        })),

      alternar: (id) =>
        set(s => ({
          todos: s.todos.map(t =>
            t.id === id ? { ...t, concluida: !t.concluida } : t
          )
        })),

      remover: (id) =>
        set(s => ({
          todos: s.todos.filter(t => t.id !== id)
        })),

      limparConcluidas: () =>
        set(s => ({
          todos: s.todos.filter(t => !t.concluida)
        }))
    }),
    { name: "todos" } // persiste no localStorage
  )
);
```

## Os componentes

### Formulário

```jsx
function FormTodo() {
  const [texto, setTexto] = useState("");
  const adicionar = useTodoStore(s => s.adicionar);

  function handleSubmit(e) {
    e.preventDefault();
    if (texto.trim()) {
      adicionar(texto.trim());
      setTexto("");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={texto}
        onChange={e => setTexto(e.target.value)}
        placeholder="Nova tarefa..."
      />
      <button>Adicionar</button>
    </form>
  );
}
```

### Item

```jsx
function ItemTodo({ todo }) {
  const alternar = useTodoStore(s => s.alternar);
  const remover = useTodoStore(s => s.remover);

  return (
    <li className={todo.concluida ? "concluida" : ""}>
      <input
        type="checkbox"
        checked={todo.concluida}
        onChange={() => alternar(todo.id)}
      />
      <span>{todo.texto}</span>
      <button onClick={() => remover(todo.id)}>×</button>
    </li>
  );
}
```

### Lista com filtro

```jsx
function ListaTodos() {
  const todos = useTodoStore(s => s.todos);
  const [filtro, setFiltro] = useState("todas"); // local — só o filtro

  const filtradas = todos.filter(t => {
    if (filtro === "ativas") return !t.concluida;
    if (filtro === "concluidas") return t.concluida;
    return true;
  });

  return (
    <div>
      <div className="filtros">
        {["todas", "ativas", "concluidas"].map(f => (
          <button
            key={f}
            className={filtro === f ? "ativo" : ""}
            onClick={() => setFiltro(f)}
          >
            {f}
          </button>
        ))}
      </div>
      <ul>
        {filtradas.map(t => <ItemTodo key={t.id} todo={t} />)}
      </ul>
    </div>
  );
}
```

### Rodapé — contadores derivados

```jsx
function RodapeTodos() {
  const ativas = useTodoStore(s =>
    s.todos.filter(t => !t.concluida).length
  );
  const limpar = useTodoStore(s => s.limparConcluidas);

  return (
    <footer>
      <span>{ativas} pendentes</span>
      <button onClick={limpar}>Limpar concluídas</button>
    </footer>
  );
}
```

## Persistência automática

O `persist` middleware salva `todos` no `localStorage` automaticamente — ao recarregar, restaura:

```jsx
persist(
  (set) => ({ ... }),
  { name: "todos" } // localStorage["todos"]
)
```

## Sem Provider — a liberdade

```jsx
// main.jsx — NÃO precisa de Provider
function App() {
  return (
    <div>
      <FormTodo />
      <ListaTodos />
      <RodapeTodos />
    </div>
  );
}
```

A store existe globalmente — qualquer componente usa.

## Desafios extras

### Desafio A — edição inline

```jsx
// na store
editar: (id, novoTexto) =>
  set(s => ({
    todos: s.todos.map(t =>
      t.id === id ? { ...t, texto: novoTexto } : t
    )
  }))
```

### Desafio B — reordenar

```jsx
reordenar: (origem, destino) =>
  set(s => {
    const copia = [...s.todos];
    const [item] = copia.splice(origem, 1);
    copia.splice(destino, 0, item);
    return { todos: copia };
  })
```

### Desafio C — categorias

```jsx
adicionar: (texto, categoria) =>
  set(s => ({
    todos: [...s.todos, { id: uuid(), texto, categoria, concluida: false }]
  }))
```

## Critérios de verificação

- Store em `store/useTodoStore.js`
- `persist` com nome — dados sobrevivem ao reload
- Seletores finos — `s.todos`, `s.adicionar`
- Filtro é estado local — não global
- `crypto.randomUUID()` para ids

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useTodoStore()` sem seletor | Re-renderiza em qualquer mudança |
| Estado de filtro na store | `useState` local — só o componente usa |
| `id` com Date.now() | `crypto.randomUUID()` — único |
| Ações fora da store | Encapsule na store — lógica centralizada |
