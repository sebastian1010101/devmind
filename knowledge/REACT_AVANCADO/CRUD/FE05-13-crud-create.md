# FE05-13 — CRUD: Create (Criação)

## O fluxo de criação

```text
Formulário → validação → POST → resposta com id → setState adiciona → UI atualiza
```

## O formulário de criação

```jsx
function FormNota({ onCriar }) {
  const [titulo, setTitulo] = useState("");
  const [conteudo, setConteudo] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!titulo.trim()) {
      setErro("Título é obrigatório");
      return;
    }

    setEnviando(true);
    setErro(null);

    try {
      const res = await api.post("/notas", { titulo, conteudo });
      onCriar(res.data); // avisa o pai — com id da API
      setTitulo("");
      setConteudo("");
    } catch (e) {
      setErro("Erro ao criar nota");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={titulo}
        onChange={e => setTitulo(e.target.value)}
        placeholder="Título"
      />
      <textarea
        value={conteudo}
        onChange={e => setConteudo(e.target.value)}
        placeholder="Conteúdo"
      />
      {erro && <p className="erro">{erro}</p>}
      <button disabled={enviando}>
        {enviando ? "Salvando..." : "Criar nota"}
      </button>
    </form>
  );
}
```

## O pai adiciona ao estado

```jsx
function ListaNotas() {
  const [notas, setNotas] = useState([]);

  function adicionar(novaNota) {
    setNotas(atual => [novaNota, ...atual]); // no topo
  }

  return (
    <>
      <FormNota onCriar={adicionar} />
      {notas.map(n => <ItemNota key={n.id} nota={n} />)}
    </>
  );
}
```

A API retorna o objeto **com id gerado** — esse objeto vai pro estado.

## Form com objeto único

```jsx
const [form, setForm] = useState({ titulo: "", conteudo: "" });

function atualizar(campo, valor) {
  setForm(f => ({ ...f, [campo]: valor }));
}

await api.post("/notas", form); // envia o objeto inteiro
setForm({ titulo: "", conteudo: "" }); // reset
```

## Validação antes de enviar

```jsx
const erros = {};

if (!form.titulo.trim()) erros.titulo = "Obrigatório";
if (form.titulo.length > 100) erros.titulo = "Máx 100 caracteres";
if (!form.conteudo.trim()) erros.conteudo = "Obrigatório";

if (Object.keys(erros).length > 0) {
  setErros(erros);
  return;
}
```

## Estado de envio — UX do submit

```jsx
<button disabled={enviando || !titulo.trim()}>
  {enviando ? (
    <>
      <span className="spinner" />
      Salvando...
    </>
  ) : (
    "Criar nota"
  )}
</button>
```

Desabilitar previne **double submit** — usuário clicando 2x criando duas notas.

## ID temporário — criação otimista

```jsx
function adicionar(novaNota) {
  const tempId = Date.now(); // id temporário
  setNotas(atual => [{ ...novaNota, id: tempId }, ...atual]);

  api.post("/notas", novaNota)
    .then(res => {
      setNotas(atual =>
        atual.map(n => n.id === tempId ? res.data : n) // troca pelo real
      );
    })
    .catch(() => {
      setNotas(atual => atual.filter(n => n.id !== tempId)); // rollback
    });
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Push direto no array | `setNotas([...notas, nova])` — imutável |
| Form sem reset | Limpe os campos no sucesso |
| Botão sem `disabled` | Double submit cria duplicatas |
| Objeto sem id do backend | `res.data` — a API gera o id |
| Erro de validação no estado errado | Valide antes de enviar |

## Resumo

- Create = form → validação → `POST` → `res.data` (com id) → `setState` adiciona
- `enviando` desabilita o botão — previne double submit
- O objeto salvo no estado vem da API — com `id` e campos gerados
- Otimista usa id temporário e troca pelo real depois
