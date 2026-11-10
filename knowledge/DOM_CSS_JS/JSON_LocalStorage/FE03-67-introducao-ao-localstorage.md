# FE03-67 — Introdução ao LocalStorage

## O que é

`localStorage` é uma API do navegador que armazena dados **de forma persistente** — os dados sobrevivem ao fechamento da aba, do navegador e até à reinicialização do computador. Faz parte do conjunto **Web Storage API**, junto com `sessionStorage`.

## localStorage vs sessionStorage vs cookies

| Característica | `localStorage` | `sessionStorage` | Cookies |
| --- | --- | --- | --- |
| Persistência | Permanente (até limpar) | Só na aba/sessão | Configurável |
| Capacidade | ~5-10 MB | ~5-10 MB | ~4 KB |
| Enviado ao servidor | Não | Não | Sim (a cada request) |
| Acesso | `window.localStorage` | `window.sessionStorage` | `document.cookie` |
| Escopo | Por origem (protocolo + domínio + porta) | Por aba + origem | Por domínio/path |

## A API

São apenas 5 operações — todas síncronas e simples:

```javascript
// Salvar
localStorage.setItem("tema", "escuro");

// Ler
const tema = localStorage.getItem("tema"); // "escuro"

// Verificar existência (getItem retorna null se não existir)
const existe = localStorage.getItem("tema") !== null;

// Remover uma chave
localStorage.removeItem("tema");

// Limpar TUDO da origem
localStorage.clear();
```

## Regra fundamental: só armazena strings

`localStorage` aceita **apenas strings**. Qualquer outro tipo é convertido com `toString()` — o que destrói objetos:

```javascript
localStorage.setItem("numero", 42);
localStorage.getItem("numero"); // "42" — string, não number!

localStorage.setItem("obj", { a: 1 });
localStorage.getItem("obj"); // "[object Object]" — perdido!

localStorage.setItem("lista", [1, 2, 3]);
localStorage.getItem("lista"); // "1,2,3" — virou CSV, não array!
```

### A ponte: JSON

Para guardar objetos e arrays, serialize com `JSON.stringify` e recupere com `JSON.parse`:

```javascript
const usuario = { nome: "Ana", idade: 28 };

// Salvar
localStorage.setItem("usuario", JSON.stringify(usuario));

// Recuperar
const texto = localStorage.getItem("usuario");
const obj = JSON.parse(texto);
console.log(obj.nome); // "Ana"
```

## Inspecionando no DevTools

```text
DevTools → Application (aba) → Storage → Local Storage → [sua origem]
```

Aí você vê todas as chaves/valores, pode editar, deletar e adicionar diretamente — essencial para depuração.

## Onde vive e quando expira

- **Origem isolada** — `http://localhost:5500` e `http://localhost:3000` são origens **diferentes**, com storages separados
- **Sem expiração automática** — dados ficam até o usuário limpar (manualmente ou via `localStorage.clear()`)
- **Compartilhado entre abas** — duas abas do mesmo site veem o mesmo storage (evento `storage` sincroniza)

## Casos de uso típicos

- **Preferências do usuário** — tema claro/escuro, idioma, tamanho de fonte
- **Dados de formulário** — salvar rascunho antes de enviar
- **Cache simples** — dados de API que não mudam frequentemente
- **Carrinho de compras** — manter itens entre sessões
- **Flags de onboarding** — "já viu o tutorial"

## Casos que NÃO deve usar

- **Tokens de autenticação sensíveis** — vulnerável a XSS (ver FE03-71)
- **Dados grandes** — limite de ~5 MB, sem indexação
- **Dados que precisam ser consultados** — para isso existe IndexedDB
- **Dados críticos** — o usuário pode limpar a qualquer momento

## Compatibilidade

Suporte universal em todos os navegadores modernos — IE8+ incluído. Não funciona em modo anônimo restrito ou quando o usuário desabilita cookies/armazenamento.

## A sintaxe alternativa (não recomendada)

```javascript
// Funciona, mas evita os métodos claros
localStorage.tema = "escuro";
localStorage.tema;       // "escuro"
delete localStorage.tema;
```

Use sempre os métodos `setItem`, `getItem`, `removeItem` — são explícitos e menos propensos a conflitos com propriedades internas.
