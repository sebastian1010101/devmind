# FE05-22 — Estados Globais: Bibliotecas de Estado Global

## O que é estado global

Dados que **muitos componentes em níveis diferentes** precisam — usuário logado, carrinho, tema, notificações. Context resolve, mas tem limites de performance e escalabilidade.

## Por que Context não basta às vezes

| Limitação do Context | Impacto |
| --- | --- |
| Todo consumidor re-renderiza | `value` muda → todos que `useContext` renderizam |
| Sem seleção fina | Não dá pra consumir só `carrinho.itens` — consome tudo |
| Re-renders em cascata | Provider no topo → árvore inteira pode re-renderizar |
| Difícil de testar fora do React | Context precisa da árvore montada |

## O panorama das bibliotecas

| Biblioteca | Filosofia | Curva | Uso |
| --- | --- | --- | --- |
| **Zustand** | Store simples, hooks | Baixa | Recomendado — leve e direto |
| **Redux** | Fluxo rígido, actions, reducers | Alta | Apps grandes, time grande |
| **Jotai** | Átomos — estado granular | Média | Estado distribuído |
| **Recoil** | Átomos + seletores | Média | Meta — em manutenção |
| **MobX** | Observável, reativo | Média | OOP, classes |
| **Context** | Nativo | Zero | Auth, tema — dados estáveis |

## Zustand — o favorito

```jsx
import { create } from "zustand";

const useStore = create((set) => ({
  contador: 0,
  incrementar: () => set(s => ({ contador: s.contador + 1 }))
}));

// consumo — seleciona só o que usa
const contador = useStore(s => s.contador);
const incrementar = useStore(s => s.incrementar);
```

- Sem Provider
- Sem boilerplate
- Seleção fina — re-render só do que usa

## Redux — o padrão enterprise

```jsx
// Store global + actions + reducers
const store = createStore(reducer);
store.dispatch({ type: "INCREMENTAR" });
```

- Estrutura rígida — previsível
- DevTools poderosos — time travel
- Verboso — muito boilerplate
- Redux Toolkit moderniza bastante

## Quando usar cada um

```text
Estado local (useState):
  formulário, modal aberto, hover — 1 componente

Context:
  tema, auth, idioma — muda raramente, muitos leem

Zustand:
  carrinho, filtros, dados de UI globais — muda com frequência

Redux:
  apps grandes, time grande, necessidade de devtools/auditoria

React Query:
  dados do servidor — cache, sync, não é "estado" real
```

## A regra prática

| Tipo de dado | Solução |
| --- | --- |
| Estado de um componente | `useState` |
| Estado de uma sub-árvore | `useState` no pai + props |
| Tema/auth/idioma | Context |
| Carrinho/filtros/UI global | Zustand |
| Dados de API | React Query |
| Estado crítico auditável | Redux |

## Erros comuns

| Erro | Correção |
| --- | --- |
| Redux para um contador | Zustand ou Context — Redux é pra apps grandes |
| Context para dados que mudam muito | Zustand — seleção fina evita re-renders |
| Estado de servidor em useState | React Query — cache e sync |
| Estado global pra tudo | Local primeiro — global só quando necessário |

## Resumo

- Context resolve compartilhamento; bibliotecas de estado resolvem performance
- Zustand = simplicidade + seleção fina; Redux = estrutura + devtools
- React Query cuida dos dados de servidor — não é estado global
- Comece local → Context se precisar compartilhar → Zustand se precisar de performance
