# BE01-07 — Biblioteca ts-node-dev

## O problema que resolve

O fluxo manual de TS no backend é lento:

```text
edita arquivo.ts → tsc compila → node roda → edita → repete tudo
```

O **ts-node-dev** automatiza: roda `.ts` direto e **reinicia a cada save** — o equivalente backend do hot reload do Vite.

## Instalação

```bash
npm install --save-dev ts-node-dev
```

## Script no package.json

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/index.ts"
  }
}
```

```bash
npm run dev
```

## As flags

| Flag | Efeito |
| --- | --- |
| `--respawn` | Reinicia o processo inteiro a cada mudança (default é só reavaliação) |
| `--transpile-only` | Pula a verificação de tipos — compilação **muito** mais rápida |
| `--watch` | Observa pastas extras além dos imports |
| `--rs` | Permite reiniciar digitando `rs` + Enter no terminal |

> Com `--transpile-only`, erros de tipo não bloqueiam a execução — mas o editor ainda os mostra em vermelho. A verificação completa roda no `tsc` do build.

## Alternativas

| Ferramenta | Diferença |
| --- | --- |
| `ts-node` | Roda `.ts`, mas sem watch/restart |
| `node --watch` + `tsx` | Nativo do Node 20+; tsx usa esbuild — ainda mais rápido |
| `nodemon` | Watch genérico — precisa de config para `.ts` |

```json
// Alternativa moderna
"dev": "tsx watch src/index.ts"
```

## Fluxo de trabalho

```text
npm run dev
    │
    ├── lê src/index.ts
    ├── compila em memória (sem gerar dist/)
    ├── executa com node
    └── observa mudanças → reinicia automaticamente
```

Em produção: `tsc` gera o `dist/` e `node` roda o JS — ts-node-dev é só desenvolvimento.

## Resumo

- ts-node-dev = ts-node + watch + restart — hot reload pra backend
- `--respawn --transpile-only` = reinício real + compilação rápida
- Só em desenvolvimento; produção usa `tsc` + `node dist/`
- `tsx watch` é a alternativa moderna mais rápida
