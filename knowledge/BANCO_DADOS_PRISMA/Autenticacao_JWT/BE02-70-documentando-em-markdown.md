# BE02-70 — Documentando em Markdown (MD)

## Por que documentar a API

Quem consome sua API (front-end, terceiros, você daqui 6 meses) precisa saber: rotas, payloads, respostas, erros. O `README.md` é o contrato.

## Estrutura de um README de API

````markdown
# Nome da API

Descrição curta — o que faz, stack usada.

## Base URL

`https://minha-api.onrender.com`

## Rodando local

```bash
npm install
cp .env.example .env   # configure as variáveis
npx prisma migrate dev
npm run dev
```

## Variáveis de ambiente

| Variável | Descrição |
| --- | --- |
| `DATABASE_URL` | Conexão Postgres |
| `JWT_SECRET` | Segredo do token |

## Endpoints

...
````

## Documentando um endpoint

````markdown
### POST /usuarios — cadastro

Cria um novo usuário.

**Body**

```json
{
  "nome": "Ana",
  "email": "ana@mail.com",
  "senha": "minimo8chars"
}
```

**Resposta — 201**

```json
{
  "id": 1,
  "nome": "Ana",
  "email": "ana@mail.com"
}
```

**Erros**

| Status | Quando |
| --- | --- |
| 409 | Email já cadastrado |
| 400 | Body inválido (campos obrigatórios) |
````

Elementos essenciais por endpoint: método + path, body de entrada, resposta de sucesso, erros possíveis, auth necessária.

## Autenticação

````markdown
## Autenticação

Rotas protegidas exigem o header:

```text
Authorization: Bearer <accessToken>
```

O token é obtido em `POST /login` e expira em 1 hora.
````

## Sintaxe útil do MD

````markdown
# H1  ## H2  ### H3            ← hierarquia
**negrito**  *itálico*  `code`
- lista / 1. numerada
| tabela | com | colunas |
```bloco de código com linguagem```
> citação
````

## Boas práticas

- Documente **erros** — não só o caminho feliz
- Exemplos reais de JSON — copie de uma resposta verdadeira
- Diga quais rotas exigem auth e qual o formato do token
- Mantenha junto do código — o `.md` desatualizado é pior que nenhum

## Erros comuns

| Erro | Correção |
| --- | --- |
| Doc sem erros possíveis | Liste 400/401/404/409 de cada rota |
| Exemplo inventado | Copie a resposta real — divergência mata a doc |
| Setup impossível de seguir | Teste o README do zero numa pasta limpa |
| JSON sem linguagem no fence | Sempre declare a linguagem do bloco — destaque de sintaxe |

## Resumo

- README de API = base URL + setup + env vars + endpoints documentados
- Cada endpoint: método, path, body, resposta de sucesso, tabela de erros
- Seção de auth explica o Bearer e como obter o token
- Doc boa é a que um estranho consegue usar sem perguntar
