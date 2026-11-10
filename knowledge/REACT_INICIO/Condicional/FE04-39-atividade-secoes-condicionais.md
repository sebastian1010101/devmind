# FE04-39 — Atividade: Renderizando seções de forma condicional

## Objetivo

Construir uma página que mostra seções diferentes conforme o estado — praticando ternários, `&&` e early returns.

## Cenário — dashboard com estados

```jsx
import { useState } from "react";

function Dashboard() {
  const [logado, setLogado] = useState(false);
  const [carregando, setCarregando] = useState(false);
  const [dados, setDados] = useState(null);
  const [erro, setErro] = useState(null);

  function entrar() {
    setCarregando(true);
    setErro(null);

    // Simula uma chamada de API
    setTimeout(() => {
      setDados({ nome: "Ana", vendas: 42 });
      setLogado(true);
      setCarregando(false);
    }, 1000);
  }

  function sair() {
    setLogado(false);
    setDados(null);
  }
```

## A renderização em camadas

```jsx
  // Early returns — cada estado tem sua tela
  if (carregando) {
    return <p className="loading">Carregando...</p>;
  }

  if (erro) {
    return (
      <div className="erro">
        <p>❌ {erro}</p>
        <button onClick={entrar}>Tentar novamente</button>
      </div>
    );
  }

  if (!logado) {
    return (
      <div className="login">
        <h1>Faça login para continuar</h1>
        <button onClick={entrar}>Entrar</button>
      </div>
    );
  }

  // Estado principal — logado e com dados
  return (
    <div className="dashboard">
      <header>
        <h1>Olá, {dados.nome}!</h1>
        <button onClick={sair}>Sair</button>
      </header>

      <section>
        <h2>Resumo</h2>
        <p>Vendas este mês: {dados.vendas}</p>
      </section>

      {/* Condicional inline — seção extra só para admins */}
      {dados.vendas > 30 && (
        <section className="destaque">
          <h3>🏆 Meta batida!</h3>
        </section>
      )}
    </div>
  );
}
```

## Seções com ternário — sidebar condicional

```jsx
function Layout({ mostrarSidebar, children }) {
  return (
    <div className={mostrarSidebar ? "layout com-sidebar" : "layout"}>
      {mostrarSidebar && (
        <aside className="sidebar">
          <nav>Menu lateral</nav>
        </aside>
      )}
      <main>{children}</main>
    </div>
  );
}
```

## Desafios extras

### Desafio A — três abas

```jsx
const [aba, setAba] = useState("perfil");

return (
  <div>
    <nav>
      <button onClick={() => setAba("perfil")}>Perfil</button>
      <button onClick={() => setAba("config")}>Config</button>
      <button onClick={() => setAba("ajuda")}>Ajuda</button>
    </nav>

    {aba === "perfil" && <SecaoPerfil />}
    {aba === "config" && <SecaoConfig />}
    {aba === "ajuda" && <SecaoAjuda />}
  </div>
);
```

### Desafio B — banner de status

```jsx
{status === "online" && <div className="banner verde">Conectado</div>}
{status === "offline" && <div className="banner vermelho">Sem conexão</div>}
{status === "manutencao" && <div className="banner amarelo">Em manutenção</div>}
```

### Desafio C — conteúdo condicional dentro de card

```jsx
<Card>
  {usuario.premium ? (
    <span className="badge-premium">⭐ Premium</span>
  ) : (
    <button>Fazer upgrade</button>
  )}
</Card>
```

## Critérios de verificação

- Early returns para estados excludentes (loading, erro, não logado)
- `&&` para seções opcionais dentro do layout principal
- Ternário quando há alternativa (A ou B)
- `key` nos itens condicionais de listas
- Números forçados a booleano (`count > 0 &&`)

## Erros comuns

| Erro | Correção |
| --- | --- |
| `itens.length && <Lista />` | `itens.length > 0 &&` — 0 renderiza |
| Early return depois de hooks | Hooks sempre no topo — return condicional vem depois |
| Ternário gigante aninhado | Acima de 3 ramos, extraia para variável ou componente |
| Esquecer `()` em JSX multilinha | `{cond && (\n<p>...\n)}` precisa dos parênteses |
