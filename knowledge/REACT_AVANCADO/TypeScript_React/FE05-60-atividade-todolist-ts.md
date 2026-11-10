# FE05-60 — Atividade: TodoList com TypeScript

## Objetivo

Todo list completo com TypeScript — estado tipado, reducer com union de actions, formulário validado e persistência.

## O tipo Todo

```typescript
interface Todo {
  id: string;
  texto: string;
  concluida: boolean;
  criadaEm: number;
  prioridade: "baixa" | "media" | "alta";
}
```

## O estado com useReducer tipado

```tsx
interface EstadoTodos {
  todos: Todo[];
  filtro: "todas" | "ativas" | "concluidas";
}

type AcaoTodo =
  | { type: "adicionar"; payload: { texto: string; prioridade: Todo["prioridade"] } }
  | { type: "alternar"; payload: string } // id
  | { type: "remover"; payload: string }
  | { type: "editar"; payload: { id: string; texto: string } }
  | { type: "limparConcluidas" }
  | { type: "setFiltro"; payload: EstadoTodos["filtro"] };

function todosReducer(state: EstadoTodos, action: AcaoTodo): EstadoTodos {
  switch (action.type) {
    case "adicionar":
      return {
        ...state,
        todos: [...state.todos, {
          id: crypto.randomUUID(),
          texto: action.payload.texto,
          prioridade: action.payload.prioridade,
          concluida: false,
          criadaEm: Date.now()
        }]
      };

    case "alternar":
      return {
        ...state,
        todos: state.todos.map(t =>
          t.id === action.payload ? { ...t, concluida: !t.concluida } : t
        )
      };

    case "remover":
      return {
        ...state,
        todos: state.todos.filter(t => t.id !== action.payload)
      };

    case "editar":
      return {
        ...state,
        todos: state.todos.map(t =>
          t.id === action.payload.id
            ? { ...t, texto: action.payload.texto }
            : t
        )
      };

    case "limparConcluidas":
      return { ...state, todos: state.todos.filter(t => !t.concluida) };

    case "setFiltro":
      return { ...state, filtro: action.payload };

    default:
      return state;
  }
}
```

## O hook customizado

```tsx
function useTodos() {
  const [estado, dispatch] = useReducer(todosReducer, {
    todos: [],
    filtro: "todas"
  });

  // persistência
  useEffect(() => {
    localStorage.setItem("todos", JSON.stringify(estado.todos));
  }, [estado.todos]);

  // filtro derivado
  const filtradas = estado.todos.filter(t => {
    if (estado.filtro === "ativas") return !t.concluida;
    if (estado.filtro === "concluidas") return t.concluida;
    return true;
  });

  return { ...estado, filtradas, dispatch };
}
```

## O formulário

```tsx
function FormTodo({ dispatch }: { dispatch: Dispatch<AcaoTodo> }) {
  const [texto, setTexto] = useState("");
  const [prioridade, setPrioridade] = useState<Todo["prioridade"]>("media");

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!texto.trim()) return;
    dispatch({
      type: "adicionar",
      payload: { texto: texto.trim(), prioridade }
    });
    setTexto("");
  }
}
```

## O item

```tsx
interface ItemTodoProps {
  todo: Todo;
  dispatch: Dispatch<AcaoTodo>;
}

function ItemTodo({ todo, dispatch }: ItemTodoProps) {
  return (
    <li className={todo.concluida ? "concluida" : ""}>
      <input
        type="checkbox"
        checked={todo.concluida}
        onChange={() => dispatch({ type: "alternar", payload: todo.id })}
      />
      <span>{todo.texto}</span>
      <span className={`prioridade ${todo.prioridade}`} />
      <button onClick={() => dispatch({ type: "remover", payload: todo.id })}>
        ×
      </button>
    </li>
  );
}
```

## O filtro

```tsx
function FiltroTodos({ filtro, dispatch }: {
  filtro: EstadoTodos["filtro"];
  dispatch: Dispatch<AcaoTodo>;
}) {
  const opcoes: EstadoTodos["filtro"][] = ["todas", "ativas", "concluidas"];

  return (
    <div>
      {opcoes.map(f => (
        <button
          key={f}
          className={filtro === f ? "ativo" : ""}
          onClick={() => dispatch({ type: "setFiltro", payload: f })}
        >
          {f}
        </button>
      ))}
    </div>
  );
}
```

## Critérios de verificação

- `Todo` interface com prioridade literal union
- `AcaoTodo` union com `type` discriminante
- `useReducer` tipado — `estado` e `action` com tipos
- `Dispatch<AcaoTodo>` nas props — type-safe dispatch
- `filtradas` derivado — sem estado duplicado
- `crypto.randomUUID()` para ids

## Erros comuns

| Erro | Correção |
| --- | --- |
| `action: any` no reducer | Union `AcaoTodo` — type-safe |
| `payload` genérico | `payload: string` ou objeto tipado |
| `filtro` sem union | `"todas" \| "ativas" \| "concluidas"` |
| `dispatch` com `Function` | `Dispatch<AcaoTodo>` — tipado |
