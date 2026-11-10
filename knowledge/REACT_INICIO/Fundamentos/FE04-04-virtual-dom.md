# FE04-04 — Virtual DOM

## O que é

O **Virtual DOM** é uma representação em memória da interface — uma árvore de objetos JavaScript leves que espelha a estrutura do DOM real. É o mecanismo que faz o React ser rápido o suficiente para redes sociais e dashboards complexos.

## O problema: manipular o DOM real é caro

Operações no DOM real são lentas porque cada mudança pode disparar reflow e repaint — o navegador recalcula geometria e repixels da tela:

```javascript
// Cada uma dessas linhas pode custar um frame inteiro
elemento.style.width = "300px";   // reflow
elemento.appendChild(novoItem);   // reflow + repaint
elemento.innerText = "novo";      // reflow
```

Num app com centenas de elementos atualizando simultaneamente, o custo acumula — a interface trava.

## A solução: Virtual DOM como camada intermediária

O React mantém uma cópia leve da UI em JavaScript puro. Quando o estado muda:

```text
1. Estado muda
      ↓
2. React gera um NOVO Virtual DOM (objetos JS — barato)
      ↓
3. Compara o novo com o anterior (processo chamado "diffing")
      ↓
4. Calcula o MÍNIMO de mudanças necessárias
      ↓
5. Aplica só essas mudanças no DOM real (em batch)
```

## Visualizando o diffing

```jsx
// Estado inicial
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>

// Depois de adicionar um item — o React compara as árvores:
// antes: 3 <li> | depois: 4 <li>
// mudança mínima: appendChild de um <li> — não recria a lista!
```

O DOM real recebe apenas `appendChild(<li>Item 4</li>)` — os outros três elementos nem são tocados.

## Por que é rápido

| Operação | Custo |
| --- | --- |
| Criar objetos JS | Nanossegundos |
| Comparar objetos JS | Muito rápido |
| Manipular DOM real | Milissegundos — caro |
| Uma operação DOM em batch | Aceitável |

O Virtual DOM troca "muitas operações DOM caras" por "muitas operações JS baratas + poucas operações DOM em lote".

## Reconciliação — o algoritmo

O React usa heurísticas para fazer o diffing em tempo quase-linear (O(n)):

### 1. Tipos diferentes → recriação total

```jsx
// Se um <div> vira <section>, o React não tenta converter —
// destrói o antigo e monta o novo do zero
{condicao ? <div>...</div> : <section>...</section>}
```

### 2. Mesmo tipo → atualização parcial

```jsx
// <button> continua <button> — React só atualiza o que mudou
<button className="ativo">    // só a classe muda
```

### 3. Listas → o papel da `key`

```jsx
// Sem key — React pode reutilizar o elemento errado
{tarefas.map(t => <li>{t.texto}</li>)}

// Com key — React sabe exatamente qual item é qual
{tarefas.map(t => <li key={t.id}>{t.texto}</li>)}
```

A `key` é o identificador estável que permite ao React rastrear elementos entre renders — inserir no meio de uma lista com `key` é eficiente; sem `key`, o React pode re-renderizar tudo ou reutilizar estado errado.

## O que NÃO é verdade sobre Virtual DOM

- ❌ "O Virtual DOM é sempre mais rápido" — para mudanças simples, JS puro pode ser mais rápido; o ganho está em **atualizações complexas em batch**
- ❌ "É uma cópia do DOM" — é uma árvore de objetos JS que *descreve* o DOM, não uma cópia literal
- ❌ "Só o React usa" — Vue, Preact, Inferno e outros usam variações do conceito

## Re-renderização vs reconciliação

Quando um componente re-renderiza:

```jsx
function Lista({ itens }) {
  return (
    <ul>
      {itens.map(i => <li key={i.id}>{i.nome}</li>)}
    </ul>
  );
}
```

```text
setState → componente re-renderiza (gera novo VDOM)
         → diffing (quais nós mudaram?)
         → commit (aplica mudanças no DOM real)
```

A re-renderização do componente **não** é o mesmo que atualizar o DOM real — o Virtual DOM é a camada que garante que só o necessário toque o DOM.

## Batch updates

O React agrupa múltiplas mudanças de estado numa única renderização:

```jsx
function handleClick() {
  setNome("Ana");      // não renderiza ainda
  setIdade(28);        // não renderiza ainda
  setCidade("SP");     // não renderiza ainda
  // React faz UM re-render com os três estados aplicados
}
```

Em versões anteriores (React 17-), isso só funcionava dentro de event handlers. Desde React 18, **todos** os updates são batchados automaticamente — timeouts, promises, eventos nativos.

## Fiber — a arquitetura interna

Desde o React 16, o Virtual DOM usa a arquitetura **Fiber** — uma reescrita que permite:

- **Pausar e retomar** renderizações (prioridade a interações do usuário)
- **Concurrent rendering** — preparar a próxima tela sem bloquear a atual
- **Suspense** — esperar dados antes de renderizar

É por isso que o React consegue renderizar apps enormes sem travar a thread principal.

## Resumo

- Virtual DOM = representação JS leve da UI real
- Diffing compara árvores e calcula mudanças mínimas
- `key` nas listas permite rastreamento eficiente
- Batch updates agrupam mudanças de estado
- O ganho é em **atualizações complexas** — não é magia em casos triviais
- Fiber permite renderização concorrente e pausável
