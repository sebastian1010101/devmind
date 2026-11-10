# FE03-62 — Módulos ES6 (import/export)

## O que são

Módulos ES6 (ESM) são o sistema nativo de organização de código do JavaScript: cada arquivo é um módulo isolado que **exporta** o que quer compartilhar e **importa** o que precisa — sem poluir o escopo global.

Antes do ESM, tudo ficava no escopo global (ou se usava `script` tags em ordem frágil). Com módulos, cada arquivo é uma caixa fechada.

## Ativando módulos no navegador

```html
<script type="module" src="app.js"></script>
```

O `type="module"` muda três coisas:

- Escopo isolado — variáveis não vazam para `window`
- `import`/`export` habilitados
- `defer` automático — o script espera o HTML estar pronto

## Exportando

### Named exports — vários por arquivo

```javascript
// utils.js
export const PI = 3.14159;

export function somar(a, b) {
  return a + b;
}

const versao = "1.0";
export { versao }; // exportação no fim do arquivo também funciona
```

### Default export — um por arquivo

```javascript
// Usuario.js
export default class Usuario {
  constructor(nome) {
    this.nome = nome;
  }
}
```

Um arquivo pode ter **um** `export default` e vários `named exports`:

```javascript
export default function principal() { }
export const auxiliar = () => { };
export const CONSTANTE = 42;
```

## Importando

### Named imports — chaves obrigatórias, nome exato

```javascript
import { somar, PI } from "./utils.js";

console.log(somar(1, 2)); // 3
console.log(PI);          // 3.14159
```

### Renomeando na importação

```javascript
import { somar as adicionar } from "./utils.js";
adicionar(1, 2); // 3
```

### Default import — sem chaves, nome livre

```javascript
import Usuario from "./Usuario.js"; // o nome 'Usuario' é escolha sua
import QualquerNome from "./Usuario.js"; // funciona igual
```

### Combinando default + named

```javascript
import principal, { auxiliar, CONSTANTE } from "./app.js";
```

### Importando tudo de uma vez

```javascript
import * as utils from "./utils.js";

utils.somar(1, 2); // acessa via namespace
utils.PI;
```

### Import só para efeito colateral

```javascript
import "./config.js"; // executa o arquivo, sem importar nada
```

## Organização típica de projeto

```text
src/
├── index.html
├── app.js          ← ponto de entrada (importa os módulos)
├── utils/
│   ├── format.js   ← export function formatarMoeda()
│   └── dom.js      ← export function criarElemento()
├── services/
│   └── api.js      ← export async function buscarDados()
└── components/
    ├── Header.js   ← export default Header
    └── Card.js     ← export default Card
```

```javascript
// app.js — orquestra os módulos
import Header from "./components/Header.js";
import { buscarDados } from "./services/api.js";
import { formatarMoeda } from "./utils/format.js";
```

## Módulos vs script tradicional

| Aspecto | `<script>` normal | `<script type="module">` |
| --- | --- | --- |
| Escopo | Global (`window`) | Isolado ao arquivo |
| `import`/`export` | Não | Sim |
| Carregamento | Bloqueia o HTML | `defer` automático |
| `this` no topo | `window` | `undefined` |
| Modo estrito | Opcional | Sempre ativo |

## Requisito: servidor HTTP

Módulos **não funcionam** abrindo o arquivo com `file://` — o navegador bloqueia por segurança (CORS). É preciso um servidor local:

```bash
# Opção 1: Live Server do VS Code (clique direito → Open with Live Server)
# Opção 2: Python
python3 -m http.server 5500

# Opção 3: Node
npx serve .
```

Acesso via `http://localhost:5500` — não `file:///...`

## Caminhos relativos

```javascript
import { x } from "./utils.js";      // mesma pasta
import { y } from "../lib/util.js";  // pasta acima
import { z } from "/src/config.js";  // caminho absoluto da raiz
```

## Erros comuns

| Erro | Causa |
| --- | --- |
| `Cannot use import outside a module` | Falta `type="module"` no `<script>` ou no Node falta `"type": "module"` no package.json |
| `Failed to fetch dynamically` / CORS | Abrindo `file://` — use servidor local |
| `Cannot find module` | Caminho errado ou falta a extensão `.js` (navegador exige o caminho completo) |
| `SyntaxError: export` | `export` fora de contexto de módulo — confira o `type="module"` |

## Boas práticas

- **Um módulo, uma responsabilidade** — arquivo gigante vira ponto de atrito
- **Named exports para utilidades** — facilitam autocomplete e refatoração
- **Default export para componentes/classes** — convenção do React e frameworks
- **`index.js` como porta de entrada** da pasta — `import { x } from "./utils"` resolve `./utils/index.js` no Node (não no navegador puro)
- **Sem efeitos colaterais silenciosos** — módulos devem exportar, não executar lógica pesada ao carregar
