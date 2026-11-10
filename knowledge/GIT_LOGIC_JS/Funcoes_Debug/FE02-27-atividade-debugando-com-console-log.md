# FE02-27 — Atividade: Debugando com console.log()

## A Arte da Depuração com `console.log()`

O processo de **depuração (debugging)** consiste em identificar, rastrear e corrigir comportamentos anômalos ou erros lógicos no código. O `console.log()` é a ferramenta mais rápida e acessível para inspecionar o estado das variáveis passo a passo.

---

## Métodos Complementares do Objeto `console`

| Método | Finalidade | Exibição Típica |
| --- | --- | --- |
| `console.log()` | Registro geral de dados e fluxo | Texto padrão |
| `console.warn()` | Avisos de alerta sobre potenciais problemas | Fundo amarelo com ícone de exclamação |
| `console.error()` | Erros críticos e exceções disparadas | Fundo vermelho com rastreamento de pilha (*stack trace*) |
| `console.table()` | Exibição de arrays ou objetos complexos | Tabela formatada e ordenada |

---

## Boas Práticas de Inspeção

Evite imprimir valores sem rótulo (ex: `console.log(x)`), pois em códigos longos é impossível lembrar a qual variável aquele número solto pertence. Identifique sempre o dado:

```javascript
const total = 1450;
const desconto = 150;

// Ruim:
console.log(total);

// Excelente (com identificação clara):
console.log("[DEBUG] Total bruto:", total);
console.log({ total, desconto }); // Dica moderna: envolver entre chaves gera um objeto automático!
```

---

## Exercício Prático de Debugging

Dado o código defeituoso abaixo que deveria calcular o preço com imposto de 10%, adicione pontos estratégicos de log para encontrar a falha:

```javascript
function calcularPrecoComTaxa(precoBase) {
  console.log("--> Entrada na função precoBase:", precoBase);

  const taxa = 0.10;
  console.log("--> Taxa aplicada:", taxa);

  // Erro comum de precedência ou cálculo
  const precoFinal = precoBase + precoBase * taxa;
  console.log("--> Preço final calculado:", precoFinal);

  return precoFinal;
}

const resultadoFinal = calcularPrecoComTaxa(100);
console.log("Resultado retornado:", resultadoFinal);
```
