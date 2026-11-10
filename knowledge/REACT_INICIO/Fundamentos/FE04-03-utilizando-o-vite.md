# FE04-03 — Utilizando o Vite

## O que é o Vite

**Vite** (francês para "rápido") é a ferramenta de build padrão para projetos React modernos — substituiu o `create-react-app` como a forma recomendada de iniciar. Criado por Evan You (autor do Vue.js), o Vite resolve o problema central do tooling front-end: velocidade.

## Por que Vite em vez de create-react-app

| Aspecto | Vite | create-react-app (CRA) |
| --- | --- | --- |
| Velocidade do dev server | Instantâneo (~ms) | Lento (~segundos) |
| Hot Module Replacement | Instantâneo | Lento |
| Build de produção | Rollup (otimizado) | Webpack |
| Manutenção | Ativo | Descontinuado oficialmente |
| Suporte | React, Vue, Svelte, vanilla | Só React |

O CRA usava bundling completo — reprocessava tudo a cada mudança. O Vite serve módulos ES nativos diretamente ao navegador em desenvolvimento — mudança de arquivo = reload parcial instantâneo.

## Criando o projeto

```bash
# Cria um novo projeto React com Vite
npm create vite@latest meu-app -- --template react

# Entra na pasta
cd meu-app

# Instala as dependências
npm install

# Sobe o servidor de desenvolvimento
npm run dev
```

O terminal mostra:

```text
  VITE v5.x.x  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Acesse `http://localhost:5173` — o projeto React está rodando.

## Estrutura gerada

```text
meu-app/
├── node_modules/          ← dependências
├── public/
│   └── vite.svg           ← assets estáticos públicos
├── src/
│   ├── assets/            ← imagens importadas
│   ├── App.css            ← estilos do componente raiz
│   ├── App.jsx            ← componente raiz da aplicação
│   ├── index.css          ← estilos globais
│   └── main.jsx           ← ponto de entrada
├── .gitignore
├── index.html             ← HTML único (SPA)
├── package.json           ← scripts e dependências
└── vite.config.js         ← configuração do Vite
```

## O ponto de entrada: main.jsx

```jsx
// src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

O fluxo: `index.html` tem um `<div id="root">` vazio → `main.jsx` monta o `<App />` dentro dele → todo o React vive dentro dessa div.

## O HTML base: index.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Meu App</title>
</head>
<body>
  <div id="root"></div>        <!-- React monta aqui -->
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

Diferença crucial: uma aplicação React é uma **Single Page Application** — existe um único HTML, e o JavaScript gerencia todo o conteúdo.

## O componente raiz: App.jsx

```jsx
// src/App.jsx
import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <h1>Meu App React</h1>
      <button onClick={() => setCount(c => c + 1)}>
        Contagem: {count}
      </button>
    </div>
  )
}

export default App
```

## Scripts do package.json

```json
{
  "scripts": {
    "dev": "vite",            // servidor de desenvolvimento
    "build": "vite build",    // build de produção → dist/
    "preview": "vite preview", // testa o build localmente
    "lint": "eslint ."        // análise de código
  }
}
```

### Fluxo de trabalho

```bash
npm run dev       # desenvolvimento — localhost:5173
npm run build     # produção — gera a pasta dist/
npm run preview   # testa o build antes de deployar
```

## Hot Module Replacement (HMR)

O superpoder do Vite: ao salvar um arquivo, **só aquele componente** é atualizado no navegador — sem reload da página inteira e sem perder o estado.

```jsx
// Edite o texto e salve — a mudança aparece instantaneamente
// O estado do contador continua intacto durante a edição
```

## Configurações comuns no vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,       // muda a porta padrão
    open: true,       // abre o navegador automaticamente
  },
  build: {
    outDir: 'dist',   // pasta de saída do build
  }
})
```

## Erros comuns

| Erro | Causa |
| --- | --- |
| `npm create vite` falha | Node desatualizado — precisa v18+ |
| `npm run dev` — comando não encontrado | Faltou `npm install` |
| Página em branco | Erro de sintaxe em JSX — confira o console do navegador |
| `Cannot find module` | Caminho de import errado ou falta extensão `.jsx` |
| Porta ocupada | `npm run dev -- --port 3001` ou mude em `vite.config.js` |

## Resumo

- `npm create vite@latest` → projeto React moderno em segundos
- `npm run dev` → servidor com HMR instantâneo
- `src/main.jsx` → ponto de entrada que monta `<App />` no `#root`
- `npm run build` → gera `dist/` otimizada para produção
- Vite é o padrão atual — CRA está obsoleto
