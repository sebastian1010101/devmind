# FE02-04 — GitHub Pages

## O que é o GitHub Pages?

O **GitHub Pages** é um serviço de hospedagem estática gratuito fornecido pelo GitHub. Ele permite publicar sites e aplicações web (HTML, CSS e JavaScript puros) diretamente a partir de um repositório no GitHub para a internet aberta, com certificado de segurança SSL (HTTPS) incluso.

---

## Requisitos Fundamentais

Para que o GitHub Pages consiga servir sua página:

1. O projeto precisa ser composto de **arquivos estáticos** (HTML, CSS, JS no navegador, imagens). Não suporta linguagens de backend com servidores ativos (como Node/Express, Python/Django, PHP ou bancos de dados SQL).
2. O arquivo principal deve estar na raiz do repositório (ou na pasta `/docs`) e chamar-se rigorosamente:

   ```text
   index.html
   ```

---

## Como Ativar o GitHub Pages no Repositório

1. Envie o seu projeto para o GitHub via terminal ou GitHub Desktop.
2. Abra a página do repositório no navegador no GitHub.
3. Clique na aba superior **Settings** (Configurações do repositório).
4. No menu lateral esquerdo, na seção *Code and automation*, clique em **Pages**.
5. Na seção **Build and deployment > Source**:
   - Deixe selecionado **Deploy from a branch**.
   - Em **Branch**, selecione a branch `main` e mantenha a pasta como `/ (root)`.
   - Clique em **Save**.
6. Aguarde cerca de 1 a 2 minutos enquanto o GitHub executa o fluxo automatizado de publicação (verificável na aba *Actions*).
7. Uma caixa azul com a URL do seu site publicado aparecerá no topo da página:

   ```text
   https://seu-usuario.github.io/nome-do-repositorio/
   ```

---

## Erros Comuns e Boas Práticas

- **Erro 404:** quase sempre acontece quando o arquivo principal foi nomeado fora do padrão (ex: `Index.html` com maiúscula, `home.html` ou dentro de subpastas não configuradas).
- **Caminhos Quebrados em Imagens e CSS:** como a URL da página inclui o nome do repositório (`/nome-do-repositorio/`), evite caminhos absolutos com barra inicial (`/style.css` ou `/img/foto.png`). Prefira sempre caminhos relativos (`./style.css` ou `img/foto.png`).
