# FE04-00 — Configuração de Ambiente: VS Code e Extensões Úteis

## O setup para React

Antes de escrever uma linha de JSX, o ambiente precisa estar pronto. O toolkit padrão do desenvolvedor React é minimalista — Node.js, VS Code e um conjunto enxuto de extensões que economizam horas de trabalho.

## Pré-requisito: Node.js

React roda no navegador, mas o *tooling* (Vite, npm, bundlers) precisa do Node instalado:

```bash
node --version  # verifique se está instalado — recomendado: LTS v18+
npm --version   # gerenciador de pacotes, vem junto
```

Baixe a versão **LTS** em [nodejs.org](https://nodejs.org) — é a mais estável para desenvolvimento.

## Extensões essenciais do VS Code

### 1. ES7+ React/Redux/React-Native snippets

A extensão mais importante para React. Atalhos que geram estruturas inteiras:

```text
rafce  → React Arrow Function Component Export
rfce   → React Function Component Export
imr    → import React
imp    → import módulo
```

```jsx
// Digitando 'rafce' + Tab, gera:
import React from 'react'

const Componente = () => {
  return (
    <div>Componente</div>
  )
}

export default Componente
```

### 2. Prettier — Code formatter

Formata o código automaticamente ao salvar — indentação, aspas, ponto e vírgula consistentes. Configure no `settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### 3. ESLint

Análise estática em tempo real — aponta erros de sintaxe, hooks mal usados e padrões problemáticos enquanto você digita. Em projetos React, o ESLint vem configurado pelo Vite.

### 4. Auto Rename Tag

Renomeia a tag de fechamento automaticamente quando você muda a de abertura — essencial em JSX:

```jsx
// Muda <div> para <section> — o </div> vira </section> sozinho
<section>conteúdo</section>
```

### 5. Error Lens

Mostra os erros do ESLint **inline**, na linha onde ocorrem — em vez de escondê-los no painel de problemas.

### 6. Live Server (para HTML/CSS puro)

Útil para os módulos anteriores — no React, quem serve é o Vite, então não é necessário aqui.

## Extensões recomendadas (opcionais)

| Extensão | Utilidade |
| --- | --- |
| **vscode-icons** | Ícones de arquivo que ajudam a navegar `src/` |
| **Path Intellisense** | Autocomplete de caminhos em `import` |
| **Color Highlight** | Pré-visualiza cores hex/rgb no CSS |
| **GitLens** | Blame e histórico Git inline |
| **Console Ninja** | Logs do `console.log` inline no editor |

## Configuração recomendada do VS Code

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  },
  "files.autoSave": "afterDelay"
}
```

O `emmet.includeLanguages` habilita Emmet em arquivos `.jsx`/`.tsx` — digitar `div.container>ul>li*3` expande a estrutura inteira.

## Estrutura de pastas do projeto

Todo projeto React criado com Vite segue esta base:

```text
meu-app/
├── node_modules/     ← dependências (não versionar)
├── public/           ← assets estáticos
├── src/
│   ├── assets/       ← imagens, fontes
│   ├── components/   ← componentes reutilizáveis
│   ├── App.jsx       ← componente raiz
│   ├── main.jsx      ← ponto de entrada
│   └── index.css     ← estilos globais
├── index.html        ← HTML base (único do projeto)
├── package.json      ← dependências e scripts
└── vite.config.js    ← configuração do Vite
```

## Checklist do ambiente

- Node.js LTS instalado (`node -v`)
- VS Code com ES7+ snippets, Prettier, ESLint e Auto Rename Tag
- `formatOnSave` ativado
- Emmet habilitado para JSX
- Terminal integrado configurado (`Ctrl+\``)

Com o ambiente pronto, o próximo passo é criar o primeiro projeto com **Vite**.
