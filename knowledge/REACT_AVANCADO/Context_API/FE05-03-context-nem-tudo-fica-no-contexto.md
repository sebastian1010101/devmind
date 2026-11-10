# FE05-03 — Context: Nem Tudo Fica no Contexto

## A tentação — contexto como estado global pra tudo

Descoberto o Context, a tentação é jogar tudo lá dentro — carrinho, formulário de contato, input de busca, estado de modal. Isso traz problemas reais.

## Por que não colocar tudo no Context

### 1. Re-renders em massa

```jsx
// ❌ Um contexto gigante — muda carrinho → Header, Footer, tudo re-renderiza
<AppContext.Provider value={{ carrinho, usuario, tema, busca, modal }}>
```

Todo `useContext` re-renderiza quando **qualquer** parte do `value` muda.

### 2. Estado local virou global desnecessariamente

```jsx
// ❌ Estado de input de busca num contexto
// Só o componente de busca usa — mas fica global
```

Estado local é mais leve, mais fácil de rastrear e não re-renderiza componentes distantes.

### 3. Difícil de debugar

```text
"Por que o Header re-renderizou?"
→ Porque o Context mudou
→ Qual parte mudou? 
→ Precisa inspecionar todo o value
```

Contextos grandes viram caixa-preta.

## O que deve ir pro Context

| Sim — Context | Não — estado local |
| --- | --- |
| Tema claro/escuro | Input de busca |
| Usuário autenticado | Valor de um formulário |
| Carrinho de compras | Modal aberto/fechado local |
| Idioma (i18n) | Hover, foco, expansão |
| Configurações globais | Estado de um accordion |

Regra: **muitos componentes em níveis diferentes precisam** → Context. **Um componente ou filhos diretos** → useState.

## Dividir contextos — não juntar

```jsx
// ❌ Um mega-contexto
<AppContext value={{ auth, tema, carrinho, notificacoes }}>

// ✅ Contextos separados por responsabilidade
<AuthProvider>
  <TemaProvider>
    <CarrinhoProvider>
      <App />
    </CarrinhoProvider>
  </TemaProvider>
</AuthProvider>
```

Mudança no carrinho só re-renderiza quem usa `useCarrinho` — Header com `useAuth` fica quieto.

## Otimizando quando o Context é necessário

### Separar estado e dispatch

```jsx
// dois contextos — quem só despacha não re-renderiza
const StateContext = createContext();
const DispatchContext = createContext();

function Provider({ children }) {
  const [state, setState] = useState(...);
  return (
    <StateContext.Provider value={state}>
      <DispatchContext.Provider value={setState}>
        {children}
      </DispatchContext.Provider>
    </StateContext.Provider>
  );
}
```

### useMemo no value

```jsx
const valor = useMemo(() => ({ dados, acao }), [dados, acao]);
```

### Componentes puros abaixo

```jsx
// o consumidor memoizado só re-renderiza se sua parte mudou
const Item = memo(function Item({ item }) {
  return <li>{item.nome}</li>;
});
```

## Alternativas quando Context não basta

| Problema | Solução |
| --- | --- |
| Re-renders demais | Zustand/Jotai — seleção fina de estado |
| Muitos contextos aninhados | Biblioteca de estado global |
| Estado derivado complexo | useReducer ou store externa |
| Dados de servidor | React Query — cache, não estado |

## O anti-padrão do Context gigante

```jsx
// ❌ AppContext com tudo
<AppContext value={{
  usuario, tema, carrinho, busca, filtro,
  modal, loading, erro, pagina, ordenacao
}}>
```

Vira uma dependência global — qualquer mudança impacta tudo.

## Erros comuns

| Erro | Correção |
| --- | --- |
| Estado de formulário no Context | `useState` local |
| Um contexto pra tudo | Divida por domínio (auth, tema, carrinho) |
| Context + useState duplicado | Um dono do estado — Context OU local |
| Re-render de tela inteira | `useMemo` no value + contextos divididos |

## Resumo

- Context não é estado global universal — é para dados realmente compartilhados
- Estado local é mais leve e mais simples de rastrear
- Divida contextos por responsabilidade
- `useMemo` no `value` e contextos separados evitam re-renders em massa
