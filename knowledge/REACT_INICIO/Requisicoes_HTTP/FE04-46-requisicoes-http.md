# FE04-46 — Requisições HTTP

## O que é uma requisição HTTP

Toda vez que um app React busca dados de um servidor — lista de produtos, perfil de usuário, posts — está fazendo uma **requisição HTTP**: o cliente (navegador) pergunta, o servidor responde.

```text
Cliente (React)                    Servidor (API)
      │                                 │
      │──── GET /api/produtos ─────────►│
      │                                 │── processa, consulta banco
      │◄─── 200 OK + JSON ─────────────│
      │                                 │
      │──── POST /api/usuarios ────────►│
      │     { nome: "Ana" }             │── cria registro
      │◄─── 201 Created ───────────────│
```

## Os verbos HTTP

| Verbo | Operação | Exemplo |
| --- | --- | --- |
| `GET` | Ler dados | Listar produtos |
| `POST` | Criar | Cadastrar usuário |
| `PUT` | Substituir completo | Atualizar perfil inteiro |
| `PATCH` | Atualizar parcial | Mudar só o e-mail |
| `DELETE` | Remover | Excluir post |

## Anatomia de uma requisição

```text
GET /api/usuarios/42 HTTP/1.1          ← método + endpoint
Host: api.exemplo.com                   ← host
Authorization: Bearer token123          ← header de auth
Content-Type: application/json          ← tipo do corpo

{"nome": "Ana"}                         ← body (POST/PUT/PATCH)
```

### Status codes essenciais

| Código | Significado |
| --- | --- |
| `200` | Sucesso |
| `201` | Criado com sucesso |
| `204` | Sucesso sem conteúdo (delete) |
| `400` | Requisição malformada |
| `401` | Não autenticado |
| `403` | Sem permissão |
| `404` | Não encontrado |
| `500` | Erro no servidor |

## JSON — o formato universal

Requisições e respostas trafegam JSON (visto no módulo anterior):

```javascript
// Enviando
body: JSON.stringify({ nome: "Ana" })

// Recebendo
const dados = await resposta.json();
```

## APIs REST — o padrão

APIs REST organizam endpoints por recurso:

```text
GET    /api/produtos        → lista todos
GET    /api/produtos/42     → um específico
POST   /api/produtos        → cria
PUT    /api/produtos/42     → atualiza completo
PATCH  /api/produtos/42     → atualiza parcial
DELETE /api/produtos/42     → remove
```

## Requisição vs Promise — o modelo async

Requisições são **assíncronas** — demoram e não bloqueiam o código:

```javascript
// fetch retorna uma Promise
const promessa = fetch("/api/produtos");

promessa
  .then(res => res.json())   // resposta → JSON
  .then(dados => console.log(dados))
  .catch(erro => console.error(erro));
```

Ou com `async/await` (a forma moderna):

```javascript
async function buscar() {
  const res = await fetch("/api/produtos");
  const dados = await res.json();
  console.log(dados);
}
```

## Requisições no React — onde vivem

```text
Componente monta → useEffect → fetch → setDados → re-render com dados
```

O `useEffect` é o lugar das requisições — executa depois do render, sem bloquear a UI. Detalhes no próximo bloco (FE04-50+).

## Erros comuns

| Erro | Correção |
| --- | --- |
| `fetch` sem `.json()` | Retorna `Response`, não os dados |
| Esquecer `async/await` | Promise não resolvida — dados `undefined` |
| Requisição no corpo do componente | Loop infinito — use `useEffect` |
| `Content-Type` ausente no POST | Servidor não entende o body |
| 404 confundido com CORS | 404 = rota errada; CORS = bloqueio de origem |
