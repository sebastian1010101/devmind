# FE03-59 — Atividade: Pesquisando por Dados

## Objetivo

Consolidar os métodos de busca — `includes`, `indexOf`, `find`, `findIndex`, `some` — construindo um sistema de pesquisa sobre uma coleção, como o campo de busca de um catálogo real.

## Cenário

Base de contatos:

```javascript
const contatos = [
  { id: 1, nome: "Ana Silva", telefone: "9999-1111", tags: ["trabalho", "familia"] },
  { id: 2, nome: "Beto Souza", telefone: "9999-2222", tags: ["amigos"] },
  { id: 3, nome: "Carla Mendes", telefone: "9999-3333", tags: ["trabalho"] },
  { id: 4, nome: "Diego Lima", telefone: "9999-4444", tags: ["familia", "amigos"] }
];
```

## Desafio 1 — Verificar existência por nome

```javascript
function existeContato(nome) {
  return contatos.some(c => c.nome.toLowerCase() === nome.toLowerCase());
}

existeContato("ana silva"); // true — insensível a maiúsculas
existeContato("João");      // false
```

## Desafio 2 — Buscar contato completo por ID

```javascript
function buscarPorId(id) {
  return contatos.find(c => c.id === id) || null;
}

buscarPorId(3); // { id: 3, nome: "Carla Mendes", ... }
buscarPorId(99); // null
```

## Desafio 3 — Posição de um contato na lista

```javascript
function posicaoDe(id) {
  return contatos.findIndex(c => c.id === id);
}

posicaoDe(2);  // 1
posicaoDe(99); // -1 — convenção para "não existe"
```

## Desafio 4 — Busca por trecho do nome

O coração de todo campo de pesquisa — `includes` dentro de `filter`:

```javascript
function pesquisar(termo) {
  const t = termo.toLowerCase();
  return contatos.filter(c => c.nome.toLowerCase().includes(t));
}

pesquisar("silva"); // [Ana Silva]
pesquisar("a");     // todos que contêm "a" no nome
```

## Desafio 5 — Contatos que possuem uma tag

Aqui `includes` opera no **array interno** de cada objeto:

```javascript
function porTag(tag) {
  return contatos.filter(c => c.tags.includes(tag));
}

porTag("familia"); // [Ana Silva, Diego Lima]
porTag("trabalho"); // [Ana Silva, Carla Mendes]
```

## Desafio 6 — Remover contato por ID

`findIndex` acha, `splice` remove (estilo mutável):

```javascript
function removerContato(id) {
  const indice = contatos.findIndex(c => c.id === id);
  if (indice !== -1) {
    return contatos.splice(indice, 1)[0]; // devolve quem foi removido
  }
  return null;
}
```

Versão imutável — retorna uma nova lista (estilo React):

```javascript
const novaLista = contatos.filter(c => c.id !== idRemover);
```

## Desafio 7 — Sistema de busca combinado

Pesquisa que cobre nome, telefone e tags ao mesmo tempo:

```javascript
function buscaGeral(termo) {
  const t = termo.toLowerCase();
  return contatos.filter(c =>
    c.nome.toLowerCase().includes(t) ||
    c.telefone.includes(t) ||
    c.tags.some(tag => tag.includes(t))
  );
}

buscaGeral("9999");  // todos — o telefone contém o trecho
buscaGeral("amigos"); // [Beto Souza, Diego Lima]
```

## Ligando à interface (DOM)

Esqueleto de como isso aparece numa página real:

```javascript
const input = document.querySelector("#busca");
const lista = document.querySelector("#resultados");

input.addEventListener("input", () => {
  const resultados = pesquisar(input.value);

  lista.innerHTML = resultados
    .map(c => `<li>${c.nome} — ${c.telefone}</li>`)
    .join("");
});
```

## Critérios de verificação

- `includes` para **existência** (retorna boolean), `find` para obter o **item**, `findIndex` para a **posição**, `some` para testar **objetos**
- Termo e campo normalizados com `.toLowerCase()` antes de comparar
- Retorno `null` (ou `-1`) tratado quando a busca não encontra nada
- `filter` + `includes` para busca textual; `some` dentro de `filter` para arrays internos

## Erros comuns a evitar

| Erro | Por que falha |
| --- | --- |
| `includes({ id: 1 })` em array de objetos | Objetos casam só por referência — use `some(c => c.id === 1)` |
| `if (lista.indexOf(x))` sem comparar | `indexOf` retorna `0` na primeira posição — `0` é falsy! Use `!== -1` |
| Esquecer `toLowerCase()` | Busca "Ana" não encontra "ana" — sempre normalize |
| `find` esperando array | `find` retorna **um** item ou `undefined`, nunca uma lista |
