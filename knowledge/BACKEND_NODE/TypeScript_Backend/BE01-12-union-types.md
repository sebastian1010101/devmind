# BE01-12 — Union Types

## O que é

Uma variável que pode ser **um tipo OU outro**:

```typescript
let id: number | string;

id = 42;     // ✅
id = "abc";  // ✅
id = true;   // ❌
```

## Union de literais — o uso mais comum

```typescript
type Status = "PENDENTE" | "PAGO" | "CANCELADO";
type Metodo = "GET" | "POST" | "PUT" | "DELETE";

function mudarStatus(novo: Status) { /* ... */ }

mudarStatus("PAGO");      // ✅
mudarStatus("QUALQUER");  // ❌
```

É a alternativa leve ao enum — mesma segurança, sem objeto em runtime.

## Narrowing — o TS refina pelo contexto

O problema: dentro da union, só métodos comuns a todos os tipos funcionam:

```typescript
function formatar(id: number | string) {
  id.toUpperCase(); // ❌ number não tem toUpperCase
}
```

A solução: **narrowing** — o TS afunila o tipo com checagens:

```typescript
function formatar(id: number | string) {
  if (typeof id === "string") {
    return id.toUpperCase(); // ✅ aqui é string
  }
  return id.toFixed(2);      // ✅ aqui é number
}
```

## Formas de narrowing

```typescript
// typeof — primitivos
if (typeof x === "string") { /* ... */ }

// instanceof — classes
if (erro instanceof AppError) { /* ... */ }

// in — propriedade existe
if ("email" in dados) { /* ... */ }

// truthiness — remove null/undefined
if (usuario) { /* aqui não é null nem undefined */ }
```

## Discriminated unions — o padrão para objetos

Uma propriedade literal ("discriminante") distingue as variantes:

```typescript
type Sucesso = { ok: true; dados: Usuario };
type Falha   = { ok: false; erro: string };
type Resultado = Sucesso | Falha;

function tratar(r: Resultado) {
  if (r.ok) {
    r.dados; // ✅ TS sabe que é Sucesso
  } else {
    r.erro;  // ✅ TS sabe que é Falha
  }
}
```

Padrão perfeito para respostas de API e reducers — impossível acessar `dados` num erro.

## Union em parâmetros flexíveis

```typescript
function log(msg: string | string[]) {
  const texto = Array.isArray(msg) ? msg.join(" ") : msg;
  console.log(texto);
}
```

## Resumo

- `A | B` = um ou outro; literais (`"A" | "B"`) substituem enums leves
- Narrowing: `typeof`, `instanceof`, `in`, truthiness, discriminante
- Discriminated union (`{ ok: true } | { ok: false }`) — o padrão pra resultados
- O TS só libera métodos seguros até você estreitar o tipo
