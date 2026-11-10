# FE04-31 — Estado: Entendendo o useState

## A anatomia

```jsx
const [valor, setValor] = useState(valorInicial);
```

`useState` retorna um array com duas posições, desestruturadas:

- **`valor`** — o estado atual
- **`setValor`** — a função que atualiza o estado e dispara re-render

```jsx
const [nome, setNome] = useState("Ana");
const [idade, setIdade] = useState(28);
const [ativo, setAtivo] = useState(false);
const [lista, setLista] = useState([]);
```

## Tipos de estado

### Primitivos

```jsx
const [texto, setTexto] = useState("");
const [numero, setNumero] = useState(0);
const [ligado, setLigado] = useState(false);
```

### Arrays

```jsx
const [itens, setItens] = useState([]);

// Adicionar — imutável!
setItens([...itens, novoItem]);

// Remover
setItens(itens.filter(i => i.id !== id));

// Atualizar um item
setItens(itens.map(i => i.id === id ? { ...i, feito: true } : i));
```

### Objetos

```jsx
const [usuario, setUsuario] = useState({ nome: "", email: "" });

// Atualizar uma propriedade — espalha o resto
setUsuario({ ...usuario, nome: "Ana" });
```

## As duas formas de atualizar

### Valor direto — quando não depende do anterior

```jsx
setNome("Beto");
setAtivo(true);
setLista(novaLista);
```

### Função — quando o novo depende do anterior

```jsx
// ❌ Pode usar valor "velho" em atualizações rápidas
setContador(contador + 1);

// ✅ Forma funcional — sempre o valor mais recente
setContador(prev => prev + 1);
setItens(prev => [...prev, novo]);
```

A forma funcional é a correta quando o update depende do estado atual — especialmente em handlers rápidos, timeouts e eventos consecutivos.

## Estado inicial computado (lazy init)

Se o valor inicial precisa de cálculo, passe uma função — executa só na primeira render:

```jsx
// ❌ Recalcula a cada render
const [dados, setDados] = useState(calcularDados());

// ✅ Calcula só uma vez
const [dados, setDados] = useState(() => calcularDados());

// ✅ Ideal para localStorage
const [tema, setTema] = useState(() =>
  localStorage.getItem("tema") || "claro"
);
```

## O que dispara re-render

Mudança de estado só re-renderiza se a **referência** mudou:

```jsx
// ✅ Nova referência — re-render
setItens([...itens, novo]);
setUsuario({ ...usuario, nome: "X" });

// ❌ Mesma referência — React ignora
itens.push(novo);
setItens(itens); // mesmo array — sem re-render!
```

É por isso que imutabilidade é obrigatória: o React compara referências, não conteúdo.

## Estado assíncrono — a pegadinha do log

```jsx
setContador(contador + 1);
console.log(contador); // ⚠️ ainda mostra o valor ANTIGO
```

`setContador` não atualiza imediatamente — agenda uma re-renderização. O log lê o valor da render atual. Para reagir ao novo valor, use `useEffect` ou a forma funcional.

## Múltiplos estados vs objeto único

```jsx
// ✅ Estados separados — mais legível
const [nome, setNome] = useState("");
const [email, setEmail] = useState("");

// ✅ Ou objeto único quando os dados andam juntos
const [form, setForm] = useState({ nome: "", email: "" });
setForm(prev => ({ ...prev, nome: "Ana" }));
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `itens.push()` + `setItens(itens)` | Imutável: `setItens([...itens, novo])` |
| `setState` esperando atualização imediata | `set` agenda — log lê o antigo |
| `useState(calcular())` custoso | `useState(() => calcular())` — lazy |
| Muitos estados relacionados | Agrupe em objeto ou `useReducer` |
| Estado que é derivação | Calcule no render — não guarde |
