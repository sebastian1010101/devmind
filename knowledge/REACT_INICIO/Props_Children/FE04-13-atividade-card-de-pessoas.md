# FE04-13 — Atividade: Card de Pessoas

## Objetivo

Criar um componente `CardPessoa` reutilizável que recebe dados via props e renderiza um cartão de perfil — praticando a passagem de diferentes tipos de props.

## O componente

```jsx
// src/components/CardPessoa.jsx
function CardPessoa({ nome, profissao, cidade, foto, online }) {
  return (
    <article className="card-pessoa">
      <img src={foto} alt={nome} className="card-pessoa__foto" />

      <div className="card-pessoa__info">
        <h2>{nome}</h2>
        <p className="card-pessoa__profissao">{profissao}</p>
        <p className="card-pessoa__cidade">{cidade}</p>

        <span className={online ? "status online" : "status offline"}>
          {online ? "Online" : "Offline"}
        </span>
      </div>
    </article>
  );
}

export default CardPessoa;
```

## O uso no App

```jsx
// src/App.jsx
import CardPessoa from "./components/CardPessoa";

function App() {
  return (
    <main>
      <h1>Equipe</h1>

      <CardPessoa
        nome="Ana Silva"
        profissao="Front-End Developer"
        cidade="Curitiba"
        foto="https://i.pravatar.cc/150?img=1"
        online={true}
      />

      <CardPessoa
        nome="Beto Souza"
        profissao="Back-End Developer"
        cidade="São Paulo"
        foto="https://i.pravatar.cc/150?img=2"
        online={false}
      />

      <CardPessoa
        nome="Carla Mendes"
        profissao="UX Designer"
        cidade="Rio de Janeiro"
        foto="https://i.pravatar.cc/150?img=3"
        online={true}
      />
    </main>
  );
}

export default App;
```

## CSS básico

```css
/* src/App.css */
.card-pessoa {
  display: flex;
  gap: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  max-width: 320px;
}

.card-pessoa__foto {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.status {
  font-size: 0.85rem;
  font-weight: 600;
}

.status.online { color: #22c55e; }
.status.offline { color: #9ca3af; }
```

## Desafios extras

### Desafio A — props com valores padrão

Torne `cidade` e `online` opcionais:

```jsx
function CardPessoa({ nome, profissao, cidade = "Não informada", foto, online = false }) {
  // ...
}
```

### Desafio B — lista a partir de dados

Extraia as pessoas para um array e renderize com `.map()`:

```jsx
function App() {
  const pessoas = [
    { id: 1, nome: "Ana", profissao: "Dev", cidade: "Curitiba", foto: "...", online: true },
    { id: 2, nome: "Beto", profissao: "Dev", cidade: "SP", foto: "...", online: false }
  ];

  return (
    <main>
      {pessoas.map(p => (
        <CardPessoa
          key={p.id}
          nome={p.nome}
          profissao={p.profissao}
          cidade={p.cidade}
          foto={p.foto}
          online={p.online}
        />
      ))}
    </main>
  );
}
```

### Desafio C — prop de função

Adicione um botão "Ver perfil" que chama uma função recebida por prop:

```jsx
// CardPessoa.jsx
function CardPessoa({ nome, profissao, onVerPerfil }) {
  return (
    <article>
      <h2>{nome}</h2>
      <p>{profissao}</p>
      <button onClick={() => onVerPerfil(nome)}>Ver perfil</button>
    </article>
  );
}

// App.jsx
function verPerfil(nome) {
  alert(`Perfil de ${nome}`);
}

<CardPessoa nome="Ana" profissao="Dev" onVerPerfil={verPerfil} />
```

## Critérios de verificação

- Props desestruturadas na assinatura da função
- Tipos corretos: `string` sem `{}`, `boolean`/`number` com `{}`
- Valores padrão via `=` na desestruturação
- `key` no `.map()` quando renderizando lista
- Componente não modifica as props recebidas

## Erros comuns

| Erro | Correção |
| --- | --- |
| `online="true"` | Passa string — use `online={true}` |
| `{nome}` dentro de texto sem JSX | Fora de `{}` é texto literal |
| Esquecer `export default` | Import falha — confira o fim do arquivo |
| `props.nome` sem `props` declarado | Desestruture na assinatura ou use `props` |
