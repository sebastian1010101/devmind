# FE02-23 — Funções com e sem Retorno

## A Palavra-Chave `return`

A diretiva `return` especifica qual valor a função deve **devolver para quem a invocou**.

Sem o comando `return`, a função executa suas linhas e finaliza devolvendo implicitamente o valor primitivo `undefined`.

---

## 1. Funções sem Retorno (Procedimentos / Efeitos Colaterais)

São funções cujo objetivo é executar uma ação externa (exibir no console, gravar em banco, disparar um alerta), mas que não precisam produzir um dado que será reaproveitado em cálculos posteriores:

```javascript
function exibirMensagem(texto) {
  console.log(`[LOG]: ${texto}`);
}

const resultado = exibirMensagem("Olá!"); // Imprime na tela
console.log(resultado); // undefined (nenhum valor retornado)
```

---

## 2. Funções com Retorno

Produzem um resultado concreto que pode ser armazenado em variáveis, passado como argumento para outras funções ou usado em operações matemáticas:

```javascript
function calcularAreaQuadrado(lado) {
  return lado * lado;
}

// O valor retornado é guardado na constante:
const areaQuarto = calcularAreaQuadrado(5);
console.log(`A área é de ${areaQuarto} metros quadrados.`); // 25
```

---

## O Encerramento Imediato da Função pelo `return`

Assim que o interpretador atinge a palavra-chave `return`, a execução da função é **interrompida imediatamente**, e nenhuma linha abaixo dela dentro do mesmo bloco é executada:

```javascript
function verificarMaioridade(idade) {
  if (idade >= 18) {
    return "Maior de idade";
  }

  return "Menor de idade";
  console.log("Esta linha NUNCA será executada!");
}
```
