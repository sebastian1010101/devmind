# FE04-61 — Lidando com modais no React

## O modal no React — o desafio

Modais precisam de controle de visibilidade (estado), renderização condicional e geralmente ficam "fora" da árvore visual normal — renderizados por cima de tudo.

## A base — estado + condicional

```jsx
function App() {
  const [aberto, setAberto] = useState(false);

  return (
    <>
      <button onClick={() => setAberto(true)}>Abrir modal</button>

      {aberto && (
        <Modal fechar={() => setAberto(false)}>
          <h2>Conteúdo do modal</h2>
        </Modal>
      )}
    </>
  );
}
```

`{aberto && <Modal />}` — o modal monta/desmonta conforme o estado.

## O componente Modal

```jsx
// components/Modal.jsx
function Modal({ fechar, children }) {
  return (
    <div className="modal-overlay" onClick={fechar}>
      <div
        className="modal-conteudo"
        onClick={e => e.stopPropagation()} // não fecha ao clicar dentro
      >
        <button className="modal-fechar" onClick={fechar}>×</button>
        {children}
      </div>
    </div>
  );
}
```

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-conteudo {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
}
```

## Fechando com ESC

```jsx
function Modal({ fechar, children }) {
  useEffect(() => {
    function aoEsc(e) {
      if (e.key === "Escape") fechar();
    }
    window.addEventListener("keydown", aoEsc);
    return () => window.removeEventListener("keydown", aoEsc);
  }, [fechar]);

  return ( /* ... */ );
}
```

## createPortal — renderizar fora da árvore

O modal renderiza dentro do componente pai, mas visualmente deveria estar acima de tudo. `createPortal` move o DOM do modal para outro lugar:

```jsx
import { createPortal } from "react-dom";

function Modal({ fechar, children }) {
  return createPortal(
    <div className="modal-overlay" onClick={fechar}>
      <div className="modal-conteudo" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body // ← monta direto no body, não dentro do pai
  );
}
```

Vantagens:

- Escapa de `overflow: hidden` ou `z-index` do pai
- Posiciona `fixed` corretamente
- Acessibilidade — fica no fim do body, fora de landmarks

## Travar o scroll do fundo

```jsx
useEffect(() => {
  if (aberto) {
    document.body.style.overflow = "hidden";
  }
  return () => {
    document.body.style.overflow = ""; // restaura ao fechar/desmontar
  };
}, [aberto]);
```

## Modal controlado vs não controlado

```jsx
// Controlado — estado no pai (recomendado para forms)
<Modal aberto={aberto} fechar={...}>
  <input value={nome} onChange={...} />
</Modal>

// Não controlado — estado dentro do modal
<Modal botao="Abrir">
  <input />
</Modal>
// O modal gerencia aberto/fechado internamente
```

## Animação de entrada

```jsx
{aberto && (
  <div className="modal-overlay entrando" onClick={fechar}>
    ...
  </div>
)}
```

```css
.modal-overlay.entrando {
  animation: fadeIn 0.2s ease-out;
}
.modal-conteudo {
  animation: subir 0.3s ease-out;
}
```

## Acessibilidade mínima

```jsx
<div
  className="modal-conteudo"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-titulo"
>
  <h2 id="modal-titulo">Título</h2>
  ...
</div>
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Click dentro fecha o modal | `e.stopPropagation()` no conteúdo |
| Scroll do fundo continua | `body.style.overflow = "hidden"` com cleanup |
| Modal preso em z-index/overflow do pai | `createPortal` para o `document.body` |
| ESC não funciona | `keydown` listener com cleanup |
| Modal some ao navegar | Portal + renderização condicional independente de rota |

## Resumo

- Estado booleano + `{aberto && <Modal>}` controla a visibilidade
- `createPortal` tira o modal da árvore visual do pai
- Overlay com `stopPropagation`, ESC e travamento de scroll são obrigatórios
- `aria-modal` + `role="dialog"` para acessibilidade
