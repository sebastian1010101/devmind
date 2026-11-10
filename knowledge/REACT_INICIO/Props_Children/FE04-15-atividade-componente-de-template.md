# FE04-15 — Atividade: Criando um Componente de Template

## Objetivo

Criar componentes "moldura" que recebem conteúdo via `children` — praticando composição, o padrão mais importante do React.

## Componente 1 — PageTemplate (layout base)

```jsx
// src/components/PageTemplate.jsx
function PageTemplate({ titulo, children }) {
  return (
    <div className="page">
      <header className="page__header">
        <h1>{titulo}</h1>
      </header>

      <main className="page__main">
        {children}
      </main>

      <footer className="page__footer">
        <p>© 2024 — Meu App</p>
      </footer>
    </div>
  );
}

export default PageTemplate;
```

## Componente 2 — Section (agrupador semântico)

```jsx
// src/components/Section.jsx
function Section({ titulo, children }) {
  return (
    <section className="section">
      <h2>{titulo}</h2>
      <div className="section__content">
        {children}
      </div>
    </section>
  );
}

export default Section;
```

## Componente 3 — Card (moldura de conteúdo)

```jsx
// src/components/Card.jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

export default Card;
```

## Uso — compondo as molduras

```jsx
// src/App.jsx
import PageTemplate from "./components/PageTemplate";
import Section from "./components/Section";
import Card from "./components/Card";

function App() {
  return (
    <PageTemplate titulo="Dashboard">
      <Section titulo="Produtos">
        <Card>
          <h3>Produto A</h3>
          <p>Descrição do produto</p>
          <button>Comprar</button>
        </Card>
        <Card>
          <h3>Produto B</h3>
          <p>Outro produto</p>
          <button>Comprar</button>
        </Card>
      </Section>

      <Section titulo="Notícias">
        <Card>
          <h3>Novidades do React</h3>
          <p>Nova versão lançada</p>
        </Card>
      </Section>
    </PageTemplate>
  );
}
```

Cada nível de moldura contribui seu estilo/estrutura — e o conteúdo interno é livre.

## Desafios extras

### Desafio A — Card com slots

Adicione áreas nomeadas além do `children`:

```jsx
function Card({ icone, children, acao }) {
  return (
    <div className="card">
      <div className="card__icone">{icone}</div>
      <div className="card__corpo">{children}</div>
      <div className="card__acao">{acao}</div>
    </div>
  );
}

<Card
  icone={<span>🛒</span>}
  acao={<button>Comprar</button>}
>
  <h3>Produto</h3>
</Card>
```

### Desafio B — Alerta temático

Template com prop de variante:

```jsx
function Alerta({ tipo = "info", children }) {
  const classes = `alerta alerta--${tipo}`; // info, sucesso, erro
  return <div className={classes}>{children}</div>;
}

<Alerta tipo="sucesso">Salvo com sucesso!</Alerta>
<Alerta tipo="erro">Falha ao processar.</Alerta>
```

### Desafio C — Lista com render prop

Children como função para customizar cada item:

```jsx
function Lista({ itens, children }) {
  return (
    <ul>
      {itens.map((item, i) => (
        <li key={i}>{children(item)}</li>
      ))}
    </ul>
  );
}

const produtos = [{ nome: "A" }, { nome: "B" }];

<Lista itens={produtos}>
  {(item) => <strong>{item.nome}</strong>}
</Lista>
```

## CSS básico das molduras

```css
.page { min-height: 100vh; display: flex; flex-direction: column; }
.page__main { flex: 1; padding: 2rem; }
.page__header { background: #1a1a2e; color: white; padding: 1rem 2rem; }
.page__footer { background: #eee; padding: 1rem 2rem; text-align: center; }

.section { margin-bottom: 2rem; }
.section__content { display: grid; gap: 1rem; }

.card { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; }
```

## Critérios de verificação

- `children` recebe e renderiza o conteúdo entre as tags
- A moldura (estrutura + estilo) é fixa; o conteúdo é livre
- Composição: `PageTemplate` → `Section` → `Card` → conteúdo arbitrário
- Slots nomeados (`icone`, `acao`) quando a moldura tem áreas distintas
- Nenhum `div` extra desnecessário — `children` elimina wrappers

## Erros comuns

| Erro | Correção |
| --- | --- |
| `<Card />` self-closing quando tem conteúdo | Use `<Card>...</Card>` para children |
| Prop com nome diferente (`content`) | O nome mágico é `children` — React captura automaticamente |
| `children` não renderizado | `{children}` precisa aparecer no JSX — senão some |
| Moldura decidindo o conteúdo | `children` é a liberdade — a moldura só estrutura |
