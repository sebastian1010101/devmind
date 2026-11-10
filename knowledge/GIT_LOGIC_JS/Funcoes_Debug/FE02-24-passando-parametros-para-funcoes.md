# FE02-24 — Passando Parâmetros para Funções

## Parâmetros vs Argumentos

Embora muitas vezes usados como sinônimos, possuem papéis técnicos distintos:

- **Parâmetros:** as variáveis declaradas na **definição da função** (entre os parênteses da criação).
- **Argumentos:** os valores reais enviados na **chamada da função** (entre os parênteses da invocação).

```javascript
// 'largura' e 'altura' são PARÂMETROS
function calcularArea(largura, altura) {
  return largura * altura;
}

// 10 e 5 são ARGUMENTOS
const resultado = calcularArea(10, 5);
```

---

## Parâmetros com Valores Padrão (Default Parameters)

Caso um argumento não seja fornecido na chamada da função, seu parâmetro correspondente assumirá o valor `undefined`. Para evitar erros ou resultados como `NaN`, o ES6 permite definir valores padrão:

```javascript
// 'taxa' possui valor padrão de 0.05 (5%) caso não seja informado
function calcularPrecoFinal(valor, taxa = 0.05) {
  return valor + (valor * taxa);
}

console.log(calcularPrecoFinal(100, 0.10)); // 110 (usou taxa enviada de 10%)
console.log(calcularPrecoFinal(100));       // 105 (usou taxa padrão de 5%)
```

---

## Parâmetros Ilimitados com Rest Operator (`...`)

Quando você não sabe com antecedência quantos argumentos o usuário irá passar:

```javascript
function somarTudo(...numeros) {
  let total = 0;
  for (const n of numeros) {
    total += n;
  }
  return total;
}

console.log(somarTudo(1, 2));             // 3
console.log(somarTudo(10, 20, 30, 40, 5)); // 105
```
