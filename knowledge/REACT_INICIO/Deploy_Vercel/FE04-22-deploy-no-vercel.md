# FE04-22 — Deploy no Vercel

## O que é a Vercel

**Vercel** é a plataforma de hospedagem criada pelos autores do Next.js — mas funciona perfeitamente com Vite, CRA e qualquer front-end estático. Oferece deploy contínuo direto do GitHub: cada push na `main` publica automaticamente.

## Por que Vercel para React

- **Detecção automática** — reconhece Vite/React e configura o build sozinho
- **Deploy contínuo** — push → build → produção, sem intervenção
- **Preview deployments** — cada PR ganha uma URL de preview
- **HTTPS e CDN** — certificado e distribuição global automáticos
- **Gratuito** — plano hobby cobre projetos pessoais

## Fluxo de deploy

### 1. Código no GitHub

```bash
git init
git add .
git commit -m "feat: projeto react"
git remote add origin https://github.com/usuario/meu-app.git
git push -u origin main
```

### 2. Conectar na Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login com GitHub
1. Clique em **Add New → Project**
1. Selecione o repositório `meu-app`
1. A Vercel detecta o framework: **Vite**
1. Confirme as configurações (vem preenchido):

```text
Framework:   Vite
Build:       npm run build
Output:      dist
Install:     npm install
```

1. Clique em **Deploy** — em ~30s o app está no ar

### 3. URL gerada

```text
https://meu-app-xyz123.vercel.app
```

Cada push na `main` dispara um novo deploy automático.

## Via CLI (alternativa)

```bash
npm i -g vercel
vercel          # na pasta do projeto — segue o wizard
vercel --prod   # deploy direto para produção
```

## Configurações importantes

### Variáveis de ambiente

Chaves e URLs de API nunca vão no código — configure no painel:

```text
Vercel → Project → Settings → Environment Variables
```

```bash
# .env local (NÃO commitar)
VITE_API_URL=https://api.exemplo.com
```

```javascript
// No código — acesso via import.meta.env (Vite)
const api = import.meta.env.VITE_API_URL;
```

### SPA redirects

Apps React com React Router precisam que todas as rotas caiam no `index.html`:

```json
// vercel.json — na raiz do projeto
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

Sem isso, `/produtos` acessado direto retorna 404 — o servidor não conhece a rota (o React Router resolve no cliente).

## Deploy contínuo na prática

```bash
# Fluxo diário
git add .
git commit -m "feat: nova seção"
git push

# → Vercel detecta, builda e publica automaticamente
# → PR aberto gera preview: meu-app-git-feature.vercel.app
```

## Vercel vs alternativas

| Plataforma | Força |
| --- | --- |
| **Vercel** | Melhor DX para front-end, preview por PR |
| **Netlify** | Equivalente, ótimos forms/functions |
| **GitHub Pages** | Grátis, mas sem preview e sem server functions |
| **Render/Fly** | Para apps com backend junto |

## Checklist pré-deploy

- `npm run build` funciona localmente sem erros
- `npm run preview` — testa o build de produção
- Caminhos de imagem usam `public/` ou imports relativos (não caminhos absolutos locais)
- Variáveis sensíveis em `.env` e configuradas na Vercel
- `vercel.json` com rewrites se usar React Router
