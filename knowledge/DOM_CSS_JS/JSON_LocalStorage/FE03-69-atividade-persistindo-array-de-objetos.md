# FE03-69 — Atividade: Persistindo Array de Objetos no LocalStorage

## Objetivo

Persistir uma lista de tarefas (array de objetos) no localStorage — adicionando, removendo e marcando como concluídas — garantindo que os dados sobrevivam ao recarregamento da página.

## Estrutura de dados

```javascript
// Cada tarefa é um objeto
const tarefa = {
  id: 1,
  texto: "Estudar JavaScript",
  concluida: false,
  criadaEm: "2024-01-15T10:30:00.000Z"
};
```

## Wrapper de storage reutilizável

```javascript
const storage = {
  get(chave, fallback = null) {
    try {
      const texto = localStorage.getItem(chave);
      return texto !== null ? JSON.parse(texto) : fallback;
    } catch {
      return fallback;
    }
  },

  set(chave, valor) {
    localStorage.setItem(chave, JSON.stringify(valor));
  }
};
```

## Módulo de tarefas

```javascript
const CHAVE = "tarefas";

function carregarTarefas() {
  return storage.get(CHAVE, []); // fallback: array vazio
}

function salvarTarefas(tarefas) {
  storage.set(CHAVE, tarefas);
}

function proximoId(tarefas) {
  return tarefas.length ? Math.max(...tarefas.map(t => t.id)) + 1 : 1;
}
```

## Operações CRUD

### Adicionar

```javascript
function adicionarTarefa(texto) {
  const tarefas = carregarTarefas();

  const nova = {
    id: proximoId(tarefas),
    texto,
    concluida: false,
    criadaEm: new Date().toISOString()
  };

  const atualizadas = [...tarefas, nova];
  salvarTarefas(atualizadas);
  return atualizadas;
}
```

### Alternar concluída

```javascript
function alternarTarefa(id) {
  const tarefas = carregarTarefas().map(t =>
    t.id === id ? { ...t, concluida: !t.concluida } : t
  );

  salvarTarefas(tarefas);
  return tarefas;
}
```

### Remover

```javascript
function removerTarefa(id) {
  const filtradas = carregarTarefas().filter(t => t.id !== id);
  salvarTarefas(filtradas);
  return filtradas;
}
```

### Limpar concluídas

```javascript
function limparConcluidas() {
  const pendentes = carregarTarefas().filter(t => !t.concluida);
  salvarTarefas(pendentes);
  return pendentes;
}
```

## Integrando com a interface

```javascript
function renderizar() {
  const tarefas = carregarTarefas();
  const lista = document.querySelector("#lista-tarefas");

  lista.innerHTML = tarefas
    .map(t => `
      <li class="${t.concluida ? "concluida" : ""}">
        <span>${t.texto}</span>
        <button data-id="${t.id}" data-acao="alternar">✓</button>
        <button data-id="${t.id}" data-acao="remover">✕</button>
      </li>
    `)
    .join("");
}

// Delegação de eventos — um listener para toda a lista
document.querySelector("#lista-tarefas").addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const id = Number(btn.dataset.id);
  const acao = btn.dataset.acao;

  if (acao === "alternar") alternarTarefa(id);
  if (acao === "remover") removerTarefa(id);

  renderizar();
});

// Formulário de nova tarefa
document.querySelector("#form-tarefa").addEventListener("submit", (e) => {
  e.preventDefault();
  const input = document.querySelector("#input-tarefa");
  const texto = input.value.trim();

  if (texto) {
    adicionarTarefa(texto);
    input.value = "";
    renderizar();
  }
});

// Carga inicial — restaura o que estava salvo
renderizar();
```

## Testando a persistência

1. Adicione 3 tarefas
2. Recarregue a página (`F5`) — as tarefas continuam lá
3. Marque uma como concluída e recarregue — o estado se mantém
4. Abra DevTools → Application → Local Storage → veja a chave `tarefas`
5. `localStorage.removeItem("tarefas")` no console e recarregue — lista vazia

## Critérios de verificação

- Dados persistem entre recarregamentos e fechamento do navegador
- `JSON.stringify` na gravação, `JSON.parse` na leitura
- Fallback `[]` evita `null` quando a chave não existe
- Cada operação (adicionar, remover, alternar) salva o array completo
- IDs únicos gerados via `Math.max` dos existentes (ou `Date.now()`)

## Erros comuns a evitar

| Erro | Por que falha |
| --- | --- |
| `storage.get("tarefas")` sem fallback | Retorna `null` na primeira vez — `.map` quebra |
| `tarefas.push(nova)` sem re-salvar | O array em memória muda, mas o localStorage não — sempre `set` depois |
| `id: tarefas.length + 1` como ID | Após remoções, IDs se repetem — use `Math.max` ou timestamp |
| Salvar o elemento DOM em vez do dado | `localStorage` não salva DOM — salve os dados e re-renderize |
