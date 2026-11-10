# BE01-04 — O que é TypeScript e suas Vantagens

## O que é

JavaScript **com tipos estáticos** — superset que compila pra JS puro:

```typescript
function soma(a: number, b: number): number {
  return a + b;
}

soma(2, 3);      // ✅ 5
soma("2", 3);    // ❌ Erro no editor — string não é number
```

O erro aparece **antes** de rodar — no editor ou na compilação.

## Por que no backend

| Sem tipos | Com TS |
| --- | --- |
| `req.body.nome` é o quê? string? number? | Interface define o contrato |
| Erro descoberto em produção | Erro descoberto no editor |
| Refatorar = medo | Renomear tipo → TS aponta tudo que quebra |
| Ler o código pra entender a API | Tipos documentam a API |

Backend lida com **dados externos não confiáveis** (requests de qualquer cliente) — tipos criam contratos explícitos entre camadas.

## Vantagens

- **Detecção precoce** — `undefined`/`null`, typos de propriedade, argumentos errados
- **IntelliSense** — autocomplete sabe exatamente o que existe no objeto
- **Refatoração segura** — mudou a interface? O compilador lista todos os pontos afetados
- **Documentação viva** — `interface Usuario` diz mais que um comentário desatualizado
- **Onboarding** — código novo se explica pelos tipos

## O custo

- Configuração extra (`tsconfig.json`, compilação)
- Curva de aprendizado (generics, narrowing...)
- Tipos só existem em desenvolvimento — **não validam dados em runtime** (para isso existe Zod, visto em BE01-56)

## TS no backend vs frontend

```text
Frontend: TS tipa props, estados, eventos, respostas de API
Backend:  TS tipa req/res, services, models, erros, entidades
```

Mesmo conhecimento, alvos diferentes — quem fez TS no React (FE05) já sabe 80%.

## Resumo

- TS = JS + verificação de tipos em tempo de desenvolvimento
- Contratos explícitos entre request → service → database
- Tipos não validam runtime — para isso há Zod
- Custo: config + aprendizado. Retorno: menos bugs em produção
