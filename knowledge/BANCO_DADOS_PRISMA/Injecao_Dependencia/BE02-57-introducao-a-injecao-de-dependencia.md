# BE02-57 — Introdução a Injeção de Dependência

## O problema — acoplamento

```ts
class UsuarioService {
  private repo = new UsuarioRepository();   // ← criou a dependência
  private mailer = new EmailService();      // ← e esta também

  async criar(dados) { ... }
}
```

`UsuarioService` **instancia** suas dependências — está colado a implementações concretas:

- Testar exige o repositório real → precisa de banco
- Trocar `EmailService` por `MailgunService` → editar a classe
- Duas implementações coexistindo → impossível sem if

## Inversão de controle

```ts
class UsuarioService {
  constructor(
    private repo: IUsuarioRepository,    // recebe pronto, não cria
    private mailer: IEmailService,
  ) {}
}
```

```text
Antes:   Service cria Repo          (service controla)
Depois:  Repo é injetado no Service (quem chama controla)
```

O controle da dependência **inverte**: em vez de `new` interno, recebe de fora. Quem monta a árvore de objetos é o **container** ou o bootstrap.

## Por que isso importa

### Testes

```ts
// teste unitário — injeta um fake, sem banco
const repoFake = { criar: jest.fn().mockResolvedValue({ id: 1 }) };
const service = new UsuarioService(repoFake, mailerFake);
```

### Substituição

```ts
// dev: EmailService fake que loga
// prod: EmailService real que envia
container.register("EmailService", { useClass: ... });
```

### Desacoplamento

O service depende de **interface/abstração**, não de implementação — trocar a peça não quebra a máquina.

## Os papéis

| Papel | Quem |
| --- | --- |
| **Interface/contrato** | `IUsuarioRepository` — o que a dependência oferece |
| **Implementação** | `PrismaUsuarioRepository`, `MockUsuarioRepository` |
| **Cliente** | `UsuarioService` — usa via contrato |
| **Container/injetor** | Registra quem implementa o quê e resolve |

## Sem framework — injeção manual

```ts
// no bootstrap
const repo = new PrismaUsuarioRepository(prisma);
const mailer = new SmtpEmailService();
const service = new UsuarioService(repo, mailer);
const controller = new UsuarioController(service);
```

Funciona — mas vira uma lista crescente de `new`s. É o que o **tsyringe** automatiza (próxima aula).

## Resistências comuns

- "É overengineering" — para 3 classes, sim; para 30, é o que mantém testável
- "Só preciso do Prisma" — Prisma pode ser a dependência injetada também

## Erros comuns

| Erro | Correção |
| --- | --- |
| `new Repo()` dentro do service | Receba via construtor |
| Service dependendo da classe concreta | Dependa de interface/`type` |
| Singleton manual espalhado | Container resolve uma vez |
| Injetar tudo | Injete o que varia — constantes não precisam |

## Resumo

- DI = dependência recebida, não criada — via construtor
- Dependa de abstração (interface), não de implementação concreta
- Ganho real: testes com fakes, implementações trocáveis
- Manual funciona para pouco; container (tsyringe) escala
