# BE02-22 — Atividade: Praticando Relacionamento N-N

## Objetivo

Implementar um N-N completo: tabela intermediária, PK composta, dados e consultas cruzando os dois lados.

## Modelo sugerido — música

```text
artista >───< genero   via   artista_genero
musica  >───< playlist via   playlist_musica
```

## Implementação

```sql
CREATE DATABASE musicas_db;
\c musicas_db

CREATE TABLE artistas (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL
);

CREATE TABLE playlists (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL
);

CREATE TABLE musicas (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  artista_id INT NOT NULL REFERENCES artistas(id)
);

CREATE TABLE playlist_musicas (
  playlist_id INT NOT NULL REFERENCES playlists(id),
  musica_id INT NOT NULL REFERENCES musicas(id),
  posicao INT,
  PRIMARY KEY (playlist_id, musica_id)
);
```

Note: `playlist_musicas` tem `posicao` — a relação tem atributo próprio (a ordem da música na playlist).

## Populando

```sql
INSERT INTO artistas (nome) VALUES ('Djavan'), ('Gal Costa');

INSERT INTO musicas (titulo, artista_id) VALUES
  ('Oceano', 1),
  ('Flor de Lis', 1),
  ('Baby', 2);

INSERT INTO playlists (nome) VALUES ('MPB Clássica'), ('Favoritas');

INSERT INTO playlist_musicas (playlist_id, musica_id, posicao) VALUES
  (1, 1, 1), (1, 3, 2),
  (2, 2, 1), (2, 3, 2);
```

## Consultas para praticar

```sql
-- músicas da playlist 1, em ordem
SELECT m.titulo, pm.posicao
FROM playlist_musicas pm
JOIN musicas m ON m.id = pm.musica_id
WHERE pm.playlist_id = 1
ORDER BY pm.posicao;

-- playlists que contêm "Baby"
SELECT p.nome
FROM playlist_musicas pm
JOIN playlists p ON p.id = pm.playlist_id
JOIN musicas m ON m.id = pm.musica_id
WHERE m.titulo = 'Baby';

-- artista das músicas de uma playlist (três tabelas!)
SELECT DISTINCT a.nome
FROM playlist_musicas pm
JOIN musicas m ON m.id = pm.musica_id
JOIN artistas a ON a.id = m.artista_id
WHERE pm.playlist_id = 1;
```

## Testando as regras

```sql
-- deve falhar: mesma música 2x na playlist
INSERT INTO playlist_musicas (playlist_id, musica_id) VALUES (1, 1);
-- ERROR: duplicate key violates PRIMARY KEY

-- deve falhar: música inexistente
INSERT INTO playlist_musicas (playlist_id, musica_id) VALUES (1, 99);
-- ERROR: violates foreign key constraint
```

## Critérios de conclusão

1. Tabela intermediária com PK composta funcionando
1. Atributo próprio da relação (`posicao`) populado e consultável
1. Query de 3 tabelas (playlist → junção → música → artista) retornando
1. PK composta barrando duplicata

## Resumo

- N-N = intermediária com 2 FKs; PK composta impede repetição
- `posicao` mostra que a junção pode guardar dados da relação
- Consultas encadeiam JOINs — às vezes 3+ tabelas no caminho
