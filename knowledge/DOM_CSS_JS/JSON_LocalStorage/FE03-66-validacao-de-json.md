# FE03-66 — Validação de JSON

## Por que validar

`JSON.parse` explode com `SyntaxError` em qualquer JSON malformado. Sem validação, um texto inválido — seja de um input, um arquivo corrompido ou uma resposta de API inesperada — derruba o script inteiro.

## Validação básica: try/catch

A forma mais comum — tente parsear e capture o erro:

```javascript
function isJSON(texto) {
  try {
    JSON.parse(texto);
    return true;
  } catch {
    return false;
  }
}

isJSON('{"a":1}');  // true
isJSON('{a:1}');    // false — chave sem aspas
isJSON('');          // false — string vazia não é JSON
```

## Validação com fallback

Em vez de retornar booleano, retorne o dado ou um valor padrão — padrão essencial ao ler localStorage:

```javascript
function lerJSON(chave, fallback = null) {
  try {
    const texto = localStorage.getItem(chave);
    return texto ? JSON.parse(texto) : fallback;
  } catch {
    return fallback;
  }
}

const config = lerJSON("config", { tema: "claro", idioma: "pt" });
// Se "config" existir → retorna o objeto parseado
// Se não existir ou estiver corrompido → { tema: "claro", idioma: "pt" }
```

## Validando a estrutura, não só a sintaxe

`JSON.parse` garante que o texto é JSON válido — mas não que tem os campos esperados. Um JSON válido pode estar "vazio" de informação útil:

```javascript
const dados = JSON.parse(texto);

// Sintaxe OK, mas e a estrutura?
if (!dados || typeof dados.nome !== "string") {
  throw new Error("Formato de usuário inválido");
}
```

### Função de validação de esquema simples

```javascript
function validarUsuario(obj) {
  return (
    obj !== null &&
    typeof obj === "object" &&
    typeof obj.nome === "string" &&
    typeof obj.idade === "number" &&
    obj.idade >= 0
  );
}

const texto = '{"nome":"Ana","idade":28}';
const dados = JSON.parse(texto);

if (validarUsuario(dados)) {
  salvar(dados);
} else {
  console.error("Usuário com formato inesperado");
}
```

## Erros clássicos de sintaxe JSON

| JSON inválido | Problema |
| --- | --- |
| `{nome: "Ana"}` | Chave sem aspas duplas |
| `{"nome": 'Ana'}` | Aspas simples |
| `{"a": 1,}` | Vírgula final (trailing comma) |
| `{"a": 1} // comentário` | Comentários não existem em JSON |
| `undefined` | Não é um valor JSON |
| `{"a": NaN}` | `NaN` não é JSON |
| `{"a": Infinity}` | `Infinity` não é JSON |
| `'{"a":1}'` em contexto errado | String contendo JSON ≠ JSON parseado |

## Ferramentas de validação

### No código — try/catch

```javascript
function parseOuPadrao(texto) {
  try {
    return { ok: true, dados: JSON.parse(texto) };
  } catch (erro) {
    return { ok: false, erro: erro.message };
  }
}
```

### Online

- **jsonlint.com** — cola o JSON, mostra erros linha a linha
- **JSON Formatter** — formata e valida ao mesmo tempo

### No editor

- VS Code valida JSON automaticamente em arquivos `.json`
- Extensões como "JSON Tools" e "Prettify JSON" ajudam a formatar

## Distinguindo os tipos de erro

```javascript
try {
  const dados = JSON.parse(texto);
  processar(dados);
} catch (erro) {
  if (erro instanceof SyntaxError) {
    console.error("JSON malformado:", erro.message);
  } else {
    console.error("Erro de processamento:", erro);
  }
}
```

`SyntaxError` = o texto não era JSON. Outros erros = JSON ok, mas o processamento falhou.

## Checklist de segurança

- Sempre `try/catch` em `JSON.parse` de origem externa
- Valide a **estrutura** depois de validar a **sintaxe**
- Forneça fallbacks sensatos — `lerJSON("chave", [])` para arrays, `{}` para objetos
- Nunca confie que o JSON de uma API tem o formato esperado — valide antes de usar
- Em produção, bibliotecas como **Zod** ou **Joi** fazem validação declarativa de esquemas

## Exemplo integrado — validar antes de salvar

```javascript
function salvarConfig(textoJSON) {
  const resultado = parseOuPadrao(textoJSON);

  if (!resultado.ok) {
    alert("JSON inválido — verifique a sintaxe");
    return false;
  }

  const { dados } = resultado;

  if (typeof dados.tema !== "string") {
    alert("Campo 'tema' obrigatório e deve ser string");
    return false;
  }

  localStorage.setItem("config", textoJSON);
  return true;
}
```
