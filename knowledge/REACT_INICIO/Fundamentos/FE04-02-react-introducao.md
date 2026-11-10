# FE04-02 — React: Introdução

## O que é React

React é uma **biblioteca JavaScript** para construir interfaces de usuário — criada pelo Facebook (Meta) em 2013 e hoje a ferramenta dominante do front-end moderno. A definição precisa: React é uma biblioteca *declarativa, baseada em componentes e orientada a estado*.

## O problema que o React resolve

### O jeito antigo: DOM imperativo

Antes do React, atualizar a interface significava manipular o DOM manualmente:

```javascript
// ❌ Imperativo — cada mudança é um comando manual
const lista = document.querySelector("#lista");
const item = document.createElement("li");
item.innerText = novaTarefa;
lista.appendChild(item);
```

Funciona para poucos elementos. Mas imagine uma rede social: cada like, comentário, mensagem e notificação exige manipulação manual, sincronização de estado com a UI e gerenciamento de efeitos colaterais. O resultado: código frágil, bugs de sincronização e interfaces que "esquecem" de atualizar.

### O jeito React: declarativo

Com React, você descreve **como a interface deve parecer** para cada estado — e o React cuida de atualizar o DOM:

```jsx
// ✅ Declarativo — descreve o resultado, não os passos
function ListaTarefas({ tarefas }) {
  return (
    <ul>
      {tarefas.map(t => <li key={t.id}>{t.texto}</li>)}
    </ul>
  );
}
```

O componente diz: *"dado este array de tarefas, a UI é esta lista"*. Quando `tarefas` muda, o React recalcula e atualiza só o necessário.

## Os três pilares

### 1. Componentes

A interface é quebrada em **blocos reutilizáveis** — cada componente é uma função que retorna JSX:

```jsx
function Botao({ children, onClick }) {
  return <button onClick={onClick}>{children}</button>;
}
```

Componentes se compõem como peças de Lego: `App` contém `Header`, `Header` contém `Nav`, `Nav` contém `NavItem`.

### 2. Estado (State)

Cada componente pode ter dados internos que mudam ao longo do tempo:

```jsx
function Contador() {
  const [contagem, setContagem] = useState(0);
  return <button onClick={() => setContagem(contagem + 1)}>{contagem}</button>;
}
```

Quando o estado muda, o React **re-renderiza** o componente automaticamente.

### 3. Virtual DOM

O React mantém uma representação leve da UI em memória (o Virtual DOM). Quando o estado muda, ele compara a nova versão com a anterior (**diffing**) e aplica **só as mudanças** no DOM real — minimizando operações custosas.

```text
Estado mudou → Novo Virtual DOM → Diff com o anterior → DOM real atualizado
```

## React vs alternativas

| Aspecto | React | Vue | Angular | Vanilla JS |
| --- | --- | --- | --- | --- |
| Tipo | Biblioteca | Framework | Framework | — |
| Curva de aprendizado | Média | Baixa | Alta | — |
| Ecossistema | Enorme | Grande | Integrado | Nenhum |
| Uso no mercado | Dominante | Crescente | Corporativo | Legado |
| Flexibilidade | Máxima | Alta | Opinativa | Total |

## O ecossistema React

React sozinho é a biblioteca — o ecossistema ao redor é o que faz aplicações completas:

```text
React (núcleo)
├── Vite / Next.js      → ferramenta de build e framework
├── React Router        → navegação entre páginas
├── Styled Components   → CSS-in-JS
├── Redux / Zustand     → gerenciamento de estado global
├── React Query         → cache de dados de API
└── Tailwind / CSS Modules → estilização
```

## Por que aprender React

- **Mercado** — a vaga média de front-end pede React
- **Componentes** — o modelo mental que rege todo o front-end moderno
- **Ecossistema** — bibliotecas para quase tudo
- **React Native** — o mesmo modelo gera apps mobile
- **Declarativo** — menos bugs de sincronização UI-estado

## O que vem a seguir

Os próximos tópicos cobrem a fundação:

- **Vite** — como criar e rodar um projeto React
- **JSX** — a sintaxe que mistura HTML e JavaScript
- **Componentes** — os blocos de construção
- **Props** — como componentes recebem dados
- **Estado** — como componentes lembram e reagem
