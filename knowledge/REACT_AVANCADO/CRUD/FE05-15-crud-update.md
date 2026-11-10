# FE05-15 — CRUD: Update (Atualização)

## O fluxo de atualização

```text
Item clicado → formulário pré-preenchido → PUT/PATCH → resposta atualizada → setState substitui
```

## PUT vs PATCH

| | PUT | PATCH |
| --- | --- | --- |
| Envio | Objeto completo | Só campos alterados |
| Uso | Edição de formulário inteiro | Toggle, campo único |

```javascript
await api.put(`/notas/${id}`, { titulo, conteudo });      // completo
await api.patch(`/notas/${id}`, { arquivada: true });     // parcial
```

## Edição inline — o padrão mais simples

```jsx
function ItemNota({ nota, onAtualizar }) {
  const [editando, setEditando] = useState(false);
  const [titulo, setTitulo] = useState(nota.titulo);

  async function salvar() {
    const res = await api.put(`/notas/${nota.id}`, {
      ...nota,
      titulo
    });
    onAtualizar(res.data);
    setEditando(false);
  }

  if (editando) {
    return (
      <div>
        <input value={titulo} onChange={e => setTitulo(e.target.value)} />
        <button onClick={salvar}>Salvar</button>
        <button onClick={() => setEditando(false)}>Cancelar</button>
      </div>
    );
  }

  return (
    <div>
      <h3>{nota.titulo}</h3>
      <button onClick={() => setEditando(true)}>Editar</button>
    </div>
  );
}
```

## O pai substitui no estado

```jsx
function atualizarNota(notaAtualizada) {
  setNotas(atual =>
    atual.map(n => n.id === notaAtualizada.id ? notaAtualizada : n)
  );
}

<ItemNota nota={n} onAtualizar={atualizarNota} />
```

`map` troca o item pelo que veio da API — mantém ordem e referências.

## Modal de edição

```jsx
function ModalEdicao({ nota, fechar, onSalvar }) {
  const [form, setForm] = useState({
    titulo: nota.titulo,
    conteudo: nota.conteudo
  });

  async function handleSubmit(e) {
    e.preventDefault();
    const res = await api.put(`/notas/${nota.id}`, form);
    onSalvar(res.data);
    fechar();
  }

  return (
    <div className="modal-overlay" onClick={fechar}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <form onSubmit={handleSubmit}>
          <input
            value={form.titulo}
            onChange={e => setForm(f => ({ ...f, titulo: e.target.value }))}
          />
          <textarea
            value={form.conteudo}
            onChange={e => setForm(f => ({ ...f, conteudo: e.target.value }))}
          />
          <button>Salvar</button>
        </form>
      </div>
    </div>
  );
}
```

## Toggle — PATCH de campo único

```jsx
async function alternarArquivada(nota) {
  const res = await api.patch(`/notas/${nota.id}`, {
    arquivada: !nota.arquivada
  });
  atualizarNota(res.data);
}

<input
  type="checkbox"
  checked={nota.arquivada}
  onChange={() => alternarArquivada(nota)}
/>
```

## Estado de edição no pai — qual item edita

```jsx
const [editandoId, setEditandoId] = useState(null);

{notas.map(n =>
  editandoId === n.id
    ? <FormEdicao key={n.id} nota={n} fechar={() => setEditandoId(null)} />
    : <ItemNota key={n.id} nota={n} editar={() => setEditandoId(n.id)} />
)}
```

## Atualização otimista

```jsx
async function alternar(nota) {
  const otimista = { ...nota, arquivada: !nota.arquivada };
  atualizarNota(otimista); // UI primeiro

  try {
    await api.patch(`/notas/${nota.id}`, { arquivada: otimista.arquivada });
  } catch {
    atualizarNota(nota); // rollback se falhar
  }
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `map` trocando sem `id` | `n.id === atualizada.id` — match pelo id |
| Form sem pre-fill | `useState(nota.titulo)` — começa com o valor atual |
| PUT sem campos não editados | `{...nota, campo}` — preserva o resto |
| Editando todos ao clicar | `editandoId` — controla qual está aberto |
| `setEditando(false)` antes do salvar | Só depois do sucesso — ou mantém aberto no erro |

## Resumo

- Update = form pré-preenchido → `PUT`/`PATCH` → `setState` com `map`
- `PUT` envia tudo; `PATCH` só o que mudou
- Edição inline ou modal — o pai substitui pelo `id`
- Otimista atualiza UI primeiro, rollback no erro
