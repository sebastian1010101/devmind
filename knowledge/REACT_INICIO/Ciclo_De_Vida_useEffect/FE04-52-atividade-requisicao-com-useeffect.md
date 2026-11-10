# FE04-52 — Atividade: Executando uma requisição com useEffect

## Objetivo

Consolidar o padrão `useEffect + fetch` aplicado a um componente real: buscar dados na montagem, gerenciar estados e renderizar.

## A base — aula anterior, agora praticada

```jsx
import { useState, useEffect } from "react";

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function carregar() {
      try {
        const res = await fetch(
          "https://jsonplaceholder.typicode.com/users"
        );

        if (!res.ok) {
          throw new Error(`Erro ${res.status}`);
        }

        const dados = await res.json();
        setUsuarios(dados);
      } catch (e) {
        setErro(e.message);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, []);

  if (carregando) return <p>Carregando usuários...</p>;
  if (erro) return <p>Erro: {erro}</p>;

  return (
    <ul>
      {usuarios.map(u => (
        <li key={u.id}>
          <strong>{u.name}</strong> — {u.email}
        </li>
      ))}
    </ul>
  );
}
```

## Passo a passo

### 1. Os três estados

```jsx
const [usuarios, setUsuarios] = useState([]);      // dados
const [carregando, setCarregando] = useState(true); // loading
const [erro, setErro] = useState(null);            // erro
```

### 2. O efeito de montagem

```jsx
useEffect(() => {
  async function carregar() {
    // async aqui dentro — nunca no callback do useEffect
  }
  carregar();
}, []); // [] = só na montagem
```

### 3. O try/catch/finally

```jsx
try {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  const dados = await res.json();
  setUsuarios(dados);
} catch (e) {
  setErro(e.message);
} finally {
  setCarregando(false); // desliga loading SEMPRE — sucesso ou falha
}
```

### 4. Os três retornos condicionais

```jsx
if (carregando) return <p>Carregando...</p>;
if (erro) return <p>Erro: {erro}</p>;
return <ul>...</ul>; // dados — happy path por último
```

## Desafios extras

### Desafio A — detalhes de um usuário

```jsx
function UsuarioDetalhe({ id }) {
  const [usuario, setUsuario] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregar() {
      setCarregando(true); // reseta loading para o novo id
      const res = await fetch(
        `https://jsonplaceholder.typicode.com/users/${id}`
      );
      setUsuario(await res.json());
      setCarregando(false);
    }
    carregar();
  }, [id]); // ← depende do id — recarrega quando muda

  if (carregando) return <p>Carregando...</p>;
  return <p>{usuario.name}</p>;
}
```

### Desafio B — requisições paralelas

```jsx
useEffect(() => {
  async function carregar() {
    const [postsRes, usersRes] = await Promise.all([
      fetch("/posts"),
      fetch("/users")
    ]);
    setPosts(await postsRes.json());
    setUsers(await usersRes.json());
  }
  carregar();
}, []);
```

### Desafio C — AbortController (cancelar na desmontagem)

```jsx
useEffect(() => {
  const controller = new AbortController();

  async function carregar() {
    try {
      const res = await fetch(url, { signal: controller.signal });
      setDados(await res.json());
    } catch (e) {
      if (e.name !== "AbortError") setErro(e.message);
    }
  }

  carregar();
  return () => controller.abort(); // cancela se desmontar
}, []);
```

## O checklist da requisição

| Requisito | Por quê |
| --- | --- |
| `useEffect` com `[]` | Uma vez — não a cada render |
| `async` dentro, nunca no callback | `useEffect` não aceita Promise |
| `res.ok` antes de `.json()` | `fetch` não falha em 404 |
| `try/catch` | Rede cai, JSON quebra — trate |
| `finally` para loading | Desliga em sucesso E erro |
| `key` na lista | React precisa identificar cada item |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useEffect(async () => ...)` | `useEffect(() => { async function f(){...} f() }, [])` |
| Fetch sem `[]` | Loop infinito de requisições |
| `setState` sem verificar se montado | AbortController ou flag `isMounted` |
| `carregando` nunca desliga | `setCarregando(false)` no `finally` |
