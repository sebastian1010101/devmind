# FE05-66 — Atividade: Cadastro e Login com Zustand

## Objetivo

Sistema completo de autenticação com Zustand — cadastro, login, logout, proteção de rotas e persistência.

## A store de auth

```tsx
// store/useAuthStore.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { api } from "../services/api";

interface Usuario {
  id: number;
  nome: string;
  email: string;
}

interface AuthStore {
  usuario: Usuario | null;
  token: string | null;
  carregando: boolean;
  erro: string | null;
  login: (email: string, senha: string) => Promise<boolean>;
  cadastrar: (dados: Omit<Usuario, "id"> & { senha: string }) => Promise<boolean>;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      usuario: null,
      token: null,
      carregando: false,
      erro: null,

      login: async (email, senha) => {
        set({ carregando: true, erro: null });
        try {
          const res = await api.post("/login", { email, senha });
          set({ usuario: res.data.usuario, token: res.data.token });
          return true;
        } catch (e) {
          set({ erro: "Credenciais inválidas" });
          return false;
        } finally {
          set({ carregando: false });
        }
      },

      cadastrar: async (dados) => {
        set({ carregando: true, erro: null });
        try {
          const res = await api.post("/cadastro", dados);
          set({ usuario: res.data.usuario, token: res.data.token });
          return true;
        } catch (e) {
          set({ erro: e.response?.data?.message || "Erro ao cadastrar" });
          return false;
        } finally {
          set({ carregando: false });
        }
      },

      logout: () => set({ usuario: null, token: null })
    }),
    {
      name: "auth",
      partialize: (s) => ({ usuario: s.usuario, token: s.token })
    }
  )
);
```

## O interceptor com Zustand

```tsx
// services/api.ts — acessa a store fora do React
import { useAuthStore } from "../store/useAuthStore";

api.interceptors.request.use(config => {
  const { token } = useAuthStore.getState();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  res => res,
  erro => {
    if (erro.response?.status === 401) {
      useAuthStore.getState().logout(); // logout automático
    }
    return Promise.reject(erro);
  }
);
```

## O formulário de login

```tsx
const schema = z.object({
  email: z.string().email("Email inválido"),
  senha: z.string().min(6, "Mínimo 6 caracteres")
});

type FormLogin = z.infer<typeof schema>;

function Login() {
  const { login, carregando, erro } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const destino = location.state?.de || "/dashboard";

  const { register, handleSubmit, formState: { errors } } = useForm<FormLogin>({
    resolver: zodResolver(schema)
  });

  async function onSubmit(dados: FormLogin) {
    const ok = await login(dados.email, dados.senha);
    if (ok) navigate(destino, { replace: true });
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="email" {...register("email")} placeholder="Email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register("senha")} placeholder="Senha" />
      {errors.senha && <span>{errors.senha.message}</span>}

      {erro && <p className="erro">{erro}</p>}
      <button disabled={carregando}>
        {carregando ? "Entrando..." : "Entrar"}
      </button>
    </form>
  );
}
```

## Rota privada com Zustand

```tsx
function RotaPrivada({ children }: { children: ReactNode }) {
  const usuario = useAuthStore(s => s.usuario);
  const carregando = useAuthStore(s => s.carregando);
  const location = useLocation();

  if (carregando) return <p>Verificando...</p>;
  if (!usuario) {
    return <Navigate to="/login" state={{ de: location.pathname }} replace />;
  }
  return <>{children}</>;
}
```

## Header com auth

```tsx
function Header() {
  const usuario = useAuthStore(s => s.usuario);
  const logout = useAuthStore(s => s.logout);
  const navigate = useNavigate();

  return (
    <header>
      {usuario ? (
        <>
          <span>Olá, {usuario.nome}</span>
          <button onClick={() => { logout(); navigate("/login"); }}>
            Sair
          </button>
        </>
      ) : (
        <Link to="/login">Entrar</Link>
      )}
    </header>
  );
}
```

## Critérios de nivelamento

- `persist` com `partialize` — só usuario + token
- `login` retorna `Promise<boolean>` — o componente navega
- Interceptor de 401 faz logout automático
- Zod validando o formulário
- `RotaPrivada` espera `carregando` — sem flash
- `location.state.de` volta pra origem

## O fluxo completo

```text
1. App monta → persist restaura token + usuario
2. /dashboard → RotaPrivada checa usuario → ok
3. Request → interceptor injeta Bearer token
4. 401 → interceptor → logout() → Navigate /login
5. Login → POST → persiste → navigate(destino)
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `login` sem `return` | `Promise<boolean>` — o componente decide |
| `partialize` faltando | Persiste `carregando`/`erro` — lixo no storage |
| `useAuthStore()` sem seletor | `useAuthStore(s => s.usuario)` |
| 401 sem logout automático | Interceptor chama `logout()` |
