# BE01-08 — Atividade: Olá Kenzinhos

Primeiro programa TypeScript rodando no Node — valida todo o setup.

## Objetivo

Criar um projeto TS do zero, compilar e executar uma saudação.

## Passo a passo

```bash
mkdir ola-kenzinhos && cd ola-kenzinhos
npm init -y
npm install -D typescript @types/node ts-node-dev
npx tsc --init
```

Ajuste o `tsconfig.json` — `rootDir: ./src`, `outDir: ./dist`, `strict: true`.

`src/index.ts`:

```typescript
function saudacao(nome: string): string {
  return `Olá, ${nome}! Bem-vindo(a) ao backend com TypeScript.`;
}

const kenzinhos: string[] = ["Ana", "Bruno", "Carla"];

kenzinhos.forEach((nome) => {
  console.log(saudacao(nome));
});
```

## Executando

```bash
# Desenvolvimento (sem compilar pra disco)
npm run dev
# → Olá, Ana! Bem-vindo(a) ao backend com TypeScript.
# → Olá, Bruno! ...
# → Olá, Carla! ...

# Ou compilando
npm run build     # tsc → dist/index.js
npm start         # node dist/index.js
```

## Erros propositais para testar

```typescript
saudacao(42);              // ❌ number não é string
const lista: string[] = [1, 2];  // ❌ number não é string
```

O `ts-node-dev` com `--transpile-only` roda mesmo assim — mas o editor acusa o erro. Sem a flag, ele bloqueia.

## Checklist

- [ ] `npm init -y` + dependências instaladas
- [ ] `tsconfig.json` com `strict`, `rootDir`, `outDir`
- [ ] `src/index.ts` roda com `npm run dev`
- [ ] `npm run build` gera `dist/index.js`
- [ ] Erro de tipo aparece no editor ao passar tipo errado

## Resumo

- Setup validado: init → tsconfig → src → dev/build/start
- ts-node-dev executa TS sem gerar arquivos
- Erros de tipo aparecem antes da execução
