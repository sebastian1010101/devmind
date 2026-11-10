# FE03-34 — REM

## A Unidade de Medida da Acessibilidade

A unidade **`rem`** significa *Root EM* (EM da Raiz). Ela é uma unidade de medida relativa calculada exclusivamente em relação ao tamanho da fonte do elemento raiz `<html>`:

```text
Se o elemento <html> possui font-size: 16px (padrão dos navegadores):
  1rem   = 16px
  0.5rem = 8px
  1.5rem = 24px
  2rem   = 32px
```

---

## Por que Usar `rem` em vez de `px`?

### O Princípio da Acessibilidade do Usuário

Usuários com baixa visão ou dificuldades de leitura costumam alterar o tamanho padrão de fonte nas configurações do seu sistema operacional ou navegador (por exemplo, de 16px para 24px):

- **Se o seu site foi feito em `px` fixos:** o navegador é forçado a ignorar a escolha do usuário, mantendo textos minúsculos e inacessíveis.
- **Se o seu site foi feito em `rem`:** todo o layout (fontes, paddings, margens e alturas de linha) escala proporcionalmente em harmonia, respeitando a configuração de acessibilidade.

---

## Tabela de Conversão Prática (Base 16px)

| Pixels (px) | Valor em REM | Aplicação Típica |
| --- | --- | --- |
| `4px` | `0.25rem` | Espaçamentos mínimos, bordas de tags |
| `8px` | `0.5rem` | Preenchimento de badges e botões compactos |
| `12px` | `0.75rem` | Legendas, datas e textos secundários |
| `16px` | `1rem` | Texto padrão de parágrafos e inputs |
| `20px` | `1.25rem` | Subtítulos de cards |
| `24px` | `1.5rem` | Títulos `<h2>` ou paddings de containers |
| `32px` | `2rem` | Títulos de destaque `<h1>` |
| `48px` | `3rem` | Números gigantes de banners (*Hero Section*) |
