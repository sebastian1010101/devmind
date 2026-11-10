# FE05-28 — Jotai: Entendendo o Básico

## O que é o Jotai

Biblioteca de estado global **atômico** — cada pedaço de estado é um "átomo" independente. O oposto do Redux (um store único): o estado é distribuído em grãos.

```bash
npm install jotai
```

## atom — a unidade de estado

```jsx
import { atom } from "jotai";

// um átomo = um pedaço de estado global
const contadorAtom = atom(0);
const usuarioAtom = atom(null);
const temaAtom = atom("claro");
```

## useAtom — ler e escrever

```jsx
import { useAtom } from "jotai";

function Contador() {
  const [contador, setContador] = useAtom(contadorAtom);
  // mesma API do useState — mas global

  return (
    <button onClick={() => setContador(c => c + 1)}>
      {contador}
    </button>
  );
}
```

Qualquer componente usando `contadorAtom` compartilha o mesmo valor.

## useAtomValue e useSetAtom — separando leitura e escrita

```jsx
import { useAtomValue, useSetAtom } from "jotai";

// só lê — não re-renderiza quando outros campos mudam
const contador = useAtomValue(contadorAtom);

// só escreve — componente não re-renderiza quando o valor muda
const setContador = useSetAtom(contadorAtom);
```

## Átomos derivados — estado computado

```jsx
const itensAtom = atom([]);
const totalAtom = atom((get) =>
  get(itensAtom).reduce((s, i) => s + i.preco, 0)
);

// totalAtom só leitura — calcula sozinho quando itens muda
const total = useAtomValue(totalAtom);
```

## Átomos com escrita — actions

```jsx
const adicionarAtom = atom(
  null,                          // sem leitura
  (get, set, novoItem) => {      // write function
    set(itensAtom, [...get(itensAtom), novoItem]);
  }
);

// no componente — só dispara
const adicionar = useSetAtom(adicionarAtom);
adicionar({ id: 1, nome: "Item" });
```

## Async atoms — fetch nativo

```jsx
const produtosAtom = atom(async () => {
  const res = await fetch("/api/produtos");
  return res.json();
});

// componente — o valor vem resolvido (com Suspense)
function Produtos() {
  const produtos = useAtomValue(produtosAtom); // suspende até resolver
  return <ul>{produtos.map(...)}</ul>;
}
```

## atomWithStorage — persistência nativa

```jsx
import { atomWithStorage } from "jotai/utils";

const temaAtom = atomWithStorage("tema", "claro");
// salva automaticamente no localStorage
```

## Jotai vs Zustand

| Jotai | Zustand |
| --- | --- |
| Átomos distribuídos | Store única |
| Sem Provider (ou com `Provider` opcional) | Sem Provider |
| `useAtom` = `[valor, set]` | `useStore(seletor)` |
| Derivados com `atom((get) => ...)` | `useMemo` ou funções |
| Async atoms nativos | Actions async na store |
| Granular — cada átomo isolado | Centralizado — um objeto |

## Quando usar

| Cenário | Escolha |
| --- | --- |
| Estado granular, muitos pedaços | Jotai — cada átomo isolado |
| Lógica centralizada num lugar | Zustand — store coesa |
| Time acostumado com Redux | Zustand é mais próximo |
| Formulários complexos | Jotai — cada campo um átomo |

## Erros comuns

| Erro | Correção |
| --- | --- |
| `atom` dentro do componente | Cria um novo a cada render — declare fora |
| `useAtom` quando só lê | `useAtomValue` — não se inscreve para escrever |
| Derivado com efeito colateral | `atom((get) => ...)` — read puro |
| Async atom sem Suspense | Envolva com `<Suspense>` |

## Resumo

- `atom(valor)` = pedaço de estado global independente
- `useAtom` = `[valor, set]`; `useAtomValue`/`useSetAtom` separam
- Átomos derivados computam — `atom((get) => ...)`
- `atomWithStorage` persiste no localStorage
- Jotai é granular; Zustand é centralizado
