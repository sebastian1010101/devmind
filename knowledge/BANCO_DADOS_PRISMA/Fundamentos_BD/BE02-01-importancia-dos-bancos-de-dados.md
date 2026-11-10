# BE02-01 — Importância dos Bancos de Dados na Tecnologia Moderna

## Onde eles estão

Quase todo sistema que você usa depende de banco de dados:

- **Bancos/fintechs** — saldo, transações, histórico
- **E-commerce** — catálogo, pedidos, estoque
- **Redes sociais** — perfis, posts, curtidas, mensagens
- **Streaming** — catálogo, progresso de visualização, recomendações
- **Saúde** — prontuários, exames, agendamentos

## O que o banco garante

### Persistência

O dado sobrevive ao processo. Se o servidor reinicia, os dados continuam lá — diferente de variáveis em memória.

```text
app restart → memória limpa → banco intacto → app religa e continua
```

### Consistência e integridade

Regras declaradas no banco são **sempre** enforceadas — não dependem do desenvolvedor lembrar:

```sql
email VARCHAR(255) UNIQUE NOT NULL
```

Nenhuma aplicação consegue inserir email duplicado ou nulo — o banco barra.

### Transações — ACID

Operações que precisam acontecer "tudo ou nada":

```sql
BEGIN;
UPDATE contas SET saldo = saldo - 100 WHERE id = 1;
UPDATE contas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;
```

| Propriedade | Significado |
| --- | --- |
| **A**tomicidade | Tudo ou nada — não existe "meia transferência" |
| **C**onsistência | O banco sai de um estado válido para outro válido |
| **I**solamento | Transações simultâneas não se interferem |
| **D**urabilidade | Depois do `COMMIT`, o dado não se perde |

Se o servidor cair no meio da transferência, o `ROLLBACK` automático desfaz — ninguém perde dinheiro no limbo.

### Concorrência

Milhares de usuários ao mesmo tempo. O SGBD gerencia locks e versões dos dados para que consultas e escritas coexistam sem corrupção.

### Performance

- **Índices** tornam buscas rápidas mesmo em tabelas gigantes
- O **otimizador de consultas** escolhe o melhor caminho para executar cada SQL

```sql
-- sem índice: lê a tabela inteira (full scan)
-- com índice em email: vai direto ao registro
CREATE INDEX idx_usuarios_email ON usuarios(email);
```

### Segurança

- Autenticação por usuário do banco
- Permissões granulares: quem pode `SELECT`, quem pode `INSERT`, em quais tabelas
- Senhas e dados sensíveis nunca trafegam pela aplicação sem controle

## O papel na arquitetura de uma API

```text
Cliente → API (Express/Node) → Banco de dados (PostgreSQL)
              ↑
         regras de negócio vivem aqui,
         mas o dado verdadeiro vive no banco
```

A API é stateless — pode ser recriada a qualquer momento. O **banco é a fonte da verdade**.

## Por que isso importa para o dev

- Saber modelar dados evita retrabalho (mudança de schema em produção é cara)
- Consultas bem escritas são a diferença entre 5ms e 5s de resposta
- Entender transações evita bugs de dinheiro sumindo/duplicando

## Resumo

- Bancos de dados sustentam praticamente todo software moderno
- Garantem persistência, integridade, transações ACID, concorrência e segurança
- Índices e otimizador entregam performance em escala
- Na arquitetura de API, o banco é a fonte da verdade — a aplicação é descartável, o dado não
