# BE02-61 — Dotenv CLI

## O que é

O `dotenv` carrega `.env` **dentro do código**. O **dotenv-cli** carrega **pelo comando** — útil para scripts que não importam `dotenv`:

```bash
npm install -D dotenv-cli
```

## O problema que resolve

```bash
# prisma CLI lê .env automaticamente — mas .env.test? Não.
npx prisma migrate deploy   # usa .env — sempre

# E se o comando não carrega env nenhum?
node scripts/seed.js        # process.env vazio
```

## Usando

```bash
# Carrega .env antes de executar o comando
npx dotenv -- node scripts/seed.js

# Carrega um arquivo específico
npx dotenv -e .env.test -- jest
npx dotenv -e .env.production -- npm start
```

## Nos scripts do package.json

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "test": "dotenv -e .env.test -- jest",
    "migrate:test": "dotenv -e .env.test -- prisma migrate deploy",
    "seed": "dotenv -- node dist/seed.js"
  }
}
```

## Múltiplos arquivos env

```text
.env            → desenvolvimento (default)
.env.test       → banco de teste (DATABASE_URL → app_test)
.env.production → produção (referência — prod usa vars do Render)
```

```bash
dotenv -e .env.test -- jest --runInBand
```

O `-e` aponta o arquivo — cada ambiente com sua `DATABASE_URL`.

## O caso clássico — testes com banco separado

```bash
# Sem dotenv-cli, o jest lê .env — banco de DEV 😱
# Com dotenv-cli:
dotenv -e .env.test -- jest
# Agora DATABASE_URL aponta pra app_test — deleteMany é seguro
```

## `.env` padrão vs `-e`

```bash
dotenv -- comando           # carrega .env
dotenv -e .env.test -- cmd  # carrega .env.test
dotenv -e .env -e .env.local -- cmd  # múltiplos — último prevalece
```

## Resumo

- `dotenv-cli` = carrega env pelo comando, não pelo código
- `dotenv -e .env.test -- jest` = testes no banco certo
- Scripts: `test`, `migrate:test`, `seed` cada um com seu env
- Múltiplos `-e` se acumulam — o último sobrescreve
