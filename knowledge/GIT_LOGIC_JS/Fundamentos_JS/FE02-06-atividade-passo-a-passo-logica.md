# FE02-06 — Atividade: Passo a Passo Lógica

## Objetivo da Atividade

Desenvolver o pensamento computacional através do exercício de **decomposição de problemas complexos em etapas atômicas sequenciais**, aplicando estruturas condicionais básicas em pseudocódigo antes de escrever código real.

---

## Enunciado do Desafio 1: O Algoritmo da Lâmpada

Escreva o passo a passo lógico para o problema cotidiano: *"A lâmpada do meu quarto não está acendendo"*.

### Resolução de Referência

1. Início do procedimento.
2. Verificar se o interruptor da parede está na posição ligado.
   - Se estiver desligado: ligar o interruptor e verificar se acendeu.
   - Se acendeu: problema resolvido &rarr; Fim.
3. Se continuar apagada, verificar se a lâmpada está rosqueada firmemente no bocal.
   - Se estiver frouxa: rosquear e testar novamente.
   - Se acendeu: problema resolvido &rarr; Fim.
4. Se continuar apagada, verificar se há energia elétrica no restante da casa.
   - Se não houver energia geral: aguardar o retorno da rede elétrica &rarr; Fim.
5. Se houver energia na casa, a lâmpada atual provavelmente está queimada:
   - Retirar a lâmpada com segurança.
   - Substituir por uma lâmpada nova e funcional.
   - Testar o interruptor.
6. Fim do procedimento.

---

## Enunciado do Desafio 2: Média Escolar de um Aluno

Elabore um algoritmo para calcular a média de duas provas bimestrais de um estudante e determinar sua situação acadêmica:

- Média maior ou igual a 7.0: Aprovado.
- Média entre 5.0 e 6.9: Recuperação.
- Média menor que 5.0: Reprovado.

### Resolução em Pseudocódigo

```text
ALGORITMO CalcularMediaEscolar
INÍCIO
  // 1. Entrada de dados
  LER nota1
  LER nota2

  // 2. Processamento
  media = (nota1 + nota2) / 2

  // 3. Tomada de decisão lógica
  SE media >= 7.0 ENTÃO
    EXIBIR "Parabéns! O aluno está Aprovado com média: " + media
  SENÃO SE media >= 5.0 ENTÃO
    EXIBIR "O aluno está em Recuperação com média: " + media
  SENÃO
    EXIBIR "Infelizmente o aluno está Reprovado com média: " + media
  FIM_SE
FIM
```
