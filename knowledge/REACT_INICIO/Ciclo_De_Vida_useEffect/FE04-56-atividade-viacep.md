# FE04-56 — Atividade: Consumindo a API do ViaCEP

## Objetivo

Integrar uma API pública real — **ViaCEP** — buscando endereços por CEP digitado pelo usuário. Pratica `useEffect` com dependências, validação de input e estados de loading/erro.

## A API do ViaCEP

```text
GET https://viacep.com.br/ws/{cep}/json/

Exemplo: https://viacep.com.br/ws/01001000/json/
```

```json
// Resposta de sucesso
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP"
}

// CEP inexistente
{ "erro": true }
```

## A implementação

```jsx
import { useState, useEffect } from "react";

function BuscaCep() {
  const [cep, setCep] = useState("");
  const [cepBusca, setCepBusca] = useState(""); // dispara o fetch
  const [endereco, setEndereco] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    if (!cepBusca) return; // nada pra buscar

    async function buscar() {
      setCarregando(true);
      setErro(null);

      try {
        const res = await fetch(
          `https://viacep.com.br/ws/${cepBusca}/json/`
        );

        if (!res.ok) throw new Error(`Erro ${res.status}`);

        const dados = await res.json();

        if (dados.erro) {
          throw new Error("CEP não encontrado");
        }

        setEndereco(dados);
      } catch (e) {
        setErro(e.message);
        setEndereco(null);
      } finally {
        setCarregando(false);
      }
    }

    buscar();
  }, [cepBusca]); // roda quando o usuário confirma a busca

  function handleSubmit(e) {
    e.preventDefault();
    const limpo = cep.replace(/\D/g, ""); // remove não-dígitos

    if (limpo.length !== 8) {
      setErro("CEP deve ter 8 dígitos");
      return;
    }

    setErro(null);
    setCepBusca(limpo); // ← dispara o useEffect
  }

  return (
    <div>
      <h1>Busca de CEP</h1>

      <form onSubmit={handleSubmit}>
        <input
          value={cep}
          onChange={e => setCep(e.target.value)}
          placeholder="Digite o CEP (ex: 01001000)"
          maxLength={9}
        />
        <button type="submit" disabled={carregando}>
          {carregando ? "Buscando..." : "Buscar"}
        </button>
      </form>

      {erro && <p className="erro">{erro}</p>}

      {endereco && !carregando && (
        <div className="endereco">
          <h2>Endereço encontrado</h2>
          <p><strong>CEP:</strong> {endereco.cep}</p>
          <p><strong>Logradouro:</strong> {endereco.logradouro}</p>
          <p><strong>Bairro:</strong> {endereco.bairro}</p>
          <p><strong>Cidade:</strong> {endereco.localidade} — {endereco.uf}</p>
        </div>
      )}
    </div>
  );
}
```

## O padrão — input separado da busca

```jsx
const [cep, setCep] = useState("");        // o que o usuário digita
const [cepBusca, setCepBusca] = useState(""); // o que dispara o fetch
```

Separar evita fazer requisição **a cada letra digitada**. O fetch só dispara no submit.

Alternativa: debounce (busca automática ao parar de digitar):

```jsx
useEffect(() => {
  const limpo = cep.replace(/\D/g, "");
  if (limpo.length !== 8) return;

  const timer = setTimeout(() => {
    setCepBusca(limpo);
  }, 500);

  return () => clearTimeout(timer);
}, [cep]);
```

## O caso `erro: true` do ViaCEP

Diferente de um 404 HTTP, o ViaCEP retorna **200 com `{erro: true}`** para CEP inexistente. Por isso:

```jsx
const dados = await res.json();
if (dados.erro) throw new Error("CEP não encontrado");
```

## Formatação do CEP — máscara simples

```jsx
function formatarCep(valor) {
  return valor
    .replace(/\D/g, "")
    .replace(/(\d{5})(\d{3})/, "$1-$2")
    .slice(0, 9);
}

<input
  value={cep}
  onChange={e => setCep(formatarCep(e.target.value))}
  placeholder="00000-000"
/>
```

## Desafios extras

### Desafio A — histórico de buscas

```jsx
const [historico, setHistorico] = useState(() =>
  JSON.parse(localStorage.getItem("historico") || "[]")
);

// ao achar endereço, adiciona ao histórico
useEffect(() => {
  if (endereco) {
    setHistorico(h => [
      endereco.cep,
      ...h.filter(c => c !== endereco.cep)
    ].slice(0, 5));
  }
}, [endereco]);
```

### Desafio B — estado vazio

```jsx
{!endereco && !carregando && !erro && (
  <p>Digite um CEP para buscar o endereço.</p>
)}
```

### Desafio C — múltiplos CEPs

```jsx
// Buscar uma lista de CEPs em paralelo
const resultados = await Promise.all(
  ceps.map(c => fetch(`https://viacep.com.br/ws/${c}/json/`).then(r => r.json()))
);
```

## Critérios de verificação

- `useEffect` dependendo de `cepBusca` — não de cada tecla
- Validação de 8 dígitos antes de buscar
- `dados.erro` tratado como CEP inexistente
- Loading desabilita o botão
- Erro limpa o endereço anterior (`setEndereco(null)`)
- Máscara de formatação se implementada

## Erros comuns

| Erro | Correção |
| --- | --- |
| Fetch dependendo de `cep` (cada tecla) | Use `cepBusca` separado ou debounce |
| `erro: true` ignorado | Cheque `dados.erro` — ViaCEP retorna 200 com erro |
| `cep` com formatação enviado | `replace(/\D/g, "")` antes da URL |
| Estado velho ao clicar de novo | `setErro(null)` + `setCarregando(true)` no início do efeito |
