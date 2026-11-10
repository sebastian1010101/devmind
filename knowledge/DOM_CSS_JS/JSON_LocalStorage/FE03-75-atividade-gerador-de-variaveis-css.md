# FE03-75 — Atividade: Gerador de Variáveis CSS

## Objetivo

Construir um painel que permite ao usuário criar e editar **variáveis CSS** (`--cor-primaria`, `--fonte-base`, etc.) visualmente, aplicando-as em tempo real na página e persistindo as preferências no `localStorage`.

## Conceito

CSS Custom Properties são controladas por JavaScript via `style.setProperty` — combinando isso com `localStorage`, criamos um **editor de temas funcional**.

```javascript
// O coração: JavaScript controla variáveis CSS
document.documentElement.style.setProperty("--cor-primaria", "#ff6600");
```

## Estrutura HTML

```html
<div class="painel">
  <h2>Personalizar Tema</h2>

  <label>
    Cor primária:
    <input type="color" id="cor-primaria" value="#3498db">
  </label>

  <label>
    Cor de fundo:
    <input type="color" id="cor-fundo" value="#ffffff">
  </label>

  <label>
    Cor do texto:
    <input type="color" id="cor-texto" value="#222222">
  </label>

  <label>
    Tamanho da fonte:
    <input type="range" id="fonte" min="12" max="24" value="16">
  </label>

  <label>
    Borda arredondada:
    <input type="range" id="raio" min="0" max="20" value="8">
  </label>

  <button id="salvar">Salvar Tema</button>
  <button id="resetar">Restaurar Padrão</button>
</div>

<main class="preview">
  <h1>Preview</h1>
  <p>Este texto reflete as variáveis em tempo real.</p>
  <button class="btn">Botão de exemplo</button>
</main>
```

## CSS com variáveis

```css
:root {
  --cor-primaria: #3498db;
  --cor-fundo: #ffffff;
  --cor-texto: #222222;
  --fonte-base: 16px;
  --raio-borda: 8px;
}

body {
  background: var(--cor-fundo);
  color: var(--cor-texto);
  font-size: var(--fonte-base);
}

.btn {
  background: var(--cor-primaria);
  border-radius: var(--raio-borda);
  color: white;
  padding: 0.5rem 1rem;
  border: none;
}
```

## JavaScript — gerador + persistência

```javascript
const CHAVE = "app:tema-custom";

// Mapa: id do input → nome da variável CSS
const VARIAVEIS = {
  "cor-primaria": "--cor-primaria",
  "cor-fundo": "--cor-fundo",
  "cor-texto": "--cor-texto",
  "fonte": "--fonte-base",
  "raio": "--raio-borda"
};

// Sufixos por tipo (range precisa de unidade)
const SUFIXOS = {
  "fonte": "px",
  "raio": "px"
};
```

### Aplicar uma variável

```javascript
function aplicarVariavel(inputId, valor) {
  const nomeVar = VARIAVEIS[inputId];
  const sufixo = SUFIXOS[inputId] || "";
  document.documentElement.style.setProperty(nomeVar, `${valor}${sufixo}`);
}
```

### Aplicar todas (na carga e ao salvar)

```javascript
function aplicarTodas(prefs) {
  Object.keys(VARIAVEIS).forEach(inputId => {
    const input = document.getElementById(inputId);
    const valor = prefs[inputId] || input.value;

    // Atualiza o input E aplica a variável
    input.value = valor;
    aplicarVariavel(inputId, valor);
  });
}
```

### Ler o estado atual dos inputs

```javascript
function lerInputs() {
  const prefs = {};
  Object.keys(VARIAVEIS).forEach(inputId => {
    prefs[inputId] = document.getElementById(inputId).value;
  });
  return prefs;
}
```

### Eventos

```javascript
// Preview em tempo real — aplica sem salvar
Object.keys(VARIAVEIS).forEach(inputId => {
  document.getElementById(inputId).addEventListener("input", (e) => {
    aplicarVariavel(inputId, e.target.value);
  });
});

// Salvar — persiste no localStorage
document.getElementById("salvar").addEventListener("click", () => {
  const prefs = lerInputs();
  localStorage.setItem(CHAVE, JSON.stringify(prefs));
  alert("Tema salvo!");
});

// Restaurar padrão
document.getElementById("resetar").addEventListener("click", () => {
  localStorage.removeItem(CHAVE);
  location.reload(); // volta aos defaults do CSS
});
```

### Carga inicial

```javascript
const salvo = JSON.parse(localStorage.getItem(CHAVE) || "null");
if (salvo) aplicarTodas(salvo);
```

## Desafios extras

### Desafio A — salvar automaticamente (sem botão)

Troque o botão por salvamento automático com debounce:

```javascript
let timeout;
Object.keys(VARIAVEIS).forEach(inputId => {
  document.getElementById(inputId).addEventListener("input", (e) => {
    aplicarVariavel(inputId, e.target.value);
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      localStorage.setItem(CHAVE, JSON.stringify(lerInputs()));
    }, 500); // salva 500ms após a última mudança
  });
});
```

### Desafio B — exportar/importar tema como JSON

```javascript
// Exportar — copia o JSON das preferências
document.getElementById("exportar").addEventListener("click", () => {
  const prefs = localStorage.getItem(CHAVE) || "{}";
  navigator.clipboard.writeText(prefs);
});

// Importar — cola e aplica
document.getElementById("importar").addEventListener("click", async () => {
  const texto = await navigator.clipboard.readText();
  const prefs = JSON.parse(texto);
  localStorage.setItem(CHAVE, texto);
  aplicarTodas(prefs);
});
```

### Desafio C — geração dinâmica de inputs a partir de um objeto

```javascript
const ESQUEMA = [
  { id: "cor-primaria", label: "Cor Primária", tipo: "color", var: "--cor-primaria" },
  { id: "cor-fundo", label: "Cor Fundo", tipo: "color", var: "--cor-fundo" },
  { id: "fonte", label: "Fonte", tipo: "range", min: 12, max: 24, var: "--fonte-base", sufixo: "px" }
];

function gerarPainel() {
  const painel = document.querySelector(".painel");
  ESQUEMA.forEach(({ id, label, tipo, ...resto }) => {
    painel.innerHTML += `
      <label>${label}:
        <input type="${tipo}" id="${id}" ${resto.min ? `min="${resto.min}" max="${resto.max}"` : ""}>
      </label>`;
  });
}
```

## Critérios de verificação

- `style.setProperty("--nome", valor)` aplica a variável em tempo real
- Inputs refletem o estado salvo ao carregar
- Unidades CSS adicionadas (`px`, `rem`) via sufixo — não no objeto salvo
- `localStorage` persiste o tema entre sessões
- Reset volta aos valores padrão do `:root` no CSS

## Erros comuns a evitar

| Erro | Correção |
| --- | --- |
| `setProperty("fonte", "16")` | Falta a unidade — `"16px"`, use sufixo |
| Input `range` retorna string | Converta com `Number()` se precisar de cálculo |
| Salvar valores sem prefixo `--` | A variável CSS precisa de `--nome` — mapeie corretamente |
| `getPropertyValue` para ler | Para ler o valor computado: `getComputedStyle(el).getPropertyValue("--var")` |
