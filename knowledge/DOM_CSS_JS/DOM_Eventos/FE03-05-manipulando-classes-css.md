# FE03-05 — Manipulando classes CSS

## Por que Alterar Classes em vez de Estilos Inline?

Alterar estilos diretamente com a propriedade `.style` (ex: `elemento.style.backgroundColor = "red"`) adiciona CSS inline com especificidade alta, misturando a lógica de programação com regras visuais.

A **boa prática da indústria** estabelece:
- O **CSS** define todas as classes de design e estados visuais (ex: `.ativo`, `.oculto`, `.modo-escuro`).
- O **JavaScript** apenas adiciona, remove ou alterna essas classes nos elementos conforme o usuário interage.

---

## O Objeto `classList`

O objeto `element.classList` é a interface padrão para manipular a lista de classes CSS de qualquer nó do DOM:

### 1. `classList.add(classe1, classe2, ...)`
Adiciona uma ou mais classes ao elemento sem sobrescrever as existentes:

```javascript
const alerta = document.querySelector(".banner");
alerta.classList.add("destaque", "animar");
```

### 2. `classList.remove(classe1, ...)`
Remove uma classe específica do elemento:

```javascript
alerta.classList.remove("destaque");
```

### 3. `classList.toggle(classe)`
Alterna a classe de forma automática:
- Se o elemento **já possuir** a classe, ele a **remove**.
- Se o elemento **não possuir** a classe, ele a **adiciona**.

```javascript
const menuLateral = document.querySelector(".sidebar");

// Perfeito para botões de abrir/fechar menu e alternador de tema escuro:
menuLateral.classList.toggle("aberto");
```

### 4. `classList.contains(classe)`
Retorna um valor booleano (`true` ou `false`) indicando se o elemento possui aquela classe específica:

```javascript
if (menuLateral.classList.contains("aberto")) {
  console.log("O menu está visível na tela.");
}
```
