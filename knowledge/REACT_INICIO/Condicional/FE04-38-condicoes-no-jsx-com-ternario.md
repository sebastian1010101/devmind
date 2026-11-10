# FE04-38 — Condições no JSX com ternário

## Por que ternário

Dentro de JSX só cabem **expressões** — `if/else` é statement, não cabe entre `{}`. O operador ternário é a expressão condicional que resolve isso:

```jsx
{condicao ? <ComponenteA /> : <ComponenteB />}
```

## Os três padrões

### 1. Ternário — se/senão

```jsx
{logado ? (
  <p>Bem-vindo, {usuario.nome}!</p>
) : (
  <button>Entrar</button>
)}
```

### 2. `&&` — renderizar só se verdadeiro

```jsx
{notificacoes.length > 0 && (
  <span className="badge">{notificacoes.length}</span>
)}
```

### 3. `||` — fallback quando falsy

```jsx
<p>{usuario.nome || "Visitante"}</p>
<img src={usuario.foto || "/avatar-padrao.png"} />
```

## A armadilha do `&&` com números

```jsx
// ❌ Se count = 0, renderiza "0" na tela!
{count && <Lista itens={itens} />}

// ✅ Force booleano
{count > 0 && <Lista itens={itens} />}
{Boolean(count) && <Lista itens={itens} />}
```

`0` é falsy mas **renderiza** — `&&` com número pode exibir `0` literalmente. Sempre force a expressão a boolean.

## Condicionais dentro de atributos

```jsx
<button className={ativo ? "botao ativo" : "botao"}>
<button disabled={carregando}>
<img src={foto || "/padrao.png"} />
<span>{online ? "🟢" : "⚫"}</span>
```

## Múltiplas condições — cadeia de ternários

```jsx
{status === "carregando" ? (
  <Spinner />
) : status === "erro" ? (
  <p>Erro ao carregar</p>
) : status === "vazio" ? (
  <p>Nenhum resultado</p>
) : (
  <Lista dados={dados} />
)}
```

Funciona, mas perde legibilidade rápido — acima de 2-3 ramificações, extraia para função ou early returns.

## Fora do JSX — early return

Quando a condição decide **se o componente renderiza**, early return é mais limpo que ternário gigante:

```jsx
function Item({ dado }) {
  if (!dado) return <p>Sem dados</p>;
  if (dado.carregando) return <Spinner />;

  return <div>{dado.conteudo}</div>;
}
```

## Extraindo para variável

```jsx
function Painel({ status }) {
  let conteudo;

  if (status === "loading") conteudo = <Spinner />;
  else if (status === "erro") conteudo = <Erro />;
  else conteudo = <Dados />;

  return <section>{conteudo}</section>;
}
```

## Mapa de decisão

| Situação | Padrão |
| --- | --- |
| Se/senão simples | `? :` |
| Renderiza só se verdadeiro | `&&` |
| Fallback para valor | `\|\|` ou `??` |
| Mais de 2-3 ramificações | Early return ou função auxiliar |
| Condicionar atributo | Ternário inline no atributo |

## Resumo

- Ternário para se/senão; `&&` para condicional simples; `||` para fallback
- `count &&` com número renderiza `0` — force booleano
- Acima de 3 ramificações, early return ou variável
- `??` (nullish) é melhor que `||` quando `0` ou `""` são valores válidos
