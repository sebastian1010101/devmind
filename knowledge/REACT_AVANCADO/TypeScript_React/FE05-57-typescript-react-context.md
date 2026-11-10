# FE05-57 — TypeScript no React: Context

## O Context tipado — createContext

```tsx
interface AuthContextType {
  usuario: Usuario | null;
  carregando: boolean;
  login: (email: string, senha: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);
//                                 ↑ pode ser null — sem Provider
```

## O Provider com valor tipado

```tsx
export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(true);

  async function login(email: string, senha: string): Promise<boolean> {
    const res = await api.post("/login", { email, senha });
    setUsuario(res.data.usuario);
    return true;
  }

  function logout() {
    setUsuario(null);
    localStorage.removeItem("token");
  }

  return (
    <AuthContext.Provider value={{ usuario, carregando, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

## O hook customizado — o guarda

```tsx
export function useAuth() {
  const contexto = useContext(AuthContext);

  if (!contexto) {
    throw new Error("useAuth deve estar dentro de AuthProvider");
  }

  return contexto; // AuthContextType — nunca null aqui
}
```

```tsx
// componente — seguro, sem null check
function Header() {
  const { usuario, logout } = useAuth();
  return usuario ? <button onClick={logout}>Sair</button> : null;
}
```

## Context com valor padrão — sem Provider

```tsx
// quando faz sentido ter default — sem Provider
const TemaContext = createContext<"claro" | "escuro">("claro");

// uso direto — mesmo sem Provider, retorna "claro"
const tema = useContext(TemaContext);
```

## O tema completo — contexto mais Provider

```tsx
interface TemaContextType {
  tema: "claro" | "escuro";
  alternar: () => void;
}

const TemaContext = createContext<TemaContextType | null>(null);

export function TemaProvider({ children }: { children: ReactNode }) {
  const [tema, setTema] = useState<"claro" | "escuro">("claro");
  const alternar = () => setTema(t => t === "claro" ? "escuro" : "claro");

  return (
    <TemaContext.Provider value={{ tema, alternar }}>
      {children}
    </TemaContext.Provider>
  );
}

export function useTema() {
  const ctx = useContext(TemaContext);
  if (!ctx) throw new Error("useTema fora do Provider");
  return ctx;
}
```

## Context de lista — CRUD tipado

```tsx
interface NotasContextType {
  notas: Nota[];
  criar: (dados: Omit<Nota, "id">) => Promise<Nota>;
  atualizar: (id: number, dados: Partial<Nota>) => Promise<Nota>;
  remover: (id: number) => Promise<void>;
  carregando: boolean;
}

const NotasContext = createContext<NotasContextType | null>(null);
```

`Omit` e `Partial` reutilizam o tipo `Nota` — sem duplicar.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `createContext()` sem generic | `createContext<Tipo \| null>(null)` |
| `useContext` retornando null | Hook customizado com throw |
| `value` sem `useMemo` | `useMemo(() => ({...}), [...])` |
| Context com `any` | Interface do contexto |

## Resumo

- `createContext<Tipo | null>(null)` — pode ser sem Provider
- Hook `useX` com `throw` — valida o Provider cedo
- `Omit`/`Partial` para actions de CRUD — sem duplicar tipos
- `useMemo` no `value` — performance
