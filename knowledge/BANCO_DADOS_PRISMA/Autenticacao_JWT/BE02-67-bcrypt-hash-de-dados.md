# BE02-67 — Bcrypt: Hash de Dados

## Por que hash, não criptografia

```text
criptografia:  texto → cifrado → (com chave) → texto    reversível
hash:          texto → hash                          irreversível
```

Senha se **hasheia**, não se criptografa. Se o banco vazar:

- Criptografado + chave vazada = senhas expostas
- Hash bcrypt = mesmo com o banco, o atacante quebra por força bruta cara

## Setup

```bash
npm install bcrypt
npm install -D @types/bcrypt
```

## hash — gravando

```ts
import bcrypt from "bcrypt";

const hash = await bcrypt.hash(senha, 10);
// $2b$10$N9qo8uLOickgx2ZMRZoMye...   ← 60 chars
```

```ts
// no registro
const usuario = await prisma.usuario.create({
  data: { nome, email, senha: await bcrypt.hash(senha, 10) },
});
```

O `10` é o **custo** (rounds de salt) — quanto maior, mais lento de calcular (seguro) e de quebrar. `10`–`12` é o padrão atual.

## compare — conferindo

```ts
const ok = await bcrypt.compare(senhaDigitada, usuario.senha);
if (!ok) throw new AppError("Credenciais inválidas", 401);
```

O hash embute o salt — `compare` extrai e refaz a conta. Nunca `bcrypt.hash(senha) === hash` — o salt muda a cada hash.

```ts
await bcrypt.hash("123", 10)   // $2b$10$abc...
await bcrypt.hash("123", 10)   // $2b$10$xyz...  ← diferente!
await bcrypt.compare("123", hash1)  // true — mesmo assim confere
```

## O que o hash contém

```text
$2b$10$N9qo8uLOickgx2ZMRZoMye...
│   │  │
│   │  └─ salt (22 chars) + hash (31 chars)
│   └───── custo (2^10 rounds)
└───────── versão do algoritmo
```

Tudo embutido — `compare` só precisa do hash.

## Alternativas modernas

| Algoritmo | Status |
| --- | --- |
| **bcrypt** | Padrão maduro — o da aula |
| **argon2** | Recomendação atual OWASP — mais resistente a GPU |
| **scrypt** | Nativo no Node (`crypto.scrypt`) |
| MD5/SHA1 puro | **Nunca** — rápido demais, quebra fácil |

## Regras de ouro

- Senha **nunca** vai pro log, pro JWT, pro response
- `select` no Prisma para não devolver `senha`/hash
- Custo alto o bastante para ser lento (~100ms é bom)
- Força bruta no login: rate-limit + tentativas limitadas

## Erros comuns

| Erro | Correção |
| --- | --- |
| `bcrypt.hash` a cada login | Hash só no registro/troca — login usa `compare` |
| `senha === hash` | Sempre `bcrypt.compare` |
| Hash no response | `select` whitelist — omita `senha` |
| Custo muito baixo | `10` é o mínimo sensato; `12` comum |
| Retornar o hash ao cliente | Nunca — nem "para conferir" |

## Resumo

- `bcrypt.hash(senha, 10)` no registro — unidirecional, salt embutido
- `bcrypt.compare(digitada, hash)` no login — nunca compare strings
- Mesmo input dá hash diferente (salt) — `compare` resolve
- Hash nunca sai do servidor — `select` o omite
