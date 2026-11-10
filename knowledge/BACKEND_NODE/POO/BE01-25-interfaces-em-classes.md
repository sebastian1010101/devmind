# BE01-25 — Implementação de Interfaces em Classes

## `implements` — contrato obrigatório

A classe **promete** ter a forma da interface:

```typescript
interface Autenticavel {
  login(email: string, senha: string): boolean;
  logout(): void;
}

class Usuario implements Autenticavel {
  login(email: string, senha: string): boolean {
    return senha === "123456"; // simplificado
  }

  logout(): void {
    console.log("Saiu");
  }

  // ❌ esquecer um membro = erro de compilação
}
```

Se a classe não implementar tudo, o TS reclama na hora.

## Interface vs classe abstrata

```typescript
// Interface — só contrato, zero implementação
interface Pagavel {
  pagar(valor: number): void;
}

// Classe abstrata — contrato + código compartilhado
abstract class Pagavel {
  abstract pagar(valor: number): void;
  log() { /* implementação real herdada */ }
}
```

| Interface | Classe abstrata |
| --- | --- |
| Pode implementar várias | Só herda de uma |
| Sem implementação | Pode ter métodos concretos |
| Sem construtor | Tem construtor/estado |
| Não existe em runtime | Existe |

## Múltiplas interfaces

```typescript
interface Imprimivel {
  imprimir(): string;
}

interface Serializavel {
  paraJson(): string;
}

class Relatorio implements Imprimivel, Serializavel {
  imprimir() { return "Relatório..."; }
  paraJson() { return "{}"; }
}
```

Classe implementa N interfaces — é o "multiplo" que herança não permite.

## O padrão no backend: contrato de repositório

```typescript
interface Usuario {
  id: number;
  nome: string;
  email: string;
}

interface IUsuarioRepository {
  criar(dados: Omit<Usuario, "id">): Usuario;
  buscarPorId(id: number): Usuario | undefined;
  listar(): Usuario[];
}

// Implementação em memória — dev e testes
class UsuarioRepositoryMemoria implements IUsuarioRepository {
  private dados: Usuario[] = [];

  criar(dados: Omit<Usuario, "id">) {
    const u = { id: this.dados.length + 1, ...dados };
    this.dados.push(u);
    return u;
  }

  buscarPorId(id: number) {
    return this.dados.find((u) => u.id === id);
  }

  listar() {
    return this.dados;
  }
}

// Depois: UsuarioRepositoryPrisma implementa o MESMO contrato
```

## O ganho: injeção de dependência

```typescript
class UsuarioService {
  constructor(private repo: IUsuarioRepository) {}
  // recebe a INTERFACE — não a implementação concreta
}

// Testes: memória. Produção: Prisma. O service nem percebe.
const service = new UsuarioService(new UsuarioRepositoryMemoria());
```

Dependa de abstrações, não de implementações — o **D do SOLID**.

## Resumo

- `implements` = a classe jura seguir o contrato da interface
- N interfaces por classe; interfaces não carregam implementação
- Repositório por interface → troca memória por Prisma sem tocar o service
- Dependa de abstrações — injeção de dependência nasce daqui
