# FE04-35 — Atividade: Formulário de contato com estados

## Objetivo

Construir um formulário de contato completo com inputs controlados, validação e feedback de envio.

## O componente

```jsx
import { useState } from "react";

function FormContato() {
  const [form, setForm] = useState({
    nome: "",
    email: "",
    assunto: "",
    mensagem: ""
  });
  const [erros, setErros] = useState({});
  const [enviado, setEnviado] = useState(false);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));

    // Limpa o erro do campo ao digitar
    if (erros[name]) {
      setErros(prev => ({ ...prev, [name]: "" }));
    }
  }

  function validar() {
    const novosErros = {};

    if (!form.nome.trim()) {
      novosErros.nome = "Nome é obrigatório";
    }
    if (!form.email.includes("@")) {
      novosErros.email = "E-mail inválido";
    }
    if (!form.mensagem.trim()) {
      novosErros.mensagem = "Mensagem é obrigatória";
    }

    return novosErros;
  }

  function handleSubmit(e) {
    e.preventDefault();

    const novosErros = validar();
    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    // "Envio" — aqui seria uma chamada de API
    console.log("Enviando:", form);
    setEnviado(true);
    setForm({ nome: "", email: "", assunto: "", mensagem: "" });
  }

  if (enviado) {
    return (
      <div className="sucesso">
        <h2>✅ Mensagem enviada!</h2>
        <button onClick={() => setEnviado(false)}>Enviar outra</button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="campo">
        <label htmlFor="nome">Nome</label>
        <input
          id="nome"
          name="nome"
          value={form.nome}
          onChange={handleChange}
          className={erros.nome ? "erro" : ""}
        />
        {erros.nome && <span className="msg-erro">{erros.nome}</span>}
      </div>

      <div className="campo">
        <label htmlFor="email">E-mail</label>
        <input
          id="email"
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          className={erros.email ? "erro" : ""}
        />
        {erros.email && <span className="msg-erro">{erros.email}</span>}
      </div>

      <div className="campo">
        <label htmlFor="assunto">Assunto</label>
        <select
          id="assunto"
          name="assunto"
          value={form.assunto}
          onChange={handleChange}
        >
          <option value="">Selecione...</option>
          <option value="duvida">Dúvida</option>
          <option value="sugestao">Sugestão</option>
          <option value="suporte">Suporte</option>
        </select>
      </div>

      <div className="campo">
        <label htmlFor="mensagem">Mensagem</label>
        <textarea
          id="mensagem"
          name="mensagem"
          value={form.mensagem}
          onChange={handleChange}
          rows={5}
          className={erros.mensagem ? "erro" : ""}
        />
        {erros.mensagem && <span className="msg-erro">{erros.mensagem}</span>}
      </div>

      <button type="submit">Enviar</button>
    </form>
  );
}
```

## CSS para os erros

```css
.campo input.erro,
.campo textarea.erro {
  border-color: #e74c3c;
}

.msg-erro {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.25rem;
  display: block;
}
```

## Desafios extras

### Desafio A — validação em tempo real

```jsx
// Valida no onBlur — feedback antes do submit
<input
  onBlur={() => {
    if (!form.email.includes("@")) {
      setErros(prev => ({ ...prev, email: "E-mail inválido" }));
    }
  }}
/>
```

### Desafio B — contador de caracteres

```jsx
const MAX = 500;

<textarea
  maxLength={MAX}
  value={form.mensagem}
  onChange={handleChange}
/>
<span>{form.mensagem.length}/{MAX}</span>
```

### Desafio C — estado de envio

```jsx
const [enviando, setEnviando] = useState(false);

async function handleSubmit(e) {
  e.preventDefault();
  setEnviando(true);
  await enviarParaAPI(form);
  setEnviando(false);
  setEnviado(true);
}

<button disabled={enviando}>
  {enviando ? "Enviando..." : "Enviar"}
</button>
```

## Critérios de verificação

- Inputs controlados com `value` + `onChange`
- Objeto `form` único + `handleChange` genérico por `name`
- `e.preventDefault()` no submit
- Erros por campo com feedback visual
- Formulário limpa após envio bem-sucedido
- Estado `enviado` para tela de confirmação

## Erros comuns

| Erro | Correção |
| --- | --- |
| Input sem `name` no objeto | O `handleChange` genérico precisa do `name` |
| Erro persiste ao corrigir | Limpe `erros[name]` no `onChange` |
| `checked` em vez de `value` no select | Select usa `value`/`onChange` normal |
