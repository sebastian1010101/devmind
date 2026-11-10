# FE03-18 — Introdução ao Figma

## O que é o Figma?

O **Figma** é a ferramenta de design de interfaces (UI/UX) mais utilizada no mercado global de tecnologia. Ele roda diretamente no navegador de forma colaborativa em tempo real e permite que designers construam protótipos visuais e passem as especificações exatas para os desenvolvedores front-end (*Design Handoff*).

---

## O Modo de Inspeção de Código (Dev Mode)

Para desenvolvedores, o recurso mais importante é o **Dev Mode** (Modo Desenvolvedor), que permite clicar em qualquer componente visual do protótipo e inspecionar suas propriedades técnicas exatas:

- **Dimensões e Espaçamentos:** largura, altura, preenchimentos internos (`padding`) e margens de afastamento até os elementos vizinhos (basta segurar a tecla `Alt` / `Option` e passar o mouse).
- **Cores Exatas:** códigos hexadecimais, RGB e variáveis de cor do projeto.
- **Tipografia:** família de fontes, peso (`font-weight`), tamanho (`font-size`) e altura de linha (`line-height`).
- **Exportação de Ativos (Assets):** download de ícones em vetor (`SVG`) e fotos em `WebP` ou `PNG`.

---

## Traduzindo o Layout do Figma para HTML e CSS

Ao receber um layout no Figma, siga um fluxo estruturado:

1. **Visão Macroscópica:** identifique as grandes seções semânticas da página (`<header>`, `<main>`, `<section>`, `<footer>`).
2. **Definição de Design Tokens:** extraia a paleta de cores primárias, secundárias e neutras, além das fontes base para transformá-las em **Variáveis CSS**.
3. **Mapeamento de Containers:** verifique se os elementos estão centralizados com largura fixa máxima (padrão de `.container`).
4. **Construção dos Componentes:** monte as caixas individuais (cards, botões, barras de navegação) utilizando Flexbox conforme os alinhamentos medidos.
