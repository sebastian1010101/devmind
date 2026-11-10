# FE04-40 — Atividade: Condicionando o visual de um componente

## Objetivo

Mudar o **visual** de componentes conforme o estado — classes dinâmicas, estilos condicionais e indicadores visuais.

## Padrão 1 — classe condicional com ternário

```jsx
function Tarefa({ feita }) {
  return (
    <li className={feita ? "tarefa feita" : "tarefa"}>
      <span>{/* texto */}</span>
    </li>
  );
}
```

```css
.tarefa { /* base */ }
.tarefa.feita { opacity: 0.5; text-decoration: line-through; }
```

## Padrão 2 — múltiplas classes condicionais

```jsx
const classes = [
  "btn",
  grande && "btn--grande",
  ativo && "btn--ativo",
  perigo && "btn--perigo"
].filter(Boolean).join(" ");

<button className={classes}>Clique</button>
```

## Padrão 3 — estilo inline dinâmico

```jsx
function BarraProgresso({ valor }) {
  return (
    <div className="barra">
      <div
        className="barra__preenchimento"
        style={{
          width: `${valor}%`,
          background: valor < 30 ? "#e74c3c" : valor < 70 ? "#f39c12" : "#22c55e"
        }}
      />
    </div>
  );
}
```

A cor muda com o valor — vermelho/laranja/verde.

## Padrão 4 — indicador visual de estado

```jsx
function Usuario({ online, ultimoAcesso }) {
  return (
    <div className="usuario">
      <span className={`status ${online ? "status--online" : "status--offline"}`} />
      <span>{online ? "Online" : `Visto ${ultimoAcesso}`}</span>
    </div>
  );
}
```

```css
.status { width: 10px; height: 10px; border-radius: 50%; }
.status--online { background: #22c55e; }
.status--offline { background: #9ca3af; }
```

## O exercício — card de produto completo

```jsx
function CardProduto({ nome, preco, estoque, promocao }) {
  const esgotado = estoque === 0;
  const pouco = estoque > 0 && estoque < 5;

  return (
    <article className={`produto ${esgotado ? "produto--esgotado" : ""}`}>
      {promocao && <span className="tag-promo">Oferta</span>}

      <h3>{nome}</h3>
      <p className="preco">R$ {preco.toFixed(2)}</p>

      <span className={`estoque ${esgotado ? "estoque--zero" : pouco ? "estoque--baixo" : ""}`}>
        {esgotado
          ? "Esgotado"
          : pouco
            ? `Últimas ${estoque} un.`
            : `${estoque} em estoque`}
      </span>

      <button
        disabled={esgotado}
        className={esgotado ? "btn btn--desabilitado" : "btn btn--primario"}
      >
        {esgotado ? "Indisponível" : "Comprar"}
      </button>
    </article>
  );
}
```

## CSS das variantes

```css
.produto--esgotado { opacity: 0.6; }
.tag-promo { background: #e74c3c; color: white; padding: 2px 8px; }
.estoque--zero { color: #e74c3c; }
.estoque--baixo { color: #f39c12; }
.btn--desabilitado { background: #ccc; cursor: not-allowed; }
.btn--primario { background: #3498db; color: white; }
```

## Desafios extras

### Desafio A — tema claro/escuro por estado

```jsx
const [escuro, setEscuro] = useState(false);

<div className={escuro ? "app tema-escuro" : "app tema-claro"}>
```

### Desafio B — notificação com ícone por tipo

```jsx
const icones = { sucesso: "✅", erro: "❌", aviso: "⚠️" };

<div className={`toast toast--${tipo}`}>
  {icones[tipo]} {mensagem}
</div>
```

## Critérios de verificação

- Variantes visuais derivam do estado/props — não de lógica inline no CSS
- `className` dinâmico com ternário ou array `.filter(Boolean).join(" ")`
- Estilo inline para valores computados (`width`, `background` dinâmicos)
- Estado derivado (`esgotado = estoque === 0`) em vez de estado duplicado
- `disabled` e visual consistentes — botão desabilitado tem cara de desabilitado

## Erros comuns

| Erro | Correção |
| --- | --- |
| Estado separado para "esgotado" | Derive de `estoque === 0` — não duplique |
| `className={cond ? "a" : "b"}` sem base | Inclua a classe base: `"btn " + (cond ? "a" : "b")` |
| `style` com string | `style={{ width: "50%" }}` — objeto, não string |
| Estilos inline para classes estáticas | CSS Modules para o fixo, inline para o dinâmico |
