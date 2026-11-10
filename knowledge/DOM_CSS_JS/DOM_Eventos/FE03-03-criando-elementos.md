# FE03-03 — Criando Elementos

## A Criação Programática de Elementos

Em vez de concatenar strings de texto com `.innerHTML` (o que pode recriar todo o DOM do container e causar perda de eventos já registrados), o padrão seguro e recomendado pela indústria utiliza **criação explícita de nós de elementos**.

O ciclo possui três etapas fundamentais:

```text
+-----------------------+     +-----------------------+     +-----------------------+
|  1. document.         | --> |  2. Configurar        | --> |  3. elementoPai.      |
|     createElement()   |     |     Texto, Classes    |     |     appendChild()     |
|  (Cria nó na memória) |     |     e Atributos       |     |  (Insere na tela)     |
+-----------------------+     +-----------------------+     +-----------------------+
```

---

## 1. `document.createElement(nomeDaTag)`

Cria uma nova tag HTML na memória do navegador:

```javascript
const novoBotao = document.createElement("button");
```

---

## 2. Configurando o Elemento Criado

Antes de colocar o elemento na tela, definimos suas propriedades, textos e identificadores:

```javascript
novoBotao.innerText = "Excluir Registro";
novoBotao.id = "btn-excluir";
novoBotao.setAttribute("type", "button");
```

---

## 3. Inserindo no DOM: `.appendChild()` e `.append()`

- **`elementoPai.appendChild(novoFilho)`:** adiciona o nó no **final da lista de filhos** daquele elemento pai.
- **`elementoPai.append(nó1, nó2, ...)` (Moderno):** permite inserir múltiplos elementos e strings de uma única vez.
- **`elementoPai.prepend(novoFilho)`:** insere o novo elemento no **início** do container pai.

```javascript
const container = document.querySelector("#painel-acoes");
container.appendChild(novoBotao);
```

---

## Removendo Elementos: `.remove()`

Para eliminar um elemento do DOM:

```javascript
const elementoAntigo = document.querySelector(".card-temporario");
if (elementoAntigo) {
  elementoAntigo.remove(); // Remove o elemento diretamente da tela
}
```
