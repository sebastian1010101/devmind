# FE02-22 — Atividade: Funções sem Parâmetro

## Objetivo da Atividade

Praticar a criação, organização e invocação de funções simples sem parâmetros que encapsulam ações de exibição e mensagens padronizadas.

---

## Enunciado do Desafio

Crie um arquivo `painel.js` contendo funções sem parâmetros que exibam cabeçalhos, rodapés e relatórios padronizados no terminal para um sistema corporativo:

1. Uma função `imprimirCabecalho()` que exiba uma borda visual em caracteres `=` e o título da empresa.
2. Uma função `imprimirRodape()` que exiba um aviso de confidencialidade e o ano corrente.
3. Uma função `exibirAlertaSistema()` que imprima uma mensagem de manutenção preventiva.
4. Execute o programa chamando o cabeçalho, o alerta e o rodapé na ordem correta de exibição.

---

## Solução de Referência

```javascript
// 1. Função de cabeçalho
function imprimirCabecalho() {
  console.log("========================================");
  console.log("       SISTEMA INTERNO DEVMINDS         ");
  console.log("========================================");
}

// 2. Função de aviso de sistema
function exibirAlertaSistema() {
  console.log("[AVISO] Backup automático agendado para as 03:00.");
  console.log("[STATUS] Todos os serviços operando normalmente.");
}

// 3. Função de rodapé
function imprimirRodape() {
  console.log("----------------------------------------");
  console.log("Documento Confidencial - 2026");
  console.log("========================================\n");
}

// Invocação das funções na sequência planejada:
imprimirCabecalho();
exibirAlertaSistema();
imprimirRodape();
```
