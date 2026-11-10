# FE05-40 — Redux: Autenticação com Redux e Thunk — Parte 2

## O componente de Login completo

```jsx
function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const { carregando, erro } = useSelector(s => s.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const destino = location.state?.de || "/dashboard";

  async function handleSubmit(e) {
    e.preventDefault();
    const sucesso = await dispatch(login(email, senha));
    if (sucesso) navigate(destino, { replace: true });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={senha} onChange={e => setSenha(e.target.value)} />
      {erro && <p className="erro">{erro}</p>}
      <button disabled={carregando}>
        {carregando ? "Entrando..." : "Entrar"}
      </button>
    </form>
  );
}
```

## A rota protegida com Redux

```jsx
function RotaPrivada({ children }) {
  const { usuario, carregando } = useSelector(s => s.auth);
  const location = useLocation();

  if (carregando) return <p>Verificando...</p>;
  if (!usuario) {
    return <Navigate to="/login" state={{ de: location.pathname }} replace />;
  }
  return children;
}
```

## O Header com auth

```jsx
function Header() {
  const { usuario } = useSelector(s => s.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  function handleLogout() {
    dispatch(logout());
    navigate("/login");
  }

  return (
    <header>
      {usuario ? (
        <>
          <span>Olá, {usuario.nome}</span>
          <button onClick={handleLogout}>Sair</button>
        </>
      ) : (
        <Link to="/login">Entrar</Link>
      )}
    </header>
  );
}
```

## Verificação de sessão no App

```jsx
function App() {
  const dispatch = useDispatch();
  const { carregando } = useSelector(s => s.auth);

  useEffect(() => {
    dispatch(verificarSessao());
  }, [dispatch]);

  if (carregando) return <Loading />; // espera restaurar

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<RotasPrivadas />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/perfil" element={<Perfil />} />
      </Route>
    </Routes>
  );
}
```

## O 401 — logout automático

```jsx
// services/api.js
api.interceptors.response.use(
  res => res,
  erro => {
    if (erro.response?.status === 401) {
      store.dispatch({ type: AUTH.LOGOUT });
      localStorage.removeItem("token");
    }
    return Promise.reject(erro);
  }
);
```

Token expirado → 401 → Redux despacha logout → componentes reagem.

## O seletor de auth — hook customizado

```jsx
// hooks/useAuth.js — mesmo nome do Context, mas via Redux
export function useAuth() {
  const usuario = useSelector(s => s.auth.usuario);
  const carregando = useSelector(s => s.auth.carregando);
  const erro = useSelector(s => s.auth.erro);
  return { usuario, carregando, erro };
}
```

```jsx
function Header() {
  const { usuario } = useAuth(); // limpo
}
```

## Persistência — restaurar no load

```jsx
// authReducer — estado inicial lê o storage
const inicial = {
  usuario: JSON.parse(localStorage.getItem("usuario") || "null"),
  token: localStorage.getItem("token"),
  carregando: true, // até verificar
  erro: null
};
```

## O fluxo completo

```text
App monta
  → dispatch(verificarSessao())
  → token no storage? → GET /me
  → sucesso → SESSAO_RESTAURADA → usuario no estado
  → falha → logout() → limpa tudo

Login:
  → dispatch(login(email, senha))
  → POST /login → token + usuario
  → localStorage salva
  → LOGIN_SUCESSO → navigate(destino)
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `carregando` não cobre a restauração | `inicial.carregando = true` |
| 401 sem logout | Interceptor despacha `LOGOUT` |
| `useAuth` importando Context errado | Hook customizado via `useSelector` |
| `navigate` antes do dispatch | `await dispatch(login(...))` primeiro |

## Resumo

- `verificarSessao` roda na montagem — restaura ou limpa
- `RotaPrivada` espera `carregando` — sem flash de login
- Interceptor 401 despacha logout automático
- `useAuth` customizado encapsula os seletores
