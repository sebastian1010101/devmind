# FE05-06 — Autenticação: Parte 1

## O que é autenticação em frontend

Verificar **quem é o usuário** e manter essa identidade entre requisições. No React, envolve: login → receber token → guardar token → enviar em requisições → proteger rotas.

## O fluxo básico

```text
1. Usuário digita email + senha
2. POST /login → servidor valida
3. Servidor devolve { token, usuario }
4. Frontend salva token (localStorage)
5. Requisições futuras levam Authorization: Bearer token
6. Servidor valida o token → responde dados protegidos
```

## O token JWT

JSON Web Token — string assinada que prova identidade:

```text
eyJhbGciOi... . eyJzdWIiOiIxMj... . SflKxwRJ...
   header        payload         assinatura
```

O payload contém dados do usuário (id, email, expiração) — **legível por qualquer um**, mas impossível de falsificar sem a chave do servidor.

## Onde guardar o token

| Local | Prós | Contras |
| --- | --- | --- |
| `localStorage` | Persiste, simples | Vulnerável a XSS |
| Cookie `httpOnly` | Imune a XSS | Precisa de backend configurado |
| `sessionStorage` | Morre ao fechar | Sessão curta |
| Memória (state) | Mais seguro | Some ao recarregar |

Para estudo: `localStorage` é o padrão. Produção séria: `httpOnly` cookie.

## O formulário de login

```jsx
function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState(null);
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setCarregando(true);
    setErro(null);

    try {
      const res = await api.post("/login", { email, senha });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("usuario", JSON.stringify(res.data.usuario));
      // redirecionar para área logada
    } catch (e) {
      setErro("Email ou senha inválidos");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={senha} onChange={e => setSenha(e.target.value)} />
      {erro && <p className="erro">{erro}</p>}
      <button disabled={carregando}>Entrar</button>
    </form>
  );
}
```

## Enviando o token — interceptor do Axios

```javascript
// services/api.js
api.interceptors.request.use(config => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

Toda requisição sai autenticada automaticamente.

## Estado da autenticação

```jsx
const [usuario, setUsuario] = useState(() => {
  try {
    const salvo = localStorage.getItem("usuario");
    return salvo ? JSON.parse(salvo) : null;
  } catch {
    return null;
  }
});
```

`usuario === null` → não logado. `usuario` com dados → logado.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Senha em texto puro no localStorage | **Nunca** — só o token |
| Token sem prefixo `Bearer` | `Authorization: Bearer ${token}` |
| Guardar o token mas não o usuário | Salve ambos — ou decodifique o JWT |
| Login sem feedback de erro | Estado `erro` + mensagem clara |

## Resumo

- Auth: login → token → guardar → enviar em requisições → proteger rotas
- JWT é legível mas não falsificável — payload com dados do usuário
- `localStorage` para estudo; `httpOnly` cookie para produção
- Interceptor do Axios adiciona o token em toda requisição
