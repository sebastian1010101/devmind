# BE01-29 — O que é Backend e Sua Importância

## Frontend vs Backend

```text
┌──────────────┐   HTTP    ┌──────────────┐         ┌──────────┐
│   Frontend   │ ────────→ │   Backend    │ ──────→ │  Banco   │
│  (navegador) │ ←──────── │  (servidor)  │ ←────── │ de dados │
└──────────────┘   JSON    └──────────────┘         └──────────┘
```

| Frontend | Backend |
| --- | --- |
| O que o usuário vê | O que o usuário não vê |
| HTML/CSS/JS, React | Node.js, Express, APIs |
| Interface e experiência | Regras, dados, segurança |
| Roda no dispositivo do usuário | Roda no servidor |

## Por que o backend é indispensável

- **Segurança** — frontend é público: qualquer um abre o DevTools e altera. Validação, permissões e segredos (chaves de API, senhas) só existem no backend
- **Persistência** — dados compartilhados entre usuários moram no banco, não no `localStorage` de cada um
- **Regras de negócio** — cálculo de frete, limite de crédito, desconto — centralizado, não duplicado em cada cliente
- **Integrações** — gateway de pagamento, e-mail, storage — com credenciais que nunca podem vazar

## O que uma API backend faz

```text
1. Recebe a requisição (POST /usuarios, body JSON)
2. Autentica — quem é você?
3. Autoriza — você pode fazer isso?
4. Valida — os dados estão corretos?
5. Executa a regra de negócio
6. Persiste no banco
7. Responde (201 + JSON do recurso criado)
```

## O papel do Node.js

Node é o runtime; o framework (Express) organiza rotas, middlewares e respostas. O curso segue essa stack:

```text
Node.js (runtime) → Express (HTTP) → Prisma (banco, módulo 07)
```

## Resumo

- Backend = servidor: segurança, dados e regras — nunca confie no frontend
- Fluxo de API: autentica → autoriza → valida → executa → persiste → responde
- Node roda o servidor; Express organiza o HTTP
