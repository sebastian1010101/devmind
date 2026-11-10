# BE02-71 — Atividade: Documentando uma API

## Objetivo

Escrever a documentação completa da API de vagas/candidaturas — README utilizável por um front sem conhecer o código.

## O documento esperado

````markdown
# Vagas e Candidaturas API

API REST para gerenciar vagas de emprego e candidaturas.
Stack: Node.js, Express, TypeScript, PostgreSQL, Prisma, JWT.

## Base URL

`http://localhost:3000` (dev) | `https://api.onrender.com` (prod)

## Setup

```bash
npm install
cp .env.example .env
npx prisma migrate dev
npm run dev
```

## Variáveis

| Var | Descrição |
| --- | --- |
| `DATABASE_URL` | Postgres connection string |
| `JWT_SECRET` | Segredo do JWT |
| `PORT` | Porta (default 3000) |

## Autenticação

Rotas marcadas 🔒 exigem `Authorization: Bearer <token>` de `POST /auth/login`.
````

## Documentando os grupos

````markdown
## Auth

### POST /auth/register
```json
{ "nome": "Ana", "email": "a@a.com", "senha": "12345678" }
```
→ `201` usuário criado (sem senha) | `409` email duplicado

### POST /auth/login
```json
{ "email": "a@a.com", "senha": "12345678" }
```
→ `200` `{ "accessToken": "..." }` | `401` credenciais inválidas

## Vagas

### GET /vagas
Lista todas. Público.
→ `200` `[{ id, titulo, empresa, _count: { candidaturas } }]`

### POST /vagas 🔒
```json
{ "titulo": "Dev Jr", "empresa": "Kenzie", "descricao": "..." }
```
→ `201` | `401` sem token

### POST /vagas/:id/candidaturas 🔒
Candidata o usuário do token à vaga.
→ `201` candidatura | `404` vaga inexistente | `409` já candidatado

### GET /minhas-candidaturas 🔒
→ `200` `[{ id, status, criadoEm, vaga: {...} }]`
````

## Checklist de qualidade

1. Alguém consegue rodar o projeto seguindo o README
1. Todos os endpoints listados — sem rota escondida
1. Auth explicada: onde pegar o token, como enviar
1. Erros documentados por rota (não só sucesso)
1. Exemplos de JSON copiados de respostas reais
1. Env vars documentadas com `.env.example` no repo

## Erros comuns

| Erro | Correção |
| --- | --- |
| Doc genérica sem exemplos | Cada rota tem request+response real |
| Status de erro omitido | Liste 4xx — o front precisa tratar |
| Rota com 🔒 sem explicar auth | Seção dedicada ao Bearer |
| Setup incompleto | `migrate`, `.env`, `install` — todos os passos |

## Resumo

- README = contrato da API: setup, env, auth, endpoints
- Exemplos reais e erros documentados por rota
- Teste: alguém sem contexto deve conseguir usar
