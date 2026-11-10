# FE04-17 — Atividade: Renderizando uma Lista de Frutas

## Objetivo

Praticar o padrão `array.map()` → componentes, usando `key` corretamente e tratando o caso de lista vazia.

## Versão 1 — Lista simples

```jsx
// src/App.jsx
function App() {
  const frutas = ["Maçã", "Banana", "Uva", "Manga", "Morango"];

  return (
    <ul>
      {frutas.map(fruta => (
        <li key={fruta}>{fruta}</li>
      ))}
    </ul>
  );
}
```

`key={fruta}` funciona porque cada fruta é única — a própria string serve como identidade.

## Versão 2 — Lista de objetos com componente

```jsx
// src/components/Fruta.jsx
function Fruta({ nome, emoji, cor }) {
  return (
    <li className="fruta" style={{ borderLeft: `4px solid ${cor}` }}>
      <span>{emoji}</span>
      <strong>{nome}</strong>
    </li>
  );
}

export default Fruta;
```

```jsx
// src/App.jsx
import Fruta from "./components/Fruta";

function App() {
  const frutas = [
    { id: 1, nome: "Maçã", emoji: "🍎", cor: "#e74c3c" },
    { id: 2, nome: "Banana", emoji: "🍌", cor: "#f1c40f" },
    { id: 3, nome: "Uva", emoji: "🍇", cor: "#8e44ad" },
    { id: 4, nome: "Manga", emoji: "🥭", cor: "#e67e22" },
    { id: 5, nome: "Morango", emoji: "🍓", cor: "#e91e63" }
  ];

  return (
    <ul className="lista-frutas">
      {frutas.map(f => (
        <Fruta key={f.id} nome={f.nome} emoji={f.emoji} cor={f.cor} />
      ))}
    </ul>
  );
}
```

## Versão 3 — Com estado vazio

```jsx
function ListaFrutas({ frutas }) {
  if (frutas.length === 0) {
    return <p>Nenhuma fruta cadastrada.</p>;
  }

  return (
    <ul>
      {frutas.map(f => (
        <Fruta key={f.id} {...f} />
      ))}
    </ul>
  );
}
```

## Desafios extras

### Desafio A — contador de itens

```jsx
<p>{frutas.length} frutas cadastradas</p>
```

### Desafio B — filtrar antes de mapear

```jsx
const frutasVermelhas = frutas.filter(f => f.cor.includes("e"));

{frutasVermelhas.map(f => <Fruta key={f.id} {...f} />)}
```

### Desafio C — ordenar alfabeticamente

```jsx
{[...frutas]
  .sort((a, b) => a.nome.localeCompare(b.nome))
  .map(f => <Fruta key={f.id} {...f} />)}
```

⚠️ O `[...frutas]` copia o array antes de `sort` — `sort` muta o original.

## CSS

```css
.lista-frutas {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 0.5rem;
}

.fruta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}
```

## Critérios de verificação

- `.map()` retornando elemento/componente por item
- `key` com valor estável (`id` ou valor único — não índice em lista dinâmica)
- Componente separado para o item (`Fruta`)
- Tratamento de lista vazia
- `[...arr]` antes de `sort` para não mutar o array original

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `key={index}` em lista que muda | Estado quebrado ao reordenar/remover |
| `sort()` direto no array de estado | Muta o array — use `[...arr].sort()` |
| Sem tratamento de vazio | Lista renderiza nada silenciosamente |
| `map` sem `return` implícito | `{itens.map(i => { <li> })` retorna `undefined` |
