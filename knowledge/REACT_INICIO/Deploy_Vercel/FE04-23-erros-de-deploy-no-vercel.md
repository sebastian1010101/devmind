# FE04-23 — Erros de Deploy no Vercel

## Os erros mais comuns

O build funciona localmente, mas falha na Vercel — quase sempre é uma das causas abaixo.

## 1. Case sensitivity — o clássico

Linux (Vercel) diferencia maiúsculas; o seu sistema local pode não diferenciar:

```jsx
// ❌ Local funciona (Windows/Mac case-insensitive), Vercel quebra
import Card from "./components/card";   // arquivo: Card.jsx
import "./styles.css";                  // arquivo: Styles.css

// ✅ Case exato do arquivo
import Card from "./components/Card";
import "./Styles.css";
```

**Diagnóstico:** `Could not resolve './components/card'` no log de build.

## 2. Dependências não instaladas

```jsx
// Código usa axios mas não está no package.json
import axios from "axios"; // Module not found
```

**Causa:** `npm install axios` rodou mas não commitou o `package.json` atualizado, ou o pacote está em `devDependencies` quando deveria estar em `dependencies`.

```bash
npm install axios        # vai para dependencies
git add package.json package-lock.json
git commit -m "chore: add axios"
git push
```

## 3. Variáveis de ambiente ausentes

```javascript
// Local tem .env, Vercel não
const api = import.meta.env.VITE_API_URL; // undefined na Vercel
```

**Solução:** cadastrar no painel `Settings → Environment Variables`. Lembre: no Vite a variável precisa do prefixo `VITE_` — e `.env` **não** deve ser commitado (mas as variáveis precisam existir no painel).

## 4. Rotas SPA retornam 404

Acessar `meu-app.vercel.app/produtos` direto dá 404 — o servidor não conhece a rota do React Router:

```json
// vercel.json — solução
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

## 5. Erros de ESLint/TypeScript tratados como falha

Warnings locais viram falha de build na Vercel quando variáveis de CI tratam warnings como erro:

```bash
# O log mostra:
Treating warnings as errors because process.env.CI = true
```

**Soluções:**

```bash
# Corrige o warning localmente (recomendado)
npm run lint -- --fix
```

Ou configure `CI=false` nas variáveis de ambiente da Vercel (contorno — melhor corrigir).

## 6. Caminhos de imagem quebrados

```jsx
// ❌ Caminho absoluto local — não existe na Vercel
<img src="/home/user/projeto/foto.png" />
<img src="C:\projeto\logo.png" />

// ✅ Import como módulo (src/assets)
import logo from "./assets/logo.png";
<img src={logo} />

// ✅ Public (caminho da raiz)
<img src="/logo.png" />
```

## 7. Node version incompatível

A Vercel usa uma versão específica do Node — declare a sua:

```json
// package.json
{
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Debugando o build

1. **Leia o log de deploy** na Vercel — a última linha de erro é a causa real
2. **Reproduza localmente** — `npm run build` deve falhar igual
3. **`npm run preview`** — testa o build de produção localmente antes de subir

## Erros no log vs erros no browser

| Sintoma | Onde está |
| --- | --- |
| Build falha na Vercel | Log do deploy — erro de compilação |
| Deploy ok, página branca | Console do navegador — erro de runtime |
| Build ok, rota 404 | Falta `vercel.json` com rewrites |
| Funciona local, falha na Vercel | Case sensitivity ou env vars |

## Checklist anti-erro

- Imports com case exato dos arquivos
- `package.json` commitado com todas as dependências
- `npm run build` passa localmente
- Variáveis `VITE_*` no painel da Vercel
- `vercel.json` com rewrites para SPA
- Imagens em `public/` ou importadas — nunca caminho local
