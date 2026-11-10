# FE04-34 — Estado: Formulários

## Inputs controlados

Em React, o input é **controlado pelo estado**: o valor exibido vem do estado, e cada tecla atualiza o estado via `onChange`.

```jsx
function Formulario() {
  const [nome, setNome] = useState("");

  return (
    <input
      value={nome}                          // valor vem do estado
      onChange={(e) => setNome(e.target.value)} // estado atualiza a cada tecla
    />
  );
}
```

O ciclo: usuário digita → `onChange` → `setNome` → re-render → `value` atualizado. O estado é a **fonte única de verdade** — o input nunca tem um valor que o estado não conheça.

## Um estado por campo

```jsx
const [nome, setNome] = useState("");
const [email, setEmail] = useState("");
const [mensagem, setMensagem] = useState("");
```

```jsx
<form>
  <input value={nome} onChange={e => setNome(e.target.value)} />
  <input value={email} onChange={e => setEmail(e.target.value)} />
  <textarea value={mensagem} onChange={e => setMensagem(e.target.value)} />
</form>
```

## Objeto único para formulários maiores

Com muitos campos, um objeto de estado + handler genérico escala melhor:

```jsx
const [form, setForm] = useState({
  nome: "",
  email: "",
  telefone: ""
});

function handleChange(e) {
  const { name, value } = e.target;
  setForm(prev => ({ ...prev, [name]: value }));
}
```

```jsx
<input name="nome" value={form.nome} onChange={handleChange} />
<input name="email" value={form.email} onChange={handleChange} />
<input name="telefone" value={form.telefone} onChange={handleChange} />
```

O `[name]: value` usa o atributo `name` do input como chave — um handler serve a todos.

## Checkbox, select e radio

```jsx
const [aceito, setAceito] = useState(false);
const [cor, setCor] = useState("azul");

// Checkbox — usa .checked, não .value
<input type="checkbox" checked={aceito} onChange={e => setAceito(e.target.checked)} />

// Select — value normal
<select value={cor} onChange={e => setCor(e.target.value)}>
  <option value="azul">Azul</option>
  <option value="verde">Verde</option>
</select>

// Radio — compara o value
<input
  type="radio"
  name="plano"
  value="basico"
  checked={plano === "basico"}
  onChange={e => setPlano(e.target.value)}
/>
```

## Submit com preventDefault

```jsx
function handleSubmit(e) {
  e.preventDefault(); // impede o reload da página
  console.log(form);  // dados prontos para enviar
}

<form onSubmit={handleSubmit}>
```

## Validação básica

```jsx
function handleSubmit(e) {
  e.preventDefault();

  if (!form.nome.trim()) {
    setErro("Nome é obrigatório");
    return;
  }

  if (!form.email.includes("@")) {
    setErro("E-mail inválido");
    return;
  }

  enviar(form);
}
```

## Controlado vs não-controlado

| | Controlado | Não-controlado |
| --- | --- | --- |
| Fonte de verdade | Estado React | O próprio DOM |
| Valor | `value={estado}` | Lido via `useRef` |
| Validação em tempo real | Fácil | Difícil |
| Uso recomendado | Padrão | Casos específicos |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `value` sem `onChange` | Input fica travado — warning "controlled without onChange" |
| `defaultValue` vs `value` | `defaultValue` é não-controlado; `value` é controlado |
| `e.target.value` em checkbox | Checkbox usa `e.target.checked` |
| Form que recarrega a página | `e.preventDefault()` no `onSubmit` |

## Resumo

- Input controlado: `value={estado}` + `onChange={setEstado}`
- Objeto único + `handleChange` genérico para formulários grandes
- Checkbox/radio usam `checked`; select usa `value`
- `preventDefault` no submit — nunca deixe o form recarregar
