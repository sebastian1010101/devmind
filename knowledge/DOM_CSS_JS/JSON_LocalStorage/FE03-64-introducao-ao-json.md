# FE03-64 — Introdução ao JSON

## O que é

**JSON** (JavaScript Object Notation) é o formato padrão de troca de dados da web — um texto estruturado que representa objetos, arrays e valores primitivos. Praticamente toda API, arquivo de configuração e persistência local usa JSON.

```json
{
  "nome": "Ana",
  "idade": 28,
  "ativo": true,
  "tags": ["dev", "front-end"]
}
```

## Por que o JSON dominou

- **Legível por humanos** — texto puro, fácil de ler e depurar
- **Independente de linguagem** — Python, Java, Go, PHP, todos falam JSON
- **Nativo ao JavaScript** — a sintaxe veio do JS (mas não é JS!)
- **Leve** — menos verboso que XML, o formato que substituiu

## JSON vs objeto JavaScript

Parecem iguais, mas não são. JSON é **texto** (uma string) — objeto JS é **estrutura na memória**:

| Característica | Objeto JavaScript | JSON |
| --- | --- | --- |
| Chaves | Sem aspas ou com aspas | **Sempre** aspas duplas |
| Strings | `'a'`, `"a"`, `` `a` `` | Só `"a"` (aspas duplas) |
| Funções | Permitidas | Proibidas |
| `undefined` | Válido | Não existe |
| Comentários | Permitidos | Proibidos |
| Vírgula final | Permitida | Proibida |
| Natureza | Objeto em memória | String de texto |

```javascript
// Objeto JavaScript — válido em JS, inválido como JSON
const obj = {
  nome: 'Ana',        // aspas simples + chave sem aspas
  saudar() { },       // função não existe em JSON
  extra: undefined,   // undefined não existe em JSON
};
```

```json
{
  "nome": "Ana"
}
```

## Tipos de dados permitidos

JSON suporta exatamente 6 tipos + 1 estrutura raiz:

```json
{
  "string": "texto com aspas duplas",
  "numero": 42,
  "decimal": 3.14,
  "booleano": true,
  "nulo": null,
  "array": [1, 2, 3],
  "objeto": { "aninhado": "sim" }
}
```

**Não existem em JSON**: `undefined`, funções, `Date`, `Map`, `Set`, `Symbol`, comentários.

## Anatomia de um documento JSON

Um documento JSON válido é **um** valor raiz — geralmente objeto ou array:

```json
[
  { "id": 1, "nome": "Ana" },
  { "id": 2, "nome": "Beto" }
]
```

```json
{ "total": 2, "resultados": [{ "id": 1 }, { "id": 2 }] }
```

## Onde o JSON aparece

### APIs REST

A resposta padrão de praticamente qualquer API:

```json
{
  "usuario": {
    "id": 42,
    "login": "anasilva",
    "repositorios": 15
  }
}
```

### Arquivos de configuração

```json
// package.json
{
  "name": "meu-projeto",
  "version": "1.0.0",
  "scripts": { "dev": "vite" }
}
```

### Persistência local

LocalStorage só guarda strings — JSON é a ponte entre objetos JS e texto persistido (tema do FE03-67+).

## Erros comuns de sintaxe

```json
// ❌ Aspas simples
{ 'nome': 'Ana' }

// ❌ Chave sem aspas
{ nome: "Ana" }

// ❌ Vírgula final (trailing comma)
{ "a": 1, "b": 2, }

// ❌ Comentário
{ "nome": "Ana" } // isso quebra o parse

// ✅ Correto
{ "nome": "Ana" }
```

Qualquer um desses gera `SyntaxError` ao fazer parse — JSON é **rígido** por design: a simplicidade da gramática é o que o torna universal.
