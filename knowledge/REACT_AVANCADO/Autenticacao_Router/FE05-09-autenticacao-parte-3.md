# FE05-09 — Autenticação: Parte 3 — Rotas Protegidas

## Rotas privadas — o componente de guarda

Páginas que exigem login precisam de **verificação antes de renderizar**. O padrão: um componente que checa o auth e redireciona.

```jsx
// components/RotaPrivada.jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

function RotaPrivada({ children }) {
  const { usuario, carregando } = useAuth();

  if (carregando) {
    return <p>Verificando...</p>; // espera a sessão restaurar
  }

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
```

## Aplicando nas rotas

```jsx
<Routes>
  {/* Públicas */}
  <Route path="/login" element={<Login />} />
  <Route path="/cadastro" element={<Cadastro />} />

  {/* Privadas — qualquer nível */}
  <Route
    path="/dashboard"
    element={
      <RotaPrivada>
        <Dashboard />
      </RotaPrivada>
    }
  />
</Routes>
```

## Com Outlet — protegendo um grupo

```jsx
function RotasPrivadas() {
  const { usuario, carregando } = useAuth();

  if (carregando) return <p>Carregando...</p>;
  if (!usuario) return <Navigate to="/login" replace />;

  return <Outlet />; // todas as filhas protegidas
}
```

```jsx
<Routes>
  <Route path="/login" element={<Login />} />

  <Route element={<RotasPrivadas />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/perfil" element={<Perfil />} />
    <Route path="/config" element={<Config />} />
  </Route>
</Routes>
```

Um guarda protege **todas** as rotas do grupo.

## Redirecionando de volta — o `state` do Navigate

```jsx
// Na RotaPrivada — guarda de onde veio
<Navigate to="/login" state={{ de: location.pathname }} replace />

// No Login — volta depois de autenticar
const location = useLocation();
const navigate = useNavigate();

const destino = location.state?.de || "/dashboard";
await login(email, senha);
navigate(destino, { replace: true });
```

## Rotas públicas exclusivas — anti-login

Usuário logado não deve ver `/login` de novo:

```jsx
function RotaPublica({ children }) {
  const { usuario } = useAuth();

  if (usuario) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

<Route
  path="/login"
  element={
    <RotaPublica>
      <Login />
    </RotaPublica>
  }
/>
```

## Permissões por papel (roles)

```jsx
function RotaAdmin({ children }) {
  const { usuario } = useAuth();

  if (!usuario) return <Navigate to="/login" />;
  if (usuario.role !== "admin") return <Navigate to="/dashboard" />;

  return children;
}
```

## O fluxo completo

```text
Usuário não logado → /dashboard
  → RotaPrivada detecta usuario null
  → Navigate /login (guarda de onde veio)
  → Login ok → navigate(destino)
  → Volta pra /dashboard
```

## Verificação no backend

Frontend protege a **UI** — mas quem garante os dados é o servidor:

```jsx
// O token vai na requisição — o backend valida
api.interceptors.request.use(config => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// 401 → token expirou → força logout
api.interceptors.response.use(
  res => res,
  erro => {
    if (erro.response?.status === 401) {
      localStorage.clear();
      window.location.href = "/login";
    }
    return Promise.reject(erro);
  }
);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Guarda sem `carregando` | Flash de login antes da sessão restaurar |
| Rota privada sem guarda | Proteja com `RotaPrivada` ou grupo + `Outlet` |
| Redirecionamento sem `replace` | Voltar fica preso no login |
| Proteção só no frontend | Backend valida o token — UI é só UX |

## Resumo

- `RotaPrivada` checa `useAuth` e redireciona se não logado
- `Outlet` protege grupos inteiros de rotas
- `location.state.de` guarda a origem para voltar depois do login
- Guarda de UI ≠ segurança — o backend valida o token
