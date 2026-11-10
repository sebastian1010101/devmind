# BE01-27 — Omit, Pick e Partial

## Os utilitários de derivação

```typescript
interface Usuario {
  id: number;
  nome: string;
  email: string;
  senha: string;
  criadoEm: Date;
}
```

## `Partial<T>` — tudo opcional

```typescript
type AtualizarUsuarioDTO = Partial<Usuario>;
// { id?, nome?, email?, senha?, criadoEm? }
```

Perfeito para **PATCH/update** — o cliente manda só o que muda:

```typescript
function atualizar(id: number, dados: Partial<Usuario>) {
  const usuario = buscar(id);
  Object.assign(usuario, dados);
}
```

## `Omit<T, K>` — remove campos

```typescript
type CriarUsuarioDTO = Omit<Usuario, "id" | "criadoEm">;
// { nome, email, senha } — id e data o servidor gera

type UsuarioPublico = Omit<Usuario, "senha">;
// nunca vaza senha na resposta da API
```

## `Pick<T, K>` — escolhe campos

```typescript
type LoginDTO = Pick<Usuario, "email" | "senha">;
// { email, senha }

type UsuarioResumo = Pick<Usuario, "id" | "nome">;
```

`Pick` lista o que **fica**; `Omit` lista o que **sai**.

## O fluxo completo de uma API

```typescript
interface Usuario { id: number; nome: string; email: string; senha: string; criadoEm: Date; }

// Entrada POST — sem id/criadoEm (servidor gera)
type CriarDTO = Omit<Usuario, "id" | "criadoEm">;

// Entrada PATCH — tudo opcional, menos id
type AtualizarDTO = Partial<Omit<Usuario, "id" | "criadoEm">>;

// Saída — sem senha
type UsuarioResponse = Omit<Usuario, "senha">;
```

Um modelo, três contratos — **zero repetição**, tudo derivado.

## Outros utilitários úteis

```typescript
type ReadonlyUsuario = Readonly<Usuario>;          // tudo readonly
type Required<T> = /* torna opcionais obrigatórios */;
type Dict = Record<string, number>;                // { [k]: number }
type Retorno = ReturnType<typeof minhaFuncao>;     // extrai o retorno
type Params = Parameters<typeof minhaFuncao>;      // extrai os parâmetros
```

## Exercício mental — por que derivar

```typescript
// ❌ repetir os campos — mudou Usuario, tem que mudar aqui
interface CriarUsuarioDTO {
  nome: string;
  email: string;
  senha: string;
}

// ✅ derivar — mudou Usuario, DTO acompanha sozinho
type CriarUsuarioDTO = Omit<Usuario, "id" | "criadoEm">;
```

Fonte única de verdade — o modelo muda, os contratos seguem.

## Resumo

- `Partial` → update; `Omit` → remove; `Pick` → seleciona
- DTOs derivados da entidade — sem copiar campos
- Composição `Partial<Omit<...>>` para PATCH sem id
- `Record`, `Readonly`, `ReturnType` completam a caixa de ferramentas
