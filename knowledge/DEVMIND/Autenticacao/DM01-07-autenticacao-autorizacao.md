# DM01-07 — Autenticação, autorização e status HTTP

## Quando usar 401 e 403

Autenticar é identificar quem fez a requisição. Autorizar é verificar se essa identidade tem permissão para executar a ação. Uma API pode retornar 401 quando as credenciais válidas estão ausentes e incluir um desafio `WWW-Authenticate`. Se a identidade foi reconhecida, mas não pode acessar um relatório reservado à equipe administrativa, 403 é apropriado.

Aplique a verificação de permissão no servidor a cada recurso protegido. Ocultar um botão na interface ajuda a navegação, mas a decisão de acesso deve ser feita pela API.

Referências [RFC 9110 — 401 Unauthorized](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.2) e [403 Forbidden](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.4).
