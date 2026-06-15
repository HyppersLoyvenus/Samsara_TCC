# Samsara TCC

## Como subir com Docker

1. Crie o arquivo de ambiente:

```bash
copy .env.example .env
```

2. Suba a aplicacao:

```bash
docker compose up --build
```

O frontend fica disponivel em http://localhost:5000.

Para gerar uma nova migration depois de alterar modelos:

```bash
docker compose run --rm backend flask db migrate -m "descricao_da_alteracao"
```

Depois confira o arquivo criado em `migrations/versions/` e suba novamente:

```bash
docker compose up --build
```

## Como subir sem Docker

1. Criar e ativar o `.venv`:

```bash
python -m venv .venv
cd .venv/Scripts
activate
cd ../..
```

2. Criar e ajustar o `.env`. Para rodar fora do Docker, use `DATABASE_URL=sqlite:///database.db`.

3. Instalar dependencias, aplicar migrations e iniciar:

```bash
pip install -r requirements.txt
flask db upgrade
python main.py
```
