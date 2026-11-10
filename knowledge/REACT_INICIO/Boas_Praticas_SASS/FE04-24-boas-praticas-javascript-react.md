# FE04-24 — Boas Práticas com JavaScript/React

## Código limpo em componentes

### 1. Componentes pequenos e focados

Cada componente faz uma coisa. Se o arquivo passa de ~150 linhas, provavelmente faz mais de uma:

```jsx
// ❌ Faz tudo — dados, lista, modal, formulário
function Pagina() { /* 300 linhas */ }

// ✅ Orquestra — delega a especialistas
function Pagina() {
  return (
    <>
      <Header />
      <ListaProdutos />
      <ModalCompra />
    </>
  );
}
```

### 2. Nomes que comunicam

```jsx
// ❌
const d = data.filter(x => x.s > 0);
<button onClick={e => handleClick(e)}>ok</button>

// ✅
const produtosDisponiveis = produtos.filter(p => p.estoque > 0);
<button onClick={handleAdicionar}>Adicionar</button>
```

Convenções: `handleX` para handlers, `is/has/can` para booleanos, `onX` para props de evento.

### 3. Extraia lógica do JSX

```jsx
// ❌ Lógica inline — difícil de ler e testar
return (
  <p>{itens.filter(i => i.ativo).length} ativos de {itens.length}</p>
);

// ✅ Expressão nomeada antes do return
const totalAtivos = itens.filter(i => i.ativo).length;
return <p>{totalAtivos} ativos de {itens.length}</p>;
```

### 4. Early returns em vez de aninhamento

```jsx
// ❌ Pirâmide de ifs
function Item({ dado }) {
  if (dado) {
    if (dado.ativo) {
      return <div>{dado.nome}</div>;
    } else {
      return <p>Inativo</p>;
    }
  } else {
    return <p>Sem dados</p>;
  }
}

// ✅ Guard clauses
function Item({ dado }) {
  if (!dado) return <p>Sem dados</p>;
  if (!dado.ativo) return <p>Inativo</p>;
  return <div>{dado.nome}</div>;
}
```

## Estado bem gerenciado

### 5. Estado mínimo — derive o resto

```jsx
// ❌ Estado redundante — dois estados podem dessincronizar
const [itens, setItens] = useState([]);
const [total, setTotal] = useState(0);

// ✅ Derive — total é calculado, não guardado
const [itens, setItens] = useState([]);
const total = itens.reduce((acc, i) => acc + i.preco, 0);
```

### 6. Atualização funcional para estado dependente

```jsx
// ❌ Lê o estado atual — pode estar desatualizado
setContador(contador + 1);

// ✅ Forma funcional — sempre o valor mais recente
setContador(prev => prev + 1);
```

### 7. Imutabilidade sempre

```jsx
// ❌ Muta o array — React não detecta a mudança
itens.push(novo);
setItens(itens);

// ✅ Novo array — referência nova dispara re-render
setItens([...itens, novo]);
setItens(itens.filter(i => i.id !== id));
setItens(itens.map(i => i.id === id ? { ...i, feito: true } : i));
```

## Props e composição

### 8. Desestruture na assinatura

```jsx
// ❌ props.prop repetido
function Card(props) {
  return <h2>{props.titulo}</h2>;
}

// ✅ Contrato visível na assinatura
function Card({ titulo, preco, onComprar }) { }
```

### 9. Defaults na desestruturação

```jsx
function Botao({ texto = "Clique", variante = "primario" }) { }
```

### 10. children para composição

```jsx
// ✅ Moldura flexível
function Card({ children }) {
  return <div className="card">{children}</div>;
}
```

## Organização de código

### 11. Imports ordenados

```jsx
// 1. React e bibliotecas
import { useState } from "react";
import axios from "axios";

// 2. Componentes
import Header from "./components/Header";

// 3. Utilitários e dados
import { formatar } from "./utils";

// 4. Estilos (por último)
import styles from "./App.module.css";
```

### 12. Constantes fora do componente

```jsx
// ✅ Não recria a cada render
const CATEGORIAS = ["eletronicos", "moveis"];
const CONFIG = { limite: 10 };

function Lista() {
  const [itens, setItens] = useState([]);
  // ...
}
```

## Checklist de revisão

- Componente tem um trabalho claro?
- Nomes dizem o que a coisa faz/é?
- Lógica pesada está fora do JSX?
- Estado é o mínimo necessário?
- Atualizações de estado são imutáveis?
- `key` estável (não índice) nas listas?
- Sem `console.log` esquecido?
