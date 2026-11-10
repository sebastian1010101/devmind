# FE03-72 — Exemplos Práticos de Uso do LocalStorage

## Exemplo 1 — Tema claro/escuro persistente

O caso mais clássico: o usuário escolhe o tema e a preferência sobrevive ao reload.

```javascript
const CHAVE_TEMA = "app:tema";

function aplicarTema(tema) {
  document.documentElement.dataset.tema = tema;
  localStorage.setItem(CHAVE_TEMA, tema);
}

// Ao carregar — restaura ou usa o padrão do sistema
const salvo = localStorage.getItem(CHAVE_TEMA);
const tema = salvo || (matchMedia("(prefers-color-scheme: dark)").matches ? "escuro" : "claro");
document.documentElement.dataset.tema = tema;

// Botão de alternância
document.querySelector("#toggle-tema").addEventListener("click", () => {
  const atual = document.documentElement.dataset.tema;
  aplicarTema(atual === "claro" ? "escuro" : "claro");
});
```

```css
:root[data-tema="escuro"] {
  --bg: #1a1a1a;
  --texto: #eee;
}
:root[data-tema="claro"] {
  --bg: #fff;
  --texto: #222;
}
```

## Exemplo 2 — Rascunho de formulário

Salva o que o usuário digita, protegendo contra perda acidental:

```javascript
const CAMPOS = ["nome", "email", "mensagem"];
const CHAVE = "form:rascunho";

// Salva a cada mudança
CAMPOS.forEach(id => {
  document.querySelector(`#${id}`).addEventListener("input", () => {
    const rascunho = {};
    CAMPOS.forEach(c => rascunho[c] = document.querySelector(`#${c}`).value);
    localStorage.setItem(CHAVE, JSON.stringify(rascunho));
  });
});

// Ao carregar — restaura
const rascunho = JSON.parse(localStorage.getItem(CHAVE) || "{}");
CAMPOS.forEach(c => {
  if (rascunho[c]) document.querySelector(`#${c}`).value = rascunho[c];
});

// Ao enviar — limpa o rascunho
document.querySelector("#form").addEventListener("submit", () => {
  localStorage.removeItem(CHAVE);
});
```

## Exemplo 3 — Carrinho de compras

```javascript
const CHAVE = "loja:carrinho";

const carrinho = {
  ler() {
    return JSON.parse(localStorage.getItem(CHAVE) || "[]");
  },

  adicionar(produto) {
    const itens = this.ler();
    const existente = itens.find(i => i.id === produto.id);

    if (existente) {
      existente.qtd += 1;
    } else {
      itens.push({ ...produto, qtd: 1 });
    }

    localStorage.setItem(CHAVE, JSON.stringify(itens));
  },

  remover(id) {
    const filtrados = this.ler().filter(i => i.id !== id);
    localStorage.setItem(CHAVE, JSON.stringify(filtrados));
  },

  total() {
    return this.ler().reduce((acc, i) => acc + i.preco * i.qtd, 0);
  },

  limpar() {
    localStorage.removeItem(CHAVE);
  }
};
```

## Exemplo 4 — Flag de onboarding ("já viu o tutorial")

```javascript
const CHAVE = "app:onboarding-visto";

if (!localStorage.getItem(CHAVE)) {
  mostrarTutorial();
  localStorage.setItem(CHAVE, "true");
}
```

## Exemplo 5 — Histórico de buscas recentes

```javascript
const CHAVE = "busca:historico";
const LIMITE = 10;

function registrarBusca(termo) {
  const historico = JSON.parse(localStorage.getItem(CHAVE) || "[]");

  // Remove duplicata e adiciona no início
  const atualizado = [termo, ...historico.filter(t => t !== termo)];

  localStorage.setItem(CHAVE, JSON.stringify(atualizado.slice(0, LIMITE)));
}

function historicoBuscas() {
  return JSON.parse(localStorage.getItem(CHAVE) || "[]");
}
```

## Exemplo 6 — Cache de dados de API com TTL

```javascript
const CHAVE = "api:produtos";
const TTL = 5 * 60 * 1000; // 5 minutos

async function buscarProdutos() {
  const cache = JSON.parse(localStorage.getItem(CHAVE) || "null");

  if (cache && Date.now() - cache.timestamp < TTL) {
    return cache.dados; // cache válido
  }

  const resposta = await fetch("/api/produtos");
  const dados = await resposta.json();

  localStorage.setItem(CHAVE, JSON.stringify({
    dados,
    timestamp: Date.now()
  }));

  return dados;
}
```

## Exemplo 7 — Preferências de acessibilidade

```javascript
const CHAVE = "app:acessibilidade";

function salvarPreferencias({ fonteMaior, altoContraste }) {
  localStorage.setItem(CHAVE, JSON.stringify({ fonteMaior, altoContraste }));
  document.documentElement.classList.toggle("fonte-maior", fonteMaior);
  document.documentElement.classList.toggle("alto-contraste", altoContraste);
}

// Ao carregar
const prefs = JSON.parse(localStorage.getItem(CHAVE) || "null");
if (prefs) salvarPreferencias(prefs);
```

## Padrões transversais

| Padrão | Técnica |
| --- | --- |
| Chave namespaced | `"app:nome"` evita colisões |
| Fallback seguro | `JSON.parse(... \|\| "{}")` ou `try/catch` |
| Imutabilidade | Leia → modifique → salve o array/objeto completo |
| TTL manual | `timestamp` embutido no objeto salvo |
| Limpeza | `removeItem` ao completar a ação (ex: form enviado) |
| Limite de tamanho | `slice(0, N)` para históricos e listas |
