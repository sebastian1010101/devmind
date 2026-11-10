# BE02-81 — Jest: Meu Primeiro Teste Automatizado

## O mínimo

```ts
// soma.ts
export function soma(a: number, b: number) {
  return a + b;
}
```

```ts
// soma.test.ts
import { soma } from "./soma";

describe("soma", () => {
  it("soma dois números", () => {
    expect(soma(2, 3)).toBe(5);
  });
});
```

```bash
npx jest
# ✓ soma dois números
```

## describe / it / expect

| Peça | Papel |
| --- | --- |
| `describe("nome")` | Agrupa testes de uma unidade |
| `it("faz X")` / `test("faz X")` | Um caso de teste |
| `expect(valor)` | O resultado a verificar |
| `.toBe(x)` | O esperado |

```ts
describe("validador", () => {
  it("aceita email válido", () => { ... });
  it("rejeita email sem @", () => { ... });
  it("rejeita email vazio", () => { ... });
});
```

## Matchers — os essenciais

```ts
expect(x).toBe(5)                    // igualdade estrita (===)
expect(obj).toEqual({ id: 1 })       // igualdade profunda (objetos)
expect(x).toBeTruthy() / .toBeFalsy()
expect(x).toBeNull() / .toBeUndefined() / .toBeDefined()
expect(arr).toContain("item")        // array contém
expect(str).toMatch(/regex/)
expect(n).toBeGreaterThan(3)
expect(fn).toThrow("mensagem")       // função lança erro
```

`toBe` vs `toEqual`: primitivos `toBe`; objetos/arrays `toEqual` (comparação profunda).

## Async/await

```ts
it("cria usuário", async () => {
  const usuario = await service.criar(dados);   // await no teste
  expect(usuario.email).toBe("a@a.com");
});
```

```ts
// erro assíncrono
await expect(service.criar(dadosInvalidos)).rejects.toThrow("Email inválido");
```

`rejects` testa Promise que falha — sempre `await expect(...).rejects`.

## Testando erro síncrono

```ts
expect(() => fn()).toThrow();              // envolve em arrow
expect(() => fn()).toThrow("mensagem");
expect(() => fn()).toThrow(AppError);
```

## Um caso de borda por teste

```ts
describe("dividir", () => {
  it("divide normalmente", () => expect(dividir(6, 2)).toBe(3));
  it("lança erro ao dividir por zero", () => {
    expect(() => dividir(6, 0)).toThrow("divisão por zero");
  });
  it("retorna negativo com sinais opostos", () => {
    expect(dividir(-6, 2)).toBe(-3);
  });
});
```

## Saída que importa

```text
PASS  src/services/__tests__/soma.test.ts
  soma
    ✓ soma dois números (2 ms)
    ✓ rejeita strings
```

Verde = passou; o nome do `it` deve ler como frase: "soma dois números".

## Erros comuns

| Erro | Correção |
| --- | --- |
| `toBe` em objeto | Objetos são referências — `toEqual` |
| Promise não esperada | `await` o expect ou `rejects` |
| `toThrow` em chamada direta | `expect(() => fn())` — precisa da arrow |
| Teste que sempre passa | Confirme vendo falhar — mude o esperado |

## Resumo

- `describe` agrupa, `it` testa, `expect(...).toBe`/`toEqual` verifica
- Async: `await` + `rejects.toThrow` para erros de Promise
- Síncrono que lança: `expect(() => fn()).toThrow()`
- Um comportamento por `it`; nome que lê como frase
