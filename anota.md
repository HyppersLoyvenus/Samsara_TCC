# O que fiz, para não esquecer

1. Instalei a pip `psycopg2-binary` porque o `psycopg2` precisa de `pg_config` antes de rodar o pip install. Já o `psycopg2-binary` já vem pré-compilado;

Qual usam em produção?
- A mais tradicional é `psycopg2` e instalando as dependências do PostgreSQL no container.
- Porém hoje em dia em microsserviços, containers Docker e aplicações web comuns, usam mais a `psycopg2-binary`.
	- Para a maioria dos projetos com Docker, usar `psycopg2-binary` é perfeitamente aceitável e simplifica bastante o build. Só tendo o cuidado de manter tudo atualizado.

2. Fiz o Dockerfile da imagem python usando alpine
- Para rodar o `flask db upgrade` e `main.py` fiz um script `.sh`. 
	- Toda vez que subir o container vai dar os dois comandos em ordem, mas não tem muito problema dar `db upgrade` toda vez
	> (talvez tentar otimizar isso depois)

3. docker-compose.yml que faz o container do postgresql e do python dockerfile
- O primeiro container é o `db`, com `postgresql alpine`, `environment` puxando as variaveis de ambiente do `.env` e um `healthcheck` para garantir que o banco suba antes do web e de um sinal de que o web pode subir (assim não da erro do `flask db upgrade` e tals)
- O segundo é o `web`, criando a imagem python a partir do `Dockerfile`, puxando as variaveis do `.env`, inciando só depois do `db` graças ao `depends_on service_healthy`


## Coisas:

1. host do flask
- no `main.py` é necessário colocar `app.run(host="0.0.0.0", port=5000, debug=True)` pois o flask só mapeia o localhost por padrão, então quando subir o docker não será possível acessar a porta do flask no navegador do windows, só dentro do cointainer, por isso o host 0.0.0.0

2. .env limpo e lógica no app/config.py
- inicialmente o .env era assim:
```
POSTGRES_USER=usuario_teste
POSTGRES_PASSWORD=minha_senha
POSTGRES_DB=samsara_db

DATABASE_URL=postgresql://usuario_teste:minha_senha@db:5432/samsara_db
```
> repetindo as coisas no DATABASE_URL e sem muita facilidade para alterar bancos.

- surge então a ideia de deixar o .env assim:
```
POSTGRES_USER=usuario_teste
POSTGRES_PASSWORD=minha_senha
POSTGRES_DB=samsara_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
> só variáveis do postgresql

- e o `àpp/config.py` com uma lógica de conectar no postgresql ou no sqlite (ou qualquer banco), ficando assim:
```python
import os
from dotenv import load_dotenv

load_dotenv(".env")

class Config:
	user = os.getenv("POSTGRES_USER")
	password = os.getenv("POSTGRES_PASSWORD")
	host = os.getenv("POSTGRES_HOST")
	port = os.getenv("POSTGRES_PORT", "5432")
	db_name = os.getenv("POSTGRES_DB")

	if user:
		SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
	else:
		SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database.db"
```

3. LOUCURA

1. por que atualizar o apk no RUN

2. lógica disso: 
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /usr/src/app && \
    chmod +x teste.sh
USER appuser

3. restart: unless-stopped FOI
por que tem que ter & qual a lógica disso também

4. start_period (grace period) do healthcheck FOI
por que o qual a logica também

5. driver: bridge do networks

6. rota health no 5000/ do healthcheck