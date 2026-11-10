# FE05-16 — CRUD: Delete (Exclusão)

## O fluxo de exclusão

```text
Botão remover → confirmação → DELETE → setState filtra → UI atualiza
```

## Delete básico

```jsx
async function remover(id) {
  try {
    await api.delete(`/notas/${id}`);
    setNotas(atual => atual.filter(n => n.id !== id));
  } catch (e) {
    setErro("Erro ao remover");
  }
}
```

`filter` remove do estado — a API confirma com `204`.

## Confirmação antes de deletar

```jsx
// Opção A — window.confirm (rápido)
async function remover(id) {
  if (!window.confirm("Excluir esta nota?")) return;
  await api.delete(`/notas/${id}`);
  setNotas(atual => atual.filter(n => n.id !== id));
}
```

```jsx
// Opção B — modal customizado
function ItemNota({ nota, onRemover }) {
  const [confirmando, setConfirmando] = useState(false);

  return (
    <>
      <button onClick={() => setConfirmando(true)}>Excluir</button>
      {confirmando && (
        <ModalConfirmacao
          mensagem={`Excluir "${nota.titulo}"?`}
          confirmar={() => { onRemover(nota.id); setConfirmando(false); }}
          cancelar={() => setConfirmando(false)}
        />
      )}
    </>
  );
}
```

## Delete com undo — a UX superior

```jsx
const [ultimoRemovido, setUltimoRemovido] = useState(null);

async function remover(id) {
  const removida = notas.find(n => n.id === id);
  setNotas(atual => atual.filter(n => n.id !== id));
  setUltimoRemovido(removida);

  // espera 5s — se não desfazer, deleta de verdade
  setTimeout(async () => {
    await api.delete(`/notas/${id}`);
    setUltimoRemovido(null);
  }, 5000);
}

function desfazer() {
  setNotas(atual => [ultimoRemovido, ...atual]);
  setUltimoRemovido(null); // cancela o delete real
}
```

```jsx
{ultimoRemovido && (
  <Toast>
    Nota removida
    <button onClick={desfazer}>Desfazer</button>
  </Toast>
)}
```

## Soft delete — não deletar de verdade

```jsx
// PATCH marca como deletada — não remove do banco
await api.patch(`/notas/${id}`, { deletada: true });
setNotas(atual => atual.filter(n => n.id !== id));

// lixeira
const lixeira = await api.get("/notas?deletada=true");
```

## Delete de múltiplos — seleção

```jsx
const [selecionados, setSelecionados] = useState([]);

async function removerSelecionados() {
  await Promise.all(
    selecionados.map(id => api.delete(`/notas/${id}`))
  );
  setNotas(atual => atual.filter(n => !selecionados.includes(n.id)));
  setSelecionados([]);
}
```

## Delete otimista

```jsx
async function remover(id) {
  const backup = notas;
  setNotas(atual => atual.filter(n => n.id !== id)); // some na hora

  try {
    await api.delete(`/notas/${id}`);
  } catch {
    setNotas(backup); // volta tudo se falhar
    setErro("Não foi possível excluir");
  }
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Delete sem confirmação | `confirm` ou modal — ação irreversível |
| `filter` com índice | `filter(n => n.id !== id)` — sempre por id |
| Delete otimista sem backup | Guarde o array anterior para rollback |
| Delete sem feedback | Toast ou mensagem — confirme visualmente |

## Resumo

- Delete = `DELETE /notas/${id}` → `setNotas(filter)`
- Confirmação antes — modal ou `confirm`
- Undo com toast é a UX mais amigável
- Soft delete preserva dados — `PATCH {deletada: true}`
- Otimista remove da UI primeiro, rollback no erro
