# FE03-21 — Organizando Diretórios

## Arquitetura de Pastas no Front-End

Conforme os projetos web crescem, colocar todos os arquivos de estilo, scripts e imagens misturados na raiz do repositório gera desorganização e perda de produtividade.

A estruturação padronizada de diretórios é fundamental para que qualquer desenvolvedor da equipe localize recursos instantaneamente.

---

## Estrutura de Pastas Recomendada (Padrão Kenzie)

```text
meu-projeto/
├── index.html
├── src/
│   ├── assets/
│   │   ├── img/
│   │   │   ├── logo.svg
│   │   │   └── banner.webp
│   │   └── fonts/
│   ├── styles/
│   │   ├── reset.css
│   │   ├── global.css
│   │   ├── variables.css
│   │   └── components/
│   │       ├── header.css
│   │       ├── buttons.css
│   │       └── cards.css
│   └── scripts/
│       ├── index.js
│       ├── api.js
│       └── utils.js
└── README.md
```

---

## Responsabilidade de Cada Diretório

- **Raiz do Projeto:** contém o arquivo principal `index.html`, o `README.md` e arquivos de configuração (como `.gitignore`).
- **`src/` (Source):** o diretório que agrupa todo o código-fonte de desenvolvimento.
- **`src/assets/`:** arquivos estáticos de mídia, como imagens (`img/`), ícones (`icons/`) e fontes customizadas (`fonts/`).
- **`src/styles/`:** arquivos CSS divididos modularmente por propósito (variáveis, reset global e componentes isolados).
- **`src/scripts/`:** lógica JavaScript dividida por módulos funcionais.

---

## Boas Práticas de Nomenclatura

- Utilize apenas letras minúsculas (`lowercase`), sem espaços e sem acentos.
- Separe palavras compostas por traços (*kebab-case*), ex: `menu-lateral.css` ou `detalhes-produto.js`.
- Evite nomes genéricos e confusos como `arquivo1.css` ou `teste.js`.
