# BE01-57 — Atividade: Validação de Dados com Zod

Exercício: schemas reais para uma API — validar e sentir o `safeParse`.

## Schema de produto

```typescript
import { z } from "zod";

const produtoSchema = z.object({
  nome: z.string().min(3, "Nome deve ter ao menos 3 caracteres"),
  preco: z.number().positive("Preço deve ser positivo"),
  categoria: z.enum(["ELETRONICOS", "ALIMENTOS", "VESTUARIO"]),
  estoque: z.number().int().nonnegative().default(0),
  descricao: z.string().max(500).optional(),
});

type Produto = z.infer<typeof produtoSchema>;
```

## Testando

```typescript
// Válido
produtoSchema.parse({
  nome: "Mouse Gamer",
  preco: 129.9,
  categoria: "ELETRONICOS",
});
// ✅ retorna { nome, preco, categoria, estoque: 0 } — default aplicado

// Inválido
const r = produtoSchema.safeParse({
  nome: "Mo",               // curto
  preco: -5,                // negativo
  categoria: "INVALIDA",    // fora do enum
});

if (!r.success) {
  console.log(r.error.flatten().fieldErrors);
  // {
  //   nome: ["Nome deve ter ao menos 3 caracteres"],
  //   preco: ["Preço deve ser positivo"],
  //   categoria: ["Invalid enum value..."]
  // }
}
```

## Schema de cadastro de usuário

```typescript
const cadastroSchema = z
  .object({
    nome: z.string().min(3),
    email: z.string().email("Email inválido"),
    senha: z
      .string()
      .min(8, "Senha mínima: 8 caracteres")
      .regex(/[A-Z]/, "Precisa de maiúscula")
      .regex(/[0-9]/, "Precisa de número"),
    confirmarSenha: z.string(),
  })
  .refine((d) => d.senha === d.confirmarSenha, {
    message: "Senhas não conferem",
    path: ["confirmarSenha"],
  });
```

`.refine()` — validação cruzada entre campos; `path` aponta onde o erro aparece.

## Usando na rota (versão simples)

```typescript
app.post("/produtos", (req, res) => {
  const resultado = produtoSchema.safeParse(req.body);

  if (!resultado.success) {
    return res.status(400).json({
      message: "Dados inválidos",
      errors: resultado.error.flatten().fieldErrors,
    });
  }

  const produto = service.criar(resultado.data); // tipado!
  res.status(201).json(produto);
});
```

(BE01-58 transforma isso em middleware reutilizável.)

## Checklist

- [ ] `.parse` vs `.safeParse` entendidos
- [ ] `flatten().fieldErrors` = formato de erro pra API
- [ ] Mensagens customizadas por regra
- [ ] `.refine` para regras entre campos
- [ ] `z.infer` gera o tipo — DTO e validação de uma fonte

## Desafios

1. Schema de endereço aninhado dentro do cadastro
2. `z.coerce.number()` para query params que chegam string
3. Schema de login = `cadastroSchema.pick({ email: true, senha: true })`

## Resumo

- `safeParse` + `flatten().fieldErrors` = resposta 400 completa
- `.refine` valida relações entre campos (senha === confirmação)
- `resultado.data` sai tipado — o service recebe dados garantidos
