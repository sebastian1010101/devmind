# FE03-73 — Atividade: LocalStorage na Prática

## Objetivo

Construir um painel de preferências completo que persiste todas as configurações do usuário no localStorage — tema, idioma, tamanho de fonte e notificações — com restauração automática ao carregar.

## Estrutura

```html
<form id="preferencias">
  <label>
    Tema:
    <select name="tema">
      <option value="claro">Claro</option>
      <option value="escuro">Escuro</option>
    </select>
  </label>

  <label>
    Idioma:
    <select name="idioma">
      <option value="pt">Português</option>
      <option value="en">English</option>
      <option value="es">Español</option>
    </select>
  </label>

  <label>
    Tamanho da fonte:
    <input type="range" name="fonte" min="12" max="24" value="16">
  </label>

  <label>
    <input type="checkbox" name="notificacoes">
    Receber notificações
  </label>

  <button type="submit">Salvar</button>
</form>
```

## Implementação

### Storage helper

```javascript
const storage = {
  get(chave, fallback) {
    try {
      const t = localStorage.getItem(chave);
      return t ? JSON.parse(t) : fallback;
    } catch {
      return fallback;
    }
  },
  set(chave, valor) {
    localStorage.setItem(chave, JSON.stringify(valor));
  }
};
```

### Preferências padrão

```javascript
const PADRAO = {
  tema: "claro",
  idioma: "pt",
  fonte: 16,
  notificacoes: false
};

const CHAVE = "app:preferencias";
```

### Carregar e aplicar

```javascript
function carregar() {
  return storage.get(CHAVE, PADRAO);
}

function aplicar(prefs) {
  // Aplica no DOM
  document.documentElement.dataset.tema = prefs.tema;
  document.documentElement.lang = prefs.idioma;
  document.documentElement.style.fontSize = `${prefs.fonte}px`;

  // Preenche o formulário
  const form = document.querySelector("#preferencias");
  form.tema.value = prefs.tema;
  form.idioma.value = prefs.idioma;
  form.fonte.value = prefs.fonte;
  form.notificacoes.checked = prefs.notificacoes;
}

// Na inicialização
aplicar(carregar());
```

### Salvar ao submeter

```javascript
document.querySelector("#preferencias").addEventListener("submit", (e) => {
  e.preventDefault();
  const form = e.target;

  const prefs = {
    tema: form.tema.value,
    idioma: form.idioma.value,
    fonte: Number(form.fonte.value),
    notificacoes: form.notificacoes.checked
  };

  storage.set(CHAVE, prefs);
  aplicar(prefs);
});
```

## Desafios extras

### Desafio A — salvar automaticamente (sem botão)

```javascript
document.querySelector("#preferencias").addEventListener("input", () => {
  const form = document.querySelector("#preferencias");
  const prefs = {
    tema: form.tema.value,
    idioma: form.idioma.value,
    fonte: Number(form.fonte.value),
    notificacoes: form.notificacoes.checked
  };
  storage.set(CHAVE, prefs);
  aplicar(prefs); // aplica na hora
});
```

### Desafio B — detectar preferência do sistema na primeira visita

```javascript
function detectarPadrao() {
  const escuro = matchMedia("(prefers-color-scheme: dark)").matches;
  const idioma = navigator.language.split("-")[0]; // "pt-BR" → "pt"
  return { ...PADRAO, tema: escuro ? "escuro" : "claro", idioma };
}

// Na primeira carga, use detectarPadrao() como fallback
```

### Desafio C — botão "Restaurar padrões"

```javascript
document.querySelector("#restaurar").addEventListener("click", () => {
  storage.set(CHAVE, PADRAO);
  aplicar(PADRAO);
});
```

## Testando

1. Mude tema para escuro → recarregue → tema continua escuro
2. Altere fonte para 20 → recarregue → texto maior persistido
3. DevTools → Application → Local Storage → veja a chave `app:preferencias` como JSON
4. `localStorage.clear()` → recarregue → volta aos padrões

## Critérios de verificação

- Preferências persistem entre reloads e sessões
- `JSON.stringify`/`parse` com fallback para o objeto padrão
- Formulário reflete o estado salvo ao carregar
- Mudanças aplicadas no DOM imediatamente (não só no storage)
- `Number()` na conversão do range (volta como string)
- `checkbox` usa `.checked` (booleano), não `.value`

## Erros comuns a evitar

| Erro | Correção |
| --- | --- |
| `form.fonte.value` salvo como string | Converta com `Number()` — range retorna texto |
| `form.notificacoes.value` | Checkbox: use `.checked`, não `.value` |
| Aplicar tema sem dataset | Use `data-tema` + CSS `:root[data-tema]` |
| Sem fallback no `storage.get` | Primeira visita retorna `null` — quebra o `.tema` |
