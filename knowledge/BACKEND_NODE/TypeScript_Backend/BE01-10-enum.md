# BE01-10 — Enum

## O que é

Um **conjunto nomeado de constantes** — substitui "magic strings" e números soltos:

```typescript
enum Status {
  Pendente,
  EmAndamento,
  Concluido,
}

let tarefa: Status = Status.Pendente;
```

## Enum numérico (padrão)

```typescript
enum Status {
  Pendente,      // 0
  EmAndamento,   // 1
  Concluido,     // 2
}

Status.Concluido;   // 2
Status[0];          // "Pendente" — mapeamento reverso
```

## Enum de strings (mais útil em APIs)

```typescript
enum Status {
  Pendente = "PENDENTE",
  EmAndamento = "EM_ANDAMENTO",
  Concluido = "CONCLUIDO",
}

// No JSON da API fica legível:
// { "status": "EM_ANDAMENTO" }
```

String enums são o padrão em backend — o valor que viaja na API é autoexplicativo.

## Exemplo prático — status de pedido

```typescript
enum StatusPedido {
  Criado = "CRIADO",
  Pago = "PAGO",
  Enviado = "ENVIADO",
  Entregue = "ENTREGUE",
  Cancelado = "CANCELADO",
}

function podeSerCancelado(status: StatusPedido): boolean {
  return status === StatusPedido.Criado || status === StatusPedido.Pago;
}
```

## Enum vs union de literais

```typescript
// Enum
enum Role { Admin = "ADMIN", User = "USER" }

// Union literal — mais leve, mesma segurança
type Role = "ADMIN" | "USER";
```

| Enum | Union literal |
| --- | --- |
| Existe em runtime (gera objeto JS) | Só existe no compile-time |
| `Status.Pago` referencia membro | `"PAGO"` direto |
| Namespace organizado | Mais simples e idiomático |

Muitos projetos modernos preferem union literal + `as const`:

```typescript
const STATUS = { Pendente: "PENDENTE", Pago: "PAGO" } as const;
type Status = (typeof STATUS)[keyof typeof STATUS]; // "PENDENTE" | "PAGO"
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `status === "PAGO"` com enum numérico | Use string enum ou compare com o membro |
| Receber string da API direto no enum | Valide antes — `Object.values(Status).includes(v)` |
| Enum para 2 valores | `boolean` ou union resolve |

## Resumo

- Enum = conjunto nomeado de constantes — mata magic strings
- Prefira **string enums** em backend — legível no JSON
- Union literal é a alternativa leve e idiomática
- Valide strings vindas da API antes de tratar como enum
