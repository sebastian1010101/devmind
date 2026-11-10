# FE04-30 — Estado: Introdução

## O que é estado

**Estado** (state) é a memória de um componente — os dados que mudam ao longo do tempo e que, quando mudam, disparam uma nova renderização da interface.

```text
Estado muda → React re-renderiza → UI atualizada
```

É o que transforma uma página estática em aplicação interativa.

## Estado vs variável comum

O conceito mais importante de todo o React:

```jsx
function Contador() {
  let contagem = 0; // ❌ variável comum — React não "vê"

  function incrementar() {
    contagem += 1;
    console.log(contagem); // o número muda no console...
    // mas a TELA não muda — React não sabe que algo aconteceu
  }

  return <p>{contagem}</p>;
}
```

```jsx
function Contador() {
  const [contagem, setContagem] = useState(0); // ✅ estado — React rastreia

  function incrementar() {
    setContagem(contagem + 1); // dispara re-render → tela atualiza
  }

  return <p>{contagem}</p>;
}
```

| | Variável `let` | Estado `useState` |
| --- | --- | --- |
| Persiste entre renders | Não — reseta a cada render | Sim |
| Mudança atualiza a UI | Não | Sim |
| Onde vive | Na função (volátil) | No React (gerenciado) |

## O que guardar em estado

- Dados que **mudam** ao longo da vida do componente
- Dados que **afetam o que aparece na tela**
- Interações do usuário: inputs, toggles, seleções
- Dados de API: listas carregadas, loading, erros

## O que NÃO guardar em estado

```jsx
// ❌ Dados deriváveis — calcule direto
const [total, setTotal] = useState(0); // total pode derivar de itens

// ✅ Derive no render
const total = itens.reduce((acc, i) => acc + i.preco, 0);

// ❌ Constantes que nunca mudam
const [limite] = useState(10); // nunca muda — não precisa ser estado

// ✅ Constante fora do componente
const LIMITE = 10;
```

Regra: se pode ser **calculado** de outro estado/prop, não é estado — é derivação.

## Onde o estado vive

```jsx
function App() {
  const [tema, setTema] = useState("claro"); // estado no topo

  return (
    <>
      <Header tema={tema} />      {/* desce como prop */}
      <Botao onToggle={setTema} /> {/* função desce como prop */}
    </>
  );
}
```

O estado fica no componente que **precisa** dele — ou no ancestral comum mais próximo de quem precisa (*lifting state up*).

## Estado local vs global

| Escopo | Ferramenta |
| --- | --- |
| Um componente | `useState` |
| Ancestral compartilhado | `useState` + props (lifting) |
| Toda a aplicação | Context API, Zustand, Redux |

## O ciclo completo

```jsx
function Interruptor() {
  const [ligado, setLigado] = useState(false);

  return (
    <div>
      <p>{ligado ? "💡 Ligado" : "⚫ Desligado"}</p>
      <button onClick={() => setLigado(!ligado)}>
        Alternar
      </button>
    </div>
  );
}
```

```text
1. useState(false) → estado inicial: false
2. Renderiza "Desligado"
3. Clique → setLigado(true) → estado muda
4. React re-renderiza → "Ligado"
```

## Resumo

- Estado é a memória reativa do componente
- `useState` devolve `[valor, setValor]`
- Mudar estado = re-render automático
- Variáveis comuns não disparam re-render — é o bug nº 1 de quem começa
- Guarde só o que muda e afeta a UI — o resto é derivado ou constante
