# BE01-40 — Express: Response (res)

## O que é

O objeto para **montar e enviar** a resposta — status, corpo, headers.

## Os métodos essenciais

```typescript
res.json({ id: 1 });                 // JSON + Content-Type automático
res.status(201).json({ id: 1 });     // status + corpo
res.send("texto");                   // string/buffer
res.status(204).send();              // sucesso sem corpo
```

## Status + corpo — o padrão

```typescript
// Sucesso
res.status(200).json(produto);        // GET/PATCH
res.status(201).json(produto);        // POST criou
res.status(204).send();               // DELETE ok

// Erro — formato padronizado
res.status(404).json({ message: "Produto não encontrado" });
res.status(400).json({ message: "Dados inválidos", errors });
```

## Regra de ouro: uma resposta por request

```typescript
// ❌ duas respostas → "Cannot set headers after they are sent"
res.json(a);
res.json(b);

// ✅ early return garante uma só
if (!produto) {
  return res.status(404).json({ message: "Não encontrado" });
}
res.json(produto);
```

`res.*` não encerra a função — sem `return`, o código continua e pode tentar responder de novo.

## Headers customizados

```typescript
res.set("X-Total-Count", "150");
res.set("Location", `/produtos/${id}`); // no 201
res.header("Cache-Control", "no-cache");
```

## Outros métodos úteis

```typescript
res.redirect("/nova-url");             // 302
res.redirect(301, "/movido");
res.download("/relatorio.pdf");
res.sendStatus(404);                   // status + mensagem padrão
res.type("application/pdf");
```

## Os erros padronizados

```typescript
interface ErroResponse {
  message: string;
  statusCode?: number;
  errors?: Record<string, string[]>;  // erros por campo (validação)
}
```

Consistência: o frontend sempre sabe onde ler o erro.

## Async handlers — cuidado

```typescript
// ❌ erro em async vaza sem tratamento (Express 4)
app.get("/x", async (req, res) => {
  const d = await fetchAlgo();  // se lançar → request pendurado
});

// ✅ try/catch ou middleware de erro (BE01-50)
app.get("/x", async (req, res, next) => {
  try {
    const d = await fetchAlgo();
    res.json(d);
  } catch (e) {
    next(e); // passa pro middleware de erro
  }
});
```

## Resumo

- `res.status(n).json(dados)` — o par da API
- **Uma resposta por request** — `return` nos early returns
- Erros num formato só: `{ message, statusCode }`
- Async precisa de try/catch + `next(e)` ou middleware de erro
