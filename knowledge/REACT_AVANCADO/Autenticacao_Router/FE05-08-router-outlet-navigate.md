# FE05-08 — React Router DOM: Outlet e Navigate

## React Router — a base

Biblioteca padrão de rotas em React — SPA com navegação sem recarregar.

```bash
npm install react-router-dom
```

```jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";

<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/produtos" element={<Produtos />} />
    <Route path="/produtos/:id" element={<Detalhe />} />
    <Route path="*" element={<NaoEncontrado />} />
  </Routes>
</BrowserRouter>
```

## Outlet — layout com rotas aninhadas

`Outlet` é onde a **rota filha** renderiza — o layout pai fica fixo:

```jsx
function Layout() {
  return (
    <div>
      <Header />
      <nav>...</nav>
      <Outlet /> {/* ← a rota filha renderiza aqui */}
      <Footer />
    </div>
  );
}

<Routes>
  <Route element={<Layout />}>
    <Route path="/" element={<Home />} />
    <Route path="/produtos" element={<Produtos />} />
    <Route path="/sobre" element={<Sobre />} />
  </Route>
</Routes>
```

Header e Footer não remontam — só o `Outlet` troca.

## Rotas aninhadas profundas

```jsx
<Route path="/dashboard" element={<Dashboard />}>
  <Route index element={<Resumo />} />          {/* /dashboard */}
  <Route path="perfil" element={<Perfil />} />   {/* /dashboard/perfil */}
  <Route path="config" element={<Config />} />   {/* /dashboard/config */}
</Route>
```

```jsx
function Dashboard() {
  return (
    <div>
      <SidebarDashboard />
      <Outlet /> {/* Resumo/Perfil/Config renderizam aqui */}
    </div>
  );
}
```

## Navigate — redirecionamento declarativo

```jsx
// Redireciona na montagem
<Route path="/" element={<Navigate to="/dashboard" replace />} />

// Condicional — proteção de rota
{!usuario && <Navigate to="/login" replace />}
```

`replace` não deixa a rota no histórico — voltar não fica preso.

## useNavigate — redirecionamento imperativo

```jsx
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    await login(...);
    navigate("/dashboard"); // redireciona após login
    navigate(-1);           // volta uma página
    navigate("/", { replace: true }); // sem histórico
  }
}
```

## Link e NavLink

```jsx
import { Link, NavLink } from "react-router-dom";

<Link to="/produtos">Produtos</Link>

<NavLink
  to="/produtos"
  className={({ isActive }) => isActive ? "ativo" : ""}
>
  Produtos
</NavLink>
```

`NavLink` sabe se está ativo — estilização automática.

## useParams — parâmetros da URL

```jsx
// Rota: /produtos/:id
<Route path="/produtos/:id" element={<Detalhe />} />

function Detalhe() {
  const { id } = useParams(); // "42" da URL
  // fetch(`/api/produtos/${id}`)
}
```

## useSearchParams — query string

```jsx
// URL: /produtos?categoria=eletronicos&page=2
const [searchParams] = useSearchParams();
searchParams.get("categoria"); // "eletronicos"
searchParams.get("page");      // "2"
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `<a href>` em vez de `Link` | Recarrega a página — SPA quebra |
| `navigate` fora de evento/efeito | `Navigate` declarativo no JSX |
| `*` sem estar por último | Rota coringa captura tudo |
| `useParams` retorna string | `Number(id)` se precisa de número |

## Resumo

- `Outlet` renderiza a rota filha dentro do layout pai
- `Navigate` redireciona no JSX; `useNavigate` em código
- `NavLink` marca a rota ativa
- `useParams`/`useSearchParams` leem a URL
