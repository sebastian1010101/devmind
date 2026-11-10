# FE05-12 — CRUD: Introdução

## O que é CRUD

As quatro operações fundamentais de qualquer app com dados:

| Letra | Operação | HTTP | Exemplo |
| --- | --- | --- | --- |
| **C**reate | Criar | `POST` | Nova nota |
| **R**ead | Ler | `GET` | Listar notas |
| **U**pdate | Atualizar | `PUT`/`PATCH` | Editar nota |
| **D**elete | Deletar | `DELETE` | Remover nota |

Todo app de verdade é CRUD: produtos, usuários, posts, tarefas.

## As duas camadas do CRUD no React

```text
API (servidor)          Estado React (UI)
      │                        │
POST /notas          →  setNotas([...notas, nova])
GET  /notas          →  setNotas(dados)
PUT  /notas/:id      →  setNotas(map(...))
DELETE /notas/:id    →  setNotas(filter(...))
```

**Duas atualizações** sempre: a API (persiste) e o estado local (mostra na tela).

## O padrão de estado para CRUD

```jsx
const [itens, setItens] = useState([]);

// CREATE — adiciona ao estado
function criar(novo) {
  api.post("/notas", novo).then(res => {
    setItens(atual => [...atual, res.data]);
  });
}

// READ — carrega na montagem
useEffect(() => {
  api.get("/notas").then(res => setItens(res.data));
}, []);

// UPDATE — substitui o item alterado
function atualizar(id, dados) {
  api.put(`/notas/${id}`, dados).then(res => {
    setItens(atual =>
      atual.map(i => i.id === id ? res.data : i)
    );
  });
}

// DELETE — filtra fora
function remover(id) {
  api.delete(`/notas/${id}`).then(() => {
    setItens(atual => atual.filter(i => i.id !== id));
  });
}
```

## Otimista vs pessimista

```javascript
// Pessimista — espera a API confirmar
await api.delete(`/notas/${id}`);
setItens(atual => atual.filter(i => i.id !== id));

// Otimista — atualiza UI primeiro, rollback se falhar
setItens(atual => atual.filter(i => i.id !== id));
try {
  await api.delete(`/notas/${id}`);
} catch {
  setItens(itensAntigos); // desfaz
}
```

Otimista parece mais rápido; pessimista é mais seguro.

## Estrutura típica de um CRUD React

```text
src/
├── contexts/NotasContext.jsx   ← estado + ações CRUD
├── components/
│   ├── ListaNotas.jsx          ← Read
│   ├── FormNota.jsx            ← Create
│   ├── ItemNota.jsx            ← Update/Delete inline
│   └── ModalEdicao.jsx         ← Update em modal
└── services/api.js
```

## O contrato com a API

```javascript
// O que a API espera vs devolve
POST   /notas       { titulo, conteudo }   → 201 { id, titulo, conteudo, criadaEm }
GET    /notas                                → 200 [ { id, titulo, ... } ]
GET    /notas/:id                            → 200 { id, titulo, ... }
PUT    /notas/:id   { titulo, conteudo }   → 200 { id, titulo, ... }
DELETE /notas/:id                           → 204 (sem body)
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Só atualizar a API | Estado local precisa refletir — `setItens` |
| Só atualizar o estado | Dados somem ao recarregar — persista na API |
| `id` undefined no update/delete | Confirme que o item tem `id` da API |
| Form sem reset após criar | `setForm({})` no sucesso |

## Resumo

- CRUD = Create/Read/Update/Delete — base de todo app com dados
- Cada operação atualiza API **e** estado local
- Context ou hook customizado centralizam as 4 ações
- Otimista (UI primeiro) vs pessimista (API primeiro) — trade-off de UX vs segurança
