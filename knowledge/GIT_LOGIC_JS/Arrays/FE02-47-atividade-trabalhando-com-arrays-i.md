# FE02-47 — Atividade: Trabalhando com Arrays I

## Objetivo da Atividade

Praticar a criação de arrays, leitura de propriedades, manipulação com métodos nativos de inserção e remoção (`push`, `pop`, `shift`, `unshift`) e busca de elementos com `.includes()` e `.indexOf()`.

---

## Enunciado do Desafio

Crie um script `gerenciadorTarefas.js` para controlar uma lista de afazeres diários:

1. Inicie um array `tarefas` contendo três atividades: `"Estudar HTML"`, `"Treinar CSS"`, `"Revisar Git"`.
2. Adicione uma nova tarefa no final da lista: `"Praticar JavaScript"`.
3. Adicione uma tarefa prioritária no início da lista: `"Tomar café da manhã"`.
4. Conclua e remova a última tarefa da lista guardando-a em uma variável.
5. Conclua e remova a primeira tarefa prioritária da lista.
6. Verifique se a tarefa `"Revisar Git"` ainda está presente na lista utilizando `.includes()`.
7. Encontre o índice exato da tarefa `"Treinar CSS"` utilizando `.indexOf()`.
8. Imprima no console o estado final do array e a quantidade de tarefas restantes.

---

## Solução de Referência

```javascript
// 1. Inicialização da lista
const tarefas = ["Estudar HTML", "Treinar CSS", "Revisar Git"];
console.log("Tarefas Iniciais:", tarefas);

// 2. Inserção no final
tarefas.push("Praticar JavaScript");

// 3. Inserção no início
tarefas.unshift("Tomar café da manhã");
console.log("Após inclusões:", tarefas);

// 4. Remoção do final
const tarefaConcluidaFinal = tarefas.pop();
console.log(`Tarefa finalizada: ${tarefaConcluidaFinal}`);

// 5. Remoção do início
const tarefaConcluidaInicio = tarefas.shift();
console.log(`Tarefa inicial finalizada: ${tarefaConcluidaInicio}`);

// 6. Verificação de presença com .includes()
const precisaRevisarGit = tarefas.includes("Revisar Git");
console.log("A tarefa 'Revisar Git' ainda está na lista?", precisaRevisarGit); // true

// 7. Localização do índice com .indexOf()
const indiceTreinoCSS = tarefas.indexOf("Treinar CSS");
console.log("Índice de 'Treinar CSS':", indiceTreinoCSS); // 1

// 8. Estado final consolidado
console.log("\n=== ESTADO FINAL DA LISTA ===");
console.log("Tarefas pendentes:", tarefas);
console.log("Total restante:", tarefas.length);
```
