# DM01-05 — Repetir requisições PUT e POST com segurança

## Efeito pretendido de uma operação idempotente

Se `PUT /preferencias/42` define o mesmo tema duas vezes com o mesmo corpo, o estado pretendido depois de cada requisição é o mesmo. Isso torna PUT idempotente segundo a semântica HTTP. As respostas podem ter status distintos, por exemplo 201 ao criar o recurso e 204 ao substituí-lo, e efeitos como logs podem se repetir.

Por outro lado, repetir `POST /pedidos` pode criar dois pedidos. A semântica de POST, sozinha, não garante idempotência. Antes de repetir automaticamente um POST após um timeout, confira o contrato do endpoint e se ele oferece um mecanismo para identificar a mesma operação.

Referência [RFC 9110 — Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2).
