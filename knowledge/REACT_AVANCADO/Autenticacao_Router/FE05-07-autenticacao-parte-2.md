# FE05-07 — Autenticação: Parte 2

## Context de autenticação — o padrão

O estado de login precisa estar **global** — Header, rotas, formulários todos consomem. O `AuthContext` centraliza.

```jsx
// contexts/AuthContext.jsx
import { createContext, useState, useContext, useEffect } from "react";
import { api } from "../services/api";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [carregando, setCarregando] = useState(true);

  // Na montagem: restaura sessão salva
  useEffect(() => {
    try {
      const salvo = localStorage.getItem("usuario");
      if (salvo) setUsuario(JSON.parse(salvo));
    } finally {
      setCarregando(false);
    }
  }, []);

  async function login(email, senha) {
    const res = await api.post("/login", { email, senha });
    const { token, usuario: dados } = res.data;

    localStorage.setItem("token", token);
    localStorage.setItem("usuario", JSON.stringify(dados));
    setUsuario(dados);
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    setUsuario(null);
  }

  return (
    <AuthContext.Provider value={{ usuario, carregando, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve estar dentro de AuthProvider");
  return ctx;
}
```

## O formulário usando o contexto

```jsx
function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await login(email, senha); // o contexto faz tudo
      navigate("/dashboard");
    } catch {
      setErro("Credenciais inválidas");
    }
  }
}
```

O formulário não sabe sobre localStorage — o `AuthContext` abstrai.

## Restaurando sessão — o `carregando`

```jsx
function App() {
  const { carregando } = useAuth();

  if (carregando) return <p>Verificando sessão...</p>;

  return <Rotas />;
}
```

Sem isso: página recarrega → `usuario` ainda `null` → redireciona pro login mesmo com token válido.

## Validação do token no carregamento

Token pode estar expirado — valide com o servidor:

```jsx
useEffect(() => {
  async function verificar() {
    const token = localStorage.getItem("token");
    if (!token) {
      setCarregando(false);
      return;
    }

    try {
      const res = await api.get("/me"); // endpoint que valida
      setUsuario(res.data);
    } catch {
      logout(); // token inválido — limpa
    } finally {
      setCarregando(false);
    }
  }
  verificar();
}, []);
```

## Logout — limpando tudo

```jsx
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario");
  setUsuario(null);
  // opcional: navigate("/login")
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `carregando` não controlado | Tela pisca — login → app → login |
| Token expirado ignorado | Chame `/me` ou valide `exp` do JWT |
| Logout que não limpa storage | Remova token E usuário |
| `useAuth` fora do Provider | Erro cedo com throw no hook |

## Resumo

- `AuthContext` centraliza `usuario`, `login`, `logout`, `carregando`
- Restauração de sessão na montagem — evita flash de login
- Validação com `/me` detecta token expirado
- `login()` no contexto abstrai localStorage dos componentes
