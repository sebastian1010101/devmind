# FE03-74 — Cruzando Dados Entre Páginas Utilizando LocalStorage

## O problema

Numa aplicação de múltiplas páginas (MPA — Multi-Page Application), cada página é um HTML separado com seu próprio JavaScript. Como passar dados entre elas sem backend?

`localStorage` é a resposta — ele é **compartilhado por todas as páginas da mesma origem**.

## O fluxo

```text
pagina-a.html                localStorage                pagina-b.html
┌─────────────────┐         ┌──────────────┐            ┌─────────────────┐
│ usuário digita  │  set    │              │   get      │ lê e exibe os   │
│ dados → salva   │ ──────► │ "nome": "Ana"│ ─────────► │ dados salvos    │
└─────────────────┘         └──────────────┘            └─────────────────┘
```

## Exemplo: formulário → página de perfil

### Página 1 — formulário (salva)

```javascript
// form.html
document.querySelector("#form").addEventListener("submit", (e) => {
  e.preventDefault();

  const dados = {
    nome: e.target.nome.value,
    email: e.target.email.value
  };

  localStorage.setItem("app:perfil", JSON.stringify(dados));
  window.location.href = "perfil.html"; // navega para a outra página
});
```

### Página 2 — perfil (recupera)

```javascript
// perfil.html
const perfil = JSON.parse(localStorage.getItem("app:perfil") || "null");

if (perfil) {
  document.querySelector("#nome").textContent = perfil.nome;
  document.querySelector("#email").textContent = perfil.email;
} else {
  // Não há dados — redireciona de volta
  window.location.href = "form.html";
}
```

## Sincronização em tempo real: evento `storage`

Quando uma aba altera o `localStorage`, as **outras abas** da mesma origem recebem um evento `storage` — sincronização automática entre páginas abertas:

```javascript
// Em qualquer página — escuta mudanças feitas por outras abas
window.addEventListener("storage", (e) => {
  console.log("Chave alterada:", e.key);
  console.log("Valor antigo:", e.oldValue);
  console.log("Valor novo:", e.newValue);

  if (e.key === "app:tema") {
    aplicarTema(e.newValue);
  }
});
```

⚠️ O evento `storage` **não dispara na aba que fez a alteração** — só nas outras. A aba atual já sabe o que mudou.

## Casos de uso entre páginas

### Carrinho que persiste entre catálogo e checkout

```javascript
// catalogo.html
function adicionarAoCarrinho(produto) {
  const itens = JSON.parse(localStorage.getItem("carrinho") || "[]");
  itens.push(produto);
  localStorage.setItem("carrinho", JSON.stringify(itens));
}

// checkout.html
function renderizarCarrinho() {
  const itens = JSON.parse(localStorage.getItem("carrinho") || "[]");
  // renderiza os itens adicionados na página anterior
}
```

### Tema compartilhado entre todas as páginas

```javascript
// Em TODAS as páginas — script compartilhado
const tema = localStorage.getItem("app:tema") || "claro";
document.documentElement.dataset.tema = tema;

// Em qualquer página, ao mudar:
localStorage.setItem("app:tema", novoTema);
document.documentElement.dataset.tema = novoTema;
```

### Filtros que sobrevivem à navegação

```javascript
// listagem.html — salva o estado do filtro
function salvarFiltros() {
  const filtros = {
    categoria: selectCategoria.value,
    ordenacao: selectOrdem.value,
    busca: inputBusca.value
  };
  sessionStorage.setItem("filtros", JSON.stringify(filtros));
}

// Ao voltar — restaura os filtros aplicados
const filtros = JSON.parse(sessionStorage.getItem("filtros") || "null");
if (filtros) aplicarFiltros(filtros);
```

## Alternativas ao localStorage para passar dados

| Método | Escopo | Duração | Tamanho |
| --- | --- | --- | --- |
| `localStorage` | Mesma origem, todas as abas | Permanente | ~5 MB |
| `sessionStorage` | Mesma origem, mesma aba | Até fechar a aba | ~5 MB |
| Query string `?id=1` | URL visível | Até navegar | ~2 KB |
| Cookies | Domínio | Configurável | ~4 KB |
| `history.state` | Entrada do histórico | Até navegar | Ilimitado |

## Boas práticas

- **Valide ao ler** — dados podem ter sido alterados ou corrompidos
- **Redirecione se ausente** — página dependente sem dados deve voltar à origem
- **Use chaves namespaced** — `"app:perfil"`, não `"dados"`
- **Limpe o que não precisa mais** — após usar, `removeItem` se for descartável
- **`sessionStorage` para temporários** — dados de uma jornada só, sem persistência longa

## Erros comuns

| Erro | Por que falha |
| --- | --- |
| Esperar `storage` na aba que alterou | O evento só dispara nas **outras** abas |
| `localStorage` em `file://` | Cada arquivo é origem isolada — precisa de servidor |
| Ler sem validar | Dado pode estar corrompido ou inexistente |
| Dados grandes entre páginas | > 5 MB estoura a quota — use IndexedDB |
