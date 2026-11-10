# FE05-50 — TypeScript no React: Estados

## useState — inferência na maioria

```tsx
const [contador, setContador] = useState(0);      // number — inferido
const [nome, setNome] = useState("");              // string
const [ativo, setAtivo] = useState(false);          // boolean
const [lista, setLista] = useState<string[]>([]);   // array vazio — precisa
```

TS infere o tipo do valor inicial — mas **array/objeto vazio precisa de tipo explícito**.

## useState com tipo explícito

```tsx
interface Usuario {
  id: number;
  nome: string;
}

// pode ser null — ainda não carregou
const [usuario, setUsuario] = useState<Usuario | null>(null);

// array vazio de tipo específico
const [produtos, setProdutos] = useState<Produto[]>([]);

// union — pode ser vários tipos
const [valor, setValor] = useState<string | number>("");
```

## O union com null — o padrão async

```tsx
const [dados, setDados] = useState<Produto | null>(null);
const [carregando, setCarregando] = useState(true);

if (carregando) return <p>Carregando...</p>;
if (!dados) return <p>Sem dados</p>;

// aqui dados é Produto — narrowing automático
return <p>{dados.nome}</p>;
```

## Atualizando estado tipado

```tsx
setUsuario({
  id: 1,
  nome: "Ana"
  // ❌ sem email se a interface exige
});

// forma funcional — preserva o tipo
setContador(c => c + 1);

// com spread — TS valida o objeto resultante
setUsuario(u => u && { ...u, nome: "Novo" });
```

## useReducer — o tipo do estado e da action

```tsx
interface Estado {
  contador: number;
  historico: number[];
}

type Acao =
  | { type: "incrementar" }
  | { type: "decrementar" }
  | { type: "incrementarPor"; payload: number }
  | { type: "resetar" };

function reducer(state: Estado, action: Acao): Estado {
  switch (action.type) {
    case "incrementar":
      return { ...state, contador: state.contador + 1 };
    case "incrementarPor":
      return { ...state, contador: state.contador + action.payload };
    case "resetar":
      return { contador: 0, historico: [] };
    default:
      return state;
  }
}

const [estado, dispatch] = useReducer(reducer, { contador: 0, historico: [] });
dispatch({ type: "incrementarPor", payload: 5 }); // ✅ tipado
dispatch({ type: "inexistente" });                  // ❌ erro
```

## useRef — a referência tipada

```tsx
// DOM element
const inputRef = useRef<HTMLInputElement>(null);
inputRef.current?.focus();

// valor mutável
const contadorRef = useRef<number>(0);
contadorRef.current += 1;

// timer
const timerRef = useRef<NodeJS.Timeout | null>(null);
timerRef.current = setTimeout(() => {}, 1000);
```

## O estado no contexto — useContext tipado

```tsx
interface AuthContextType {
  usuario: Usuario | null;
  login: (email: string, senha: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("Fora do Provider");
  return ctx; // AuthContextType — nunca null aqui
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useState([])` sem tipo | `useState<Tipo[]>([])` — infere `never[]` |
| `useState(objeto)` sem tipo para props opcionais | `useState<Tipo \| null>(null)` |
| `useRef()` sem tipo | `useRef<HTMLInputElement>(null)` |
| Action sem union | `type Acao = { type: "a" } \| { type: "b" }` |

## Resumo

- `useState` infere de primitivos; explícito para arrays/objetos/null
- `T | null` é o padrão para dados que começam vazios
- `useReducer` tipa `state` e `action` — union de actions
- `useRef<HTMLInputElement>` para DOM; `useRef<T>` para valores
