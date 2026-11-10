# FE03-33 — Testando Responsividade com DevTools

## Emulando Dispositivos nas Ferramentas do Desenvolvedor

Testar páginas responsivas apenas redimensionando a janela do navegador no computador não é suficiente: navegadores móveis reais possuem densidades de pixels elevadas (*DPI / Retina Display*) e comportamentos de toque (*touch events*).

O painel **Device Mode (Modo de Dispositivo)** do DevTools permite simular aparelhos reais com precisão.

---

## Como Ativar o Device Mode

1. Abra o DevTools pressionando `F12` (ou `Ctrl + Shift + I`).
2. Clique no ícone de celular/tablet no canto superior esquerdo do painel (atalho: `Ctrl + Shift + M`).
3. A janela de visualização passa a exibir uma moldura de emulação móvel.

---

## Principais Recursos do Device Mode

- **Menu de Dispositivos Predefinidos:** alterne instantaneamente entre perfis populares como *iPhone 14/15*, *Samsung Galaxy*, *iPad Air* e *Pixel 7*.
- **Modo Responsivo Livre:** arraste as alças laterais para inspecionar qualquer largura arbitrária (ex: 375px, 768px, 1024px).
- **Orientação de Tela:** botão para alternar entre modo Retrato (*Portrait*) e Paisagem (*Landscape*).
- **Simulação de Conexão (Throttling):** teste a velocidade de carregamento em redes móveis lentas (ex: *Fast 3G* e *Slow 3G*).

---

## Como Identificar o Erro de Transbordamento (Overflow Horizontal)

O erro mais grave em interfaces responsivas é o **vazamento de conteúdo** (quando a página ganha uma barra de rolagem horizontal indesejada no celular).

Para encontrar qual elemento está transbordando no DevTools:
1. Abra a aba **Console**.
2. Execute o script de inspeção rápida:
   ```javascript
   document.querySelectorAll("*").forEach(el => {
     if (el.offsetWidth > document.documentElement.offsetWidth) {
       console.log("Elemento transbordando:", el);
     }
   });
   ```
