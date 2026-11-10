# FE02-37 — Loops com for

## A Estrutura do Laço `for`

O laço `for` concentra os três elementos fundamentais (inicialização, condição e incremento) em uma única linha no cabeçalho do comando:

```javascript
for (inicializacao; condicao; incremento) {
  // Bloco de código executado a cada iteração
}
```

---

## Fluxo de Execução Passo a Passo

```javascript
for (let i = 1; i <= 3; i++) {
  console.log(`Volta número: ${i}`);
}
```

1. **1ª Etapa (Inicialização):** executa `let i = 1` apenas uma única vez no início.
2. **2ª Etapa (Checagem):** avalia `i <= 3` (1 <= 3 é `true`).
3. **3ª Etapa (Corpo):** executa o código dentro do bloco (`console.log`).
4. **4ª Etapa (Incremento):** executa `i++` (`i` passa a valer 2).
5. **Repetição:** repete os passos 2, 3 e 4. Quando `i` passa a valer 4, a condição `4 <= 3` é `false` e o loop termina.

---

## Variações Comuns do Laço `for`

### 1. Contagem Regressiva (Decremento)

```javascript
for (let i = 10; i >= 1; i--) {
  console.log(`Contagem: ${i}`);
}
console.log("Decolagem autorizada!");
```

### 2. Passos Customizados (Pulos de 2 em 2, 5 em 5)

```javascript
// Exibe números pares de 0 a 20:
for (let i = 0; i <= 20; i += 2) {
  console.log(i);
}
```

---

## As Instruções `break` e `continue`

- **`break`:** interrompe e encerra o laço imediatamente, saindo do bloco do loop:

```javascript
for (let i = 1; i <= 10; i++) {
  if (i === 6) {
    break; // Para o loop assim que atingir 6
  }
  console.log(i); // Imprime de 1 a 5
}
```

- **`continue`:** pula a iteração atual imediatamente e vai direto para a próxima volta:

```javascript
for (let i = 1; i <= 5; i++) {
  if (i === 3) {
    continue; // Pula apenas o número 3!
  }
  console.log(i); // Imprime: 1, 2, 4, 5
}
```
