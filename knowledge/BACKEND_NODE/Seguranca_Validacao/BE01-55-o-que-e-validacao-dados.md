# BE01-55 — O que é Validação de Dados

## O princípio: nunca confie no cliente

O `req.body` é **terra de ninguém** — qualquer um pode mandar qualquer coisa:

```typescript
// Cliente manda:
POST /produtos
{ "nome": 123, "preco": "de graça", "extra": "<script>alert(1)</script>" }

// Sem validação, isso entra direto no banco 💥
```

TypeScript **não valida em runtime** — a interface existe só em compile-time. `req.body` é `any`.

## O que validar

| Aspecto | Exemplo |
| --- | --- |
| **Presença** | `nome` é obrigatório? |
| **Tipo** | `preco` é número? `ativo` é boolean? |
| **Formato** | email válido? CEP com 8 dígitos? |
| **Faixa** | `preco > 0`? `idade` entre 0-150? |
| **Comprimento** | senha mín. 8? nome máx. 100? |
| **Campos extras** | rejeitar o que não é esperado |

## Onde validar

```text
Request → [Validação] → Controller → Service → Database
              ↑
         NA BORDA — antes de tudo
```

Validar na entrada (middleware) é mais barato que:

- No controller — já entrou sujo
- No service — a regra mistura com validação
- No banco — constraint estoura como erro 500 feio

## Validação manual vs biblioteca

```typescript
// Manual — funciona, mas cresce feio
if (typeof nome !== "string" || nome.length < 3) { /* ... */ }
if (typeof preco !== "number" || preco <= 0) { /* ... */ }

// Com Zod — declarativo, tipado, reutilizável
const schema = z.object({
  nome: z.string().min(3),
  preco: z.number().positive(),
});
schema.parse(req.body); // lança erro se inválido
```

## Validação vs sanitização

- **Validação** — aceita ou rejeita: "preço deve ser número positivo"
- **Sanitização** — limpa o que entra: `trim()`, remover tags HTML, normalizar case

Validação decide se aceita; sanitização arruma o aceito.

## A resposta de erro

```json
// 400 com detalhes por campo — o padrão
{
  "message": "Dados inválidos",
  "errors": {
    "preco": ["Deve ser positivo"],
    "email": ["Formato inválido"]
  }
}
```

## Resumo

- `req.body` não é confiável — TS não valida runtime, Zod valida
- Valide na borda: middleware antes do controller
- Presença, tipo, formato, faixa, campos extras
- Erro padronizado: `400` + `{ errors: { campo: [msgs] } }`
