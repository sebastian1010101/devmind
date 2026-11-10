# FE04-16 — Renderizando Componentes via Lista de Dados

## O padrão fundamental

Quase toda interface real renderiza uma **lista de dados** — produtos, usuários, posts, mensagens. O padrão React: array de dados + `.map()` → lista de elementos.

```jsx
const frutas = ["maçã", "banana", "uva"];

function ListaFrutas() {
  return (
    <ul>
      {frutas.map(fruta => (
        <li key={fruta}>{fruta}</li>
      ))}
    </ul>
  );
}
```

## Por que `.map()` e não `for`

Dentro do JSX só cabem **expressões** — e `.map()` é uma expressão que retorna um array de elementos:

```jsx
// ❌ for não é expressão — não cabe em JSX
<ul>
  {for (const f of frutas) { <li>{f}</li> }}
</ul>

// ✅ map retorna array de elementos — JSX aceita
<ul>
  {frutas.map(f => <li key={f}>{f}</li>)}
</ul>
```

## A prop `key` — identidade dos itens

O React usa `key` para rastrear qual elemento corresponde a qual dado entre re-renderizações:

```jsx
{usuarios.map(u => <li key={u.id}>{u.nome}</li>)}
```

### Regras da key

- **Única entre irmãos** — não precisa ser globalmente única
- **Estável** — o mesmo item deve ter a mesma key sempre
- **Não é passada como prop** — `props.key` não existe dentro do componente

### ⚠️ O problema do índice como key

```jsx
// ⚠️ Funciona para listas estáticas, mas quebra com reordenação
{itens.map((item, i) => <li key={i}>{item}</li>)}
```

Usar o índice é aceitável só quando a lista **nunca muda de ordem nem de tamanho**. Se itens são adicionados, removidos ou reordenados, o índice faz o React reutilizar o estado errado — inputs que mantêm valor do item anterior, animações no item errado.

```jsx
// ✅ ID estável do dado
{usuarios.map(u => <li key={u.id}>{u.nome}</li>)}

// ✅ Sem ID? Gere um na criação do dado
{itens.map(i => <li key={i.id ?? crypto.randomUUID()}>{i.nome}</li>)}
```

## Renderizando componentes de lista

O padrão real: `.map()` gera **componentes**, não apenas tags:

```jsx
const produtos = [
  { id: 1, nome: "Teclado", preco: 150 },
  { id: 2, nome: "Mouse", preco: 80 }
];

function ListaProdutos() {
  return (
    <div className="grade">
      {produtos.map(p => (
        <CardProduto
          key={p.id}
          nome={p.nome}
          preco={p.preco}
        />
      ))}
    </div>
  );
}
```

### Com spread das props

```jsx
{produtos.map(p => <CardProduto key={p.id} {...p} />)}
```

O `{...p}` espalha `nome`, `preco` e `id` como props — conciso, mas implícito. Prefira props explícitas quando o componente não usa todas.

## Lista vazia — o estado que esquecem

```jsx
function Lista({ itens }) {
  return (
    <ul>
      {itens.length === 0
        ? <li>Nenhum item</li>                     // ✅ trata o vazio
        : itens.map(i => <li key={i.id}>{i.nome}</li>)}
    </ul>
  );
}
```

## Composição: pai passa dados, filho renderiza

```jsx
// Dados vivem no pai
function App() {
  const [tarefas] = useState([
    { id: 1, texto: "Estudar React", feita: false },
    { id: 2, texto: "Fazer exercício", feita: true }
  ]);

  return <ListaTarefas tarefas={tarefas} />;
}

// Filho só renderiza o que recebe
function ListaTarefas({ tarefas }) {
  return (
    <ul>
      {tarefas.map(t => (
        <ItemTarefa key={t.id} texto={t.texto} feita={t.feita} />
      ))}
    </ul>
  );
}
```

## Resumo

- `.map()` dentro de `{}` — a expressão que gera listas
- `key` estável e única — prefira `id` do dado, evite índice em listas dinâmicas
- Liste componentes, não só tags — `<CardProduto key={id} {...item} />`
- Sempre trate o caso de lista vazia
