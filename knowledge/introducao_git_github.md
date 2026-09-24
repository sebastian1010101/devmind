# Aula - Introdução ao Git e GitHub

## Introdução

Primeiramente, não devemos confundir Git com GitHub. Apesar de trabalharem juntos, eles se diferem, principalmente nos conceitos. O Git é um sistema de controle de versão, onde você registra todas as alterações feitas no código localmente. Por outro lado, o GitHub, é uma plataforma onde você armazena remotamente seus códigos e projetos.

## Git

O Git é um sistema de controle de versão que permite uma equipe ou grupo de pessoas a trabalhar no mesmo código simultaneamente. Com a possibilidade de manter um histórico de alterações feitas em cada linha de código, faz com que o projeto seja desenvolvido em paralelo sem interferir no código de outro desenvolvedor.

É possível salvar todas as alterações para saber quem, quando e o que foi alterado no projeto.

## GitHub

O GitHub é uma plataforma onde hospedamos nossos códigos-fontes. Ele permite que você crie repositórios fora de sua máquina e compartilhe com outros desenvolvedores.

Você pode subir seu repositório Git localmente para la plataforma GitHub, por exemplo.

Além do fácil compartilhamento de código com a comunidade, o GitHub hoje tem se tornado uma grande rede social entre os desenvolvedores, já que é possível deixar seus códigos visíveis para que recrutadores e outros desenvolvedores possam visualizar seus códigos, tornando-se um grande portfólio.

Apesar de não ser o único no mercado, é a plataforma mais relevante na comunidade. Para ter acesso e começar a subir seus códigos, crie uma conta no site oficial do GitHub.

## Diferenças entre Git e GitHub

| Git | GitHub |
| :--- | :--- |
| Cria repositórios git | Armazena Repositórios git |
| Funcionamento offline | Não funciona offline |
| O código pode ser distribuído em diversas funcionalidades | Centraliza a versão final para contribuição |
| Funcionamento Local | Funcionamento Remoto |

## Principais Termos

### Commits

Um dos termos mais comuns que você irá ouvir são os commits. São eles que vão gravar a(s) última(s) mudança(s) no seu código. Basicamente, é a forma de salvar tudo o que foi feito para não perder nenhum progresso no seu projeto. Além disso, podemos subir nosso código em 'partes' para o GitHub enviando os commits e acessá-los posteriormente para uma eventual correção e podendo consultar o que foi alterado entre um commit e outro.

### Branch

Outro termo comum utilizado no versionamento de código, são as branches. Para ter uma melhor clareza, imagine seu código fonte sendo uma árvore e cada branch sendo literalmente um galho dessa árvore. Você pode ter a sua própria branch e ir acoplando ela, ou seja, integrando sua parte do código em um código muito maior, por ejemplo. São elas que mantêm um trabalho em grupo bem organizado e sem conflitos.

### Clone

Quando clonamos um repositório, significa que iremos copiar todo o código fonte feito por outro desenvolvedor para rodar em nossa máquina. Em resumo, pegamos o código que está em uma plataforma de hospedagem de repositórios como o GitHub e copiamos para nossa máquina a fim de fazer alterações nesse código, implementar alguma lógica, etc.

### Push

Finalmente quando queremos subir nosso código para o GitHub, devemos dar o push desse código. Assim todas as alterações feitas (depois de ter feito o commit), ficarão gravadas em nosso repositório remoto no GitHub.

### Pull

O conceito de dar um pull em um código é parecido com o clone. Porém a diferença é que damos um pull em um código somente quando já temos ele em nossa máquina. Ou seja, depois de clonar o repositório, caso algum membro de uma equipe tenha feito atualizações no código e salvo no GitHub, podemos dar um pull nesse código para trazer essas atualizações para a nossa máquina local.

