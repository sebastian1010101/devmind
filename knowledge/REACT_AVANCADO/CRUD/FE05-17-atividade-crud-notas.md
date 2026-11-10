# FE05-17 — Atividade: CRUD Completo para uma Lista de Notas

## Objetivo

Integrar as 4 operações num app completo: listar, criar, editar e remover notas — com Context centralizando o estado e as ações.

## A API (JSON Server ou similar)

```text
GET    /notas       → lista
POST   /notas       → cria { titulo, conteudo }
PUT    /notas/:id   → atualiza
DELETE /notas/:id   → remove
```

## O Context do CRUD

```jsx
// contexts/NotasContext.jsx
import { createContext, useState, useContext, useEffect, useCallback } from "react";
import { api } from "../services/api";

export const NotasContext = createContext(null);

export function NotasProvider({ children }) {
  const [notas, setNotas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  // READ — na montagem
  useEffect(() => {
    async function carregar() {
      try {
        const res = await api.get("/notas");
        setNotas(res.data);
      } catch {
        setErro("Erro ao carregar notas");
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, []);

  // CREATE
  const criar = useCallback(async (dados) => {
    const res = await api.post("/notas", dados);
    setNotas(atual => [res.data, ...atual]);
    return res.data;
  }, []);

  // UPDATE
  const atualizar = useCallback(async (id, dados) => {
    const res = await api.put(`/notas/${id}`, dados);
    setNotas(atual =>
      atual.map(n => n.id === id ? res.data : n)
    );
    return res.data;
  }, []);

  // DELETE
  const remover = useCallback(async (id) => {
    await api.delete(`/notas/${id}`);
    setNotas(atual => atual.filter(n => n.id !== id));
  }, []);

  return (
    <NotasContext.Provider value={{
      notas, carregando, erro,
      criar, atualizar, remover
    }}>
      {children}
    </NotasContext.Provider>
  );
}

export function useNotas() {
  const ctx = useContext(NotasContext);
  if (!ctx) throw new Error("useNotas deve estar dentro de NotasProvider");
  return ctx;
}
```

## Os componentes

### Lista

```jsx
function ListaNotas() {
  const { notas, carregando, erro, remover } = useNotas();
  const [editando, setEditando] = useState(null);

  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>{erro}</p>;

  return (
    <ul>
      {notas.map(n =>
        editando === n.id
          ? <FormEdicao key={n.id} nota={n} fechar={() => setEditando(null)} />
          : (
            <li key={n.id}>
              <h3>{n.titulo}</h3>
              <p>{n.conteudo}</p>
              <button onClick={() => setEditando(n.id)}>Editar</button>
              <button onClick={() => remover(n.id)}>Excluir</button>
            </li>
          )
      )}
    </ul>
  );
}
```

### Formulário de criação

```jsx
function FormNota() {
  const { criar } = useNotas();
  const [titulo, setTitulo] = useState("");
  const [conteudo, setConteudo] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setEnviando(true);
    try {
      await criar({ titulo, conteudo });
      setTitulo("");
      setConteudo("");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={titulo} onChange={e => setTitulo(e.target.value)} />
      <textarea value={conteudo} onChange={e => setConteudo(e.target.value)} />
      <button disabled={enviando}>Adicionar</button>
    </form>
  );
}
```

### Formulário de edição

```jsx
function FormEdicao({ nota, fechar }) {
  const { atualizar } = useNotas();
  const [titulo, setTitulo] = useState(nota.titulo);
  const [conteudo, setConteudo] = useState(nota.conteudo);

  async function salvar() {
    await atualizar(nota.id, { titulo, conteudo });
    fechar();
  }

  return (
    <div>
      <input value={titulo} onChange={e => setTitulo(e.target.value)} />
      <textarea value={conteudo} onChange={e => setConteudo(e.target.value)} />
      <button onClick={salvar}>Salvar</button>
      <button onClick={fechar}>Cancelar</button>
    </div>
  );
}
```

## A montagem

```jsx
function App() {
  return (
    <NotasProvider>
      <FormNota />
      <ListaNotas />
    </NotasProvider>
  );
}
```

## O mapa das operações

| Ação | Contexto | API | Estado |
| --- | --- | --- | --- |
| Montar | `useEffect` inicial | `GET` | `setNotas(res.data)` |
| Criar | `criar()` | `POST` | `[res.data, ...atual]` |
| Editar | `atualizar()` | `PUT` | `map` substitui |
| Remover | `remover()` | `DELETE` | `filter` remove |

## Desafios extras

### Desafio A — busca em tempo real

```jsx
const [busca, setBusca] = useState("");
const filtradas = notas.filter(n =>
  n.titulo.toLowerCase().includes(busca.toLowerCase())
);
```

### Desafio B — confirmação de exclusão

```jsx
async function removerComConfirmacao(id) {
  if (window.confirm("Excluir?")) await remover(id);
}
```

### Desafio C — persistência local

```jsx
// fallback se a API falhar — localStorage como cache
useEffect(() => {
  localStorage.setItem("notas", JSON.stringify(notas));
}, [notas]);
```

## Critérios de verificação

- As 4 operações no Context — componentes só chamam actions
- `useCallback` nas actions para estabilidade
- Edição inline com `editando` controlando qual item
- Formulário reseta após criar
- Loading e erro cobertos na lista

## Erros comuns

| Erro | Correção |
| --- | --- |
| Estado duplicado (Context + local) | O Context é a fonte — componentes consomem |
| Actions sem `useCallback` | Referências novas a cada render |
| Edição sem pre-fill | `useState(nota.campo)` — valor atual |
| Delete sem confirmar | `window.confirm` ou modal |
