# FE02-10 — Operadores Aritméticos

## Os Operadores Matemáticos no JavaScript

O JavaScript possui operadores aritméticos nativos para realizar cálculos numéricos comuns:

| Operador | Operação | Exemplo | Resultado |
| --- | --- | --- | --- |
| `+` | Adição (Soma) | `10 + 5` | `15` |
| `-` | Subtração | `10 - 4` | `6` |
| `*` | Multiplicação | `4 * 3` | `12` |
| `/` | Divisão Real | `15 / 2` | `7.5` |
| `%` | Módulo (Resto da divisão inteira) | `10 % 3` | `1` |
| `**` | Exponenciação (Potência) | `2 ** 3` | `8` |

---

## O Poder do Operador Módulo (`%`)

O operador `%` retorna o **resto que sobra de uma divisão inteira**. É amplamente utilizado na lógica de programação para:

### 1. Descobrir se um número é Par ou Ímpar

- Se `numero % 2 === 0`, o número é **par** (divisão exata por 2).
- Se `numero % 2 !== 0`, o número é **ímpar** (sobra 1).

### 2. Ciclos e Limites Circulares

- Útil para alternar índices em carrosséis, relógios e repetições periódicas.

---

## Precedência de Operadores

Assim como na matemática convencional, o JavaScript segue a ordem padrão de operações:

1. **Parênteses `()`** têm a maior prioridade e executam primeiro.
2. **Exponenciação `**`**.
3. **Multiplicação `*`, Divisão `/` e Módulo `%`** (da esquerda para a direita).
4. **Adição `+` e Subtração `-`** (da esquerda para a direita).

```javascript
// Sem parênteses: primeiro multiplica 5 * 2 = 10, depois soma 10 + 10 = 20
const calculo1 = 10 + 5 * 2; // 20

// Com parênteses: primeiro soma 10 + 5 = 15, depois multiplica 15 * 2 = 30
const calculo2 = (10 + 5) * 2; // 30
```

---

## Operadores de Atribuição Aritmética Abreviada

Para atualizar uma variável com base no seu valor anterior de forma compacta:

```javascript
let total = 100;

total += 20; // Equivalente a: total = total + 20 (Resultado: 120)
total -= 10; // Equivalente a: total = total - 10 (Resultado: 110)
total *= 2;  // Equivalente a: total = total * 2  (Resultado: 220)
total /= 4;  // Equivalente a: total = total / 4  (Resultado: 55)

// Incremento e Decremento unitário:
let contador = 0;
contador++; // Incrementa 1 (contador passa a valer 1)
contador--; // Decrementa 1 (contador volta a valer 0)
```
