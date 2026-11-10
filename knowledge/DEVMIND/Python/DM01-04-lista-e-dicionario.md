# DM01-04 — Escolher entre lista e dicionário em Python

## Índices, chaves e valor padrão

Uma lista é uma sequência acessada por posição. Um dicionário associa chaves a valores. Para registrar quantas vezes cada status apareceu, use o status como chave. Com `get(status, 0)`, uma chave ausente devolve zero. O acesso `totais[status]` levantaria `KeyError` se a chave ainda não existisse.

```python
totais = {}
for status in ["aberto", "fechado", "aberto"]:
    totais[status] = totais.get(status, 0) + 1
# {"aberto": 2, "fechado": 1}
```

Referência [Python Tutorial — Data Structures](https://docs.python.org/3/tutorial/datastructures.html#dictionaries).
