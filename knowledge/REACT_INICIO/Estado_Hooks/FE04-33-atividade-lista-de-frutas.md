# FE04-33 — Atividade: Criando uma Lista de Frutas

## Objetivo

Construir uma lista de frutas interativa com `useState` — adicionando e removendo itens dinamicamente.

## Versão 1 — Lista com estado

```jsx
import { useState } from "react";

function App() {
  const [frutas, setFrutas] = useState([
    { id: 1, nome: "Maçã" },
    { id: 2, nome: "Banana" },
    { id: 3, nome: "Uva" }
  ]);

  return (
    <ul>
      {frutas.map(f => (
        <li key={f.id}>{f.nome}</li>
      ))}
    </ul>
  );
}
```

## Versão 2 — Adicionando itens

```jsx
function App() {
  const [frutas, setFrutas] = useState([]);
  const [input, setInput] = useState("");

  function adicionar() {
    const nome = input.trim();
    if (!nome) return;

    const nova = {
      id: Date.now(), // ID único simples
      nome
    };

    setFrutas(prev => [...prev, nova]); // imutável!
    setInput(""); // limpa o campo
  }

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && adicionar()}
        placeholder="Nome da fruta"
      />
      <button onClick={adicionar}>Adicionar</button>

      <ul>
        {frutas.map(f => (
          <li key={f.id}>{f.nome}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Versão 3 — Removendo itens

```jsx
function remover(id) {
  setFrutas(prev => prev.filter(f => f.id !== id));
}

// No JSX:
{frutas.map(f => (
  <li key={f.id}>
    {f.nome}
    <button onClick={() => remover(f.id)}>✕</button>
  </li>
))}
```

## Versão completa — lista interativa

```jsx
import { useState } from "react";

function App() {
  const [frutas, setFrutas] = useState([]);
  const [input, setInput] = useState("");

  function adicionar() {
    const nome = input.trim();
    if (!nome) return;
    setFrutas(prev => [...prev, { id: Date.now(), nome }]);
    setInput("");
  }

  function remover(id) {
    setFrutas(prev => prev.filter(f => f.id !== id));
  }

  return (
    <div>
      <h1>Lista de Frutas ({frutas.length})</h1>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === "Enter" && adicionar()}
        placeholder="Digite uma fruta"
      />
      <button onClick={adicionar}>+</button>

      {frutas.length === 0 ? (
        <p>Nenhuma fruta ainda. Adicione uma!</p>
      ) : (
        <ul>
          {frutas.map(f => (
            <li key={f.id}>
              {f.nome}
              <button onClick={() => remover(f.id)}>✕</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Desafios extras

### Desafio A — impedir duplicatas

```jsx
function adicionar() {
  const nome = input.trim();
  if (!nome) return;
  if (frutas.some(f => f.nome.toLowerCase() === nome.toLowerCase())) {
    alert("Fruta já está na lista!");
    return;
  }
  setFrutas(prev => [...prev, { id: Date.now(), nome }]);
  setInput("");
}
```

### Desafio B — marcar como favorita

```jsx
function alternarFav(id) {
  setFrutas(prev =>
    prev.map(f => f.id === id ? { ...f, favorita: !f.favorita } : f)
  );
}

// No JSX:
<li className={f.favorita ? "favorita" : ""}>
  {f.nome}
  <button onClick={() => alternarFav(f.id)}>⭐</button>
</li>
```

### Desafio C — limpar toda a lista

```jsx
<button onClick={() => setFrutas([])}>Limpar tudo</button>
```

## Critérios de verificação

- `useState` para a lista e para o input
- Atualizações imutáveis: `[...prev, novo]`, `prev.filter()`, `prev.map()`
- `key={f.id}` estável — `Date.now()` como ID simples
- Input controlado: `value={input}` + `onChange`
- Lista vazia tratada
- Sem mutação direta do array de estado

## Erros comuns

| Erro | Correção |
| --- | --- |
| `frutas.push(nova)` | `[...frutas, nova]` — nunca mute o estado |
| `key={index}` | Remoções quebram com índice — use `id` estável |
| Input não limpa após adicionar | `setInput("")` após `setFrutas` |
| `setFrutas(frutas.filter())` | Use forma funcional `prev => prev.filter()` |
