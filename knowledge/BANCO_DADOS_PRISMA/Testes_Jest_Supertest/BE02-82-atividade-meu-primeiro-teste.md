# BE02-82 — Atividade: Meu Primeiro Teste

## Objetivo

Escrever a primeira suite real: uma função de negócio com casos felizes e de erro — `describe`/`it`/`expect`, matchers certos e assíncrono.

## A função sob teste

```ts
// src/services/cadastro.ts
export function validarCadastro(dados: { nome: string; email: string; senha: string }) {
  if (!dados.nome?.trim()) throw new Error("Nome obrigatório");
  if (!dados.email?.includes("@")) throw new Error("Email inválido");
  if (dados.senha?.length < 8) throw new Error("Senha mínima: 8");
  return true;
}

export function formatarEmail(email: string) {
  return email.trim().toLowerCase();
}
```

## A suite

```ts
// __tests__/cadastro.test.ts
import { validarCadastro, formatarEmail } from "../src/services/cadastro";

describe("validarCadastro", () => {
  const valido = { nome: "Ana", email: "ana@mail.com", senha: "12345678" };

  it("aceita dados válidos", () => {
    expect(validarCadastro(valido)).toBe(true);
  });

  it("rejeita nome vazio", () => {
    expect(() => validarCadastro({ ...valido, nome: "" }))
      .toThrow("Nome obrigatório");
  });

  it("rejeita email sem @", () => {
    expect(() => validarCadastro({ ...valido, email: "ana" }))
      .toThrow("Email inválido");
  });

  it("rejeita senha curta", () => {
    expect(() => validarCadastro({ ...valido, senha: "123" }))
      .toThrow("Senha mínima: 8");
  });
});

describe("formatarEmail", () => {
  it("remove espaços e baixa case", () => {
    expect(formatarEmail("  Ana@Mail.COM ")).toBe("ana@mail.com");
  });
});
```

## Rodando

```bash
npm test -- cadastro
```

```text
PASS  __tests__/cadastro.test.ts
  validarCadastro
    ✓ aceita dados válidos
    ✓ rejeita nome vazio
    ✓ rejeita email sem @
    ✓ rejeita senha curta
  formatarEmail
    ✓ remove espaços e baixa case
```

## Casos de borda a adicionar

```ts
it("rejeita email undefined", () => {
  expect(() => validarCadastro({ nome: "A", senha: "12345678" } as any))
    .toThrow();
});

it("rejeita nome só com espaços", () => {
  expect(() => validarCadastro({ ...valido, nome: "   " }))
    .toThrow("Nome obrigatório");
});
```

Pense: o que **deveria** falhar mas passa? Undefined, espaços em branco, extremos.

## Critérios de conclusão

1. Suite verde — todos os `it` passando
1. Pelo menos um teste de erro com `toThrow`
1. Objeto base válido reaproveitado (`{ ...valido }`)
1. Borda real testada (vazio, undefined, whitespace)

## Resumo

- `{ ...baseValida, campo: invalido }` isola o que está sendo testado
- `toThrow` envolve em arrow; `rejects` em async
- Bordas são onde o teste vale — vazio, null, limite
