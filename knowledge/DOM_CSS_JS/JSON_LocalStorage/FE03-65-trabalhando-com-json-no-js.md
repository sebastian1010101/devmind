# FE03-65 — Trabalhando com JSON no JS

## Os dois métodos centrais

O JavaScript oferece um objeto global `JSON` com dois métodos que cobrem toda a conversão:

| Método | Direção | Retorna |
| --- | --- | --- |
| `JSON.stringify()` | Objeto JS → **string JSON** | `string` |
| `JSON.parse()` | String JSON → **objeto JS** | valor/objeto |

```javascript
const usuario = { nome: "Ana", idade: 28 };

const texto = JSON.stringify(usuario);
// '{"nome":"Ana","idade":28}' — virou string

const objeto = JSON.parse(texto);
// { nome: "Ana", idade: 28 } — voltou a ser objeto
```

## JSON.stringify — serializando

### Uso básico

```javascript
JSON.stringify({ a: 1 });        // '{"a":1}'
JSON.stringify([1, 2, 3]);       // '[1,2,3]'
JSON.stringify("texto");         // '"texto"'
JSON.stringify(42);              // '42'
JSON.stringify(true);            // 'true'
JSON.stringify(null);            // 'null'
```

### Formatando a saída (indentação)

O terceiro parâmetro controla o espaçamento — essencial para depuração:

```javascript
const obj = { nome: "Ana", tags: ["dev", "js"] };

JSON.stringify(obj, null, 2);
```

```json
{
  "nome": "Ana",
  "tags": [
    "dev",
    "js"
  ]
}
```

### O que é perdido na serialização

`JSON.stringify` **descarta silenciosamente** o que JSON não suporta:

```javascript
const obj = {
  nome: "Ana",
  fn: () => {},           // função → removida
  undef: undefined,       // → removida
  data: new Date(),       // → vira string ISO "2024-01-15T..."
  regex: /abc/,           // → vira {}
  simbolo: Symbol("x")    // → removida
};

JSON.stringify(obj);
// '{"nome":"Ana","data":"2024-01-15T00:00:00.000Z","regex":{}}'
```

### Filtrando com o parâmetro replacer

```javascript
// Array de chaves permitidas
JSON.stringify(usuario, ["nome", "idade"]);

// Função replacer — decide o que incluir
JSON.stringify(usuario, (chave, valor) =>
  chave === "senha" ? undefined : valor
);
```

## JSON.parse — desserializando

### Parse básico

```javascript
JSON.parse('{"nome":"Ana"}');  // { nome: "Ana" }
JSON.parse('[1,2,3]');          // [1, 2, 3]
JSON.parse('"texto"');          // "texto"
JSON.parse('42');               // 42
JSON.parse('true');             // true
```

### O que explode

`JSON.parse` é **estrito** — qualquer desvio lança `SyntaxError`:

```javascript
JSON.parse('{nome:"Ana"}');    // ❌ SyntaxError — chave sem aspas
JSON.parse("{'a':1}");          // ❌ SyntaxError — aspas simples
JSON.parse('{a:1,}');           // ❌ SyntaxError — vírgula final
JSON.parse('undefined');        // ❌ SyntaxError — não é JSON
JSON.parse('{"a":1');           // ❌ SyntaxError — JSON truncado
JSON.parse('{"a":1}');          // ✅ OK
```

### Protegendo o parse com try/catch

Sempre que a origem do texto não é 100% controlada (input do usuário, localStorage corrompido, resposta de API), envolva o parse:

```javascript
function parseSeguro(texto, fallback = null) {
  try {
    return JSON.parse(texto);
  } catch {
    return fallback;
  }
}

parseSeguro('{"a":1}');   // { a: 1 }
parseSeguro('lixo');       // null
parseSeguro('', {});       // {} — fallback customizado
```

## O par de operações na prática

### Salvando e recuperando (padrão localStorage)

```javascript
const carrinho = [
  { id: 1, qtd: 2 },
  { id: 3, qtd: 1 }
];

// Salvar — objeto vira texto
localStorage.setItem("carrinho", JSON.stringify(carrinho));

// Recuperar — texto volta a ser objeto
const salvo = JSON.parse(localStorage.getItem("carrinho") || "[]");
console.log(salvo[0].qtd); // 2
```

### Comunicação com API

```javascript
// Enviando — stringify no corpo
fetch("/api/usuarios", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nome: "Ana" })
});

// Recebendo — response.json() já faz o parse
const resposta = await fetch("/api/usuarios/1");
const dados = await resposta.json(); // objeto JS pronto
```

## O clone profundo via JSON

Antes do `structuredClone`, o truque padrão de cópia profunda era serializar e re-parsear:

```javascript
const original = { a: { b: 1 } };
const copia = JSON.parse(JSON.stringify(original));

copia.a.b = 99;
console.log(original.a.b); // 1 — cópia real
```

Limitações: perde funções, `Date` vira string, quebra em referências circulares. Prefira `structuredClone(obj)` quando disponível.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `localStorage.setItem("x", obj)` sem stringify | Salva `"[object Object]"` — sempre serialize |
| `JSON.parse` em valor já objeto | `parse` espera string — verifique o tipo antes |
| Parse sem try/catch | JSON malformado quebra o script — sempre proteja |
| Esperar `Date` de volta do parse | `parse` retorna string — reconstrua com `new Date()` |
