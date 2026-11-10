# BE02-62 — JSON Web Token (JWT)

## O que é

Um **token** que carrega dados assinados — a API emite no login e o cliente apresenta em cada requisição. O servidor verifica a assinatura sem consultar o banco.

```text
login → servidor emite JWT → cliente guarda
                         ↓
   Authorization: Bearer <token>  →  servidor verifica assinatura → ok
```

## Anatomia — 3 partes

```text
eyJhbGciOi...  .  eyJzdWI6Ij...  .  SflKxwRJ...
   HEADER          PAYLOAD          SIGNATURE
```

```json
// HEADER — algoritmo e tipo
{ "alg": "HS256", "typ": "JWT" }

// PAYLOAD — os "claims" (dados)
{ "sub": "42", "email": "ana@mail.com", "iat": 1727..., "exp": 1727... }

// SIGNATURE — HMAC(header.payload, secret)
```

Codificado em **Base64URL** — não é criptografia, é codificação. Qualquer um decodifica.

## Claims registrados

| Claim | Significa |
| --- | --- |
| `sub` | Subject — de quem é o token (id do usuário) |
| `iat` | Issued at — quando foi emitido |
| `exp` | Expiration — quando expira |
| `iss` / `aud` | Emissor / audiência |

## ⚠️ JWT não é criptografado

```text
payload é Base64 — todo mundo lê
```

- **Nunca** coloque senha, dados sensíveis ou segredos no payload
- O que a assinatura garante é **integridade** — ninguém altera sem invalidar
- Confidencialidade exige HTTPS (canal) — o token em si é legível

## Stateless — a mágica

```text
Sessão tradicional:             JWT:
servidor guarda sessão    →     servidor só verifica assinatura
em memória/redis          →     nada guardado — escala fácil
```

O servidor não mantém estado — a assinatura garante que o token foi emitido por ele. Qualquer instância da API valida qualquer token.

## Assinatura vs criptografia

- `HS256` — HMAC com segredo simétrico (mesma chave assina e verifica)
- `RS256` — par de chaves (privada assina, pública verifica)

Para API única, `HS256` com `JWT_SECRET` forte resolve.

## O ciclo completo

```text
1. POST /login { email, senha }
2. servidor: senha confere? → sign({ sub: id }) → devolve token
3. cliente: Authorization: Bearer token em toda request
4. middleware: verify(token, secret) → req.user = payload
5. expirou? → 401 — cliente faz login de novo (ou refresh token)
```

## Limitações

- Token válido **até expirar** — "deslogar" não o invalida (precisa blacklist se quiser)
- Payload legível — dados mínimos dentro
- Renovar exige novo sign — `exp` curto + refresh token é o padrão

## Resumo

- JWT = header + payload + assinatura, em Base64URL
- Assinatura garante integridade — não confidencialidade
- Stateless: o servidor verifica, não armazena
- `sub`/`exp` carregam quem e até quando; `Bearer` no header
