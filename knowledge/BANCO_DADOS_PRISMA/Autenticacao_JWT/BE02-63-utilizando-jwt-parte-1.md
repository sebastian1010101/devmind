# BE02-63 — Utilizando JWT — Parte 1

## Setup

```bash
npm install jsonwebtoken
npm install -D @types/jsonwebtoken
```

## sign — emitindo o token

```ts
import jwt from "jsonwebtoken";

const token = jwt.sign(
  { email: usuario.email },              // payload — dados mínimos
  process.env.JWT_SECRET as string,      // segredo (do .env)
  {
    subject: usuario.id.toString(),      // sub → quem é
    expiresIn: "1d",                     // exp → validade
  }
);
```

```ts
// response do login
return res.json({ accessToken: token });
```

## `expiresIn` — formatos

| Valor | Significa |
| --- | --- |
| `"15m"` | 15 minutos |
| `"1h"` | 1 hora |
| `"1d"` | 1 dia |
| `3600` | 3600 segundos |

APIs comuns: `15m`–`1h` para access token; refresh token separado para sessão longa.

## O segredo

```env
JWT_SECRET="uma-string-longa-e-aleatoria-de-pelo-menos-32-chars"
```

- Aleatório e comprido — `openssl rand -base64 48` gera um
- No `.env`, nunca no código
- Vazou → todo mundo forja tokens — rotacione

## O que colocar no payload

```ts
// ✅ mínimo — identidade
{ sub: usuario.id, email: usuario.email }

// ❌ demais
{ senha, cpf, dadosPessoais }   // visível a qualquer um
```

Quanto menor o payload, melhor — trafega em toda requisição.

## Decodificando para debug

```ts
const decoded = jwt.decode(token);   // só lê — não verifica!
// { email: "...", sub: "42", iat: ..., exp: ... }
```

`jwt.io` cola o token e mostra o payload — útil em desenvolvimento.

## sign síncrono vs assíncrono

```ts
jwt.sign(payload, secret, options)              // síncrono — retorna token
jwt.sign(payload, secret, options, callback)    // assíncrono
```

O síncrono é o padrão nas APIs — a operação é rápida.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `secretOrPrivateKey must have a value` | `JWT_SECRET` não carregou — confira `.env` e `dotenv` |
| Payload gigante | Mínimo necessário — id/email bastam |
| Token sem expiração | Sempre `expiresIn` — token eterno é risco |
| Senha no payload | Payload é legível — nunca |

## Resumo

- `jwt.sign(payload, secret, { subject, expiresIn })` emite o token
- `subject` = id do usuário; `expiresIn` sempre definido
- Segredo no `.env`, forte e longo — vazou = forja livre
- `jwt.decode` lê sem verificar — debug only
