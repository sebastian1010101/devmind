# BE01-13 — Tipo Any e Quando Utilizá-lo

## O que é

`any` **desliga a verificação de tipos** — a variável aceita e vira qualquer coisa:

```typescript
let qualquer: any = "texto";
qualquer = 42;
qualquer.metodoInexistente(); // compila! 💥 explode só em runtime
```

Todo o benefício do TS desaparece onde `any` toca — e ele é contagioso:

```typescript
const dados: any = JSON.parse(texto);
dados.usuario.nome;          // sem verificação
const x = dados.campo;       // x também é any — o veneno se espalha
```

## De onde o `any` vem

| Origem | Exemplo |
| --- | --- |
| Explícito | `let x: any` |
| `JSON.parse` | retorna `any` |
| `catch (e)` sem `useUnknownInCatchVariables` | `e` era any (hoje é `unknown` com strict) |
| Lib sem tipos | falta `@types/lib` |
| `noImplicitAny: false` | parâmetros sem anotação viram any |

## `any` vs `unknown` — a alternativa segura

```typescript
let valor: unknown = JSON.parse(texto);

valor.nome;          // ❌ TS obriga a verificar primeiro

if (typeof valor === "object" && valor !== null && "nome" in valor) {
  valor.nome;        // ✅ agora é seguro
}
```

`unknown` aceita qualquer coisa **mas exige narrowing antes de usar** — é o `any` com cinto de segurança.

## Quando `any` é aceitável

- Migração incremental de JS legado — funciona hoje, tipa depois
- Prototipagem rápida descartável
- Fronteiras de libs sem tipos (isole num wrapper tipado)
- `as any` pontual em testes para simular dados malformados

Mesmo aceitável, deixe o escape pequeno e explícito:

```typescript
// Melhor que any solto: normalize na entrada
const dadosBrutos: unknown = JSON.parse(texto);
const usuario = dadosBrutos as Usuario; // afirmação pontual e visível
```

## Sinais de alerta

| Cheiro | Problema |
| --- | --- |
| `: any[]` em arrays de resposta | Tipifique com a interface real |
| `as any` pra "fazer passar" | Esconde bug real — resolva a causa |
| Função que retorna `any` | Anote o retorno correto |
| `catch (e: any)` | `catch (e)` já é `unknown` com strict — faça narrowing |

## Regra de ouro

```text
Dado externo chega como unknown → valida (Zod/narrowing) → vira tipo interno confiável
```

## Resumo

- `any` desliga o TS — evita como padrão
- `unknown` + narrowing = a alternativa type-safe
- Aceitável em migração e bordas de libs — isolado e explícito
- Valide dados externos; nunca confie cegamente em `as`
