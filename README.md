# Samsara - Agenda Financeira

Um sistema que serve como uma agenda para acompanhar despesas financeiras e enviar alertas automatizados por e-mail.
## Pré-Requisitos
* [Docker](https://www.docker.com/get-started/) instalado e rodando.
* [Python](https://www.python.org/downloads/) (3.14 ou superior) caso queira subir sem docker.
* Arquivo `.env` configurado na raiz do projeto com as variáveis de ambiente preenchidas corretamente.

## Sumário
1. [Instalação & Execução](#instalacao-execucao)
2. [Estrutura do projeto](#estrutura-projeto)
3. [Como enviar um alerta de teste](#enviar-alerta-teste)

## Instalação & Execução <a name="instalacao-execucao"></a>
### **Via Docker**

1. Criar o arquivo `.env` na raiz do projeto copiando o `.env.example`:
   ```sh
   copy .env.example .env
   ```
   1.1 se necessário, abrir o arquivo `.env` recém criado e preencher os campos abaixo:
   ```env
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   POSTGRES_HOST=
   POSTGRES_PORT=
   ```

2. Subir a aplicação com Docker Compose:
   ```sh
   docker compose up --build -d
   ```
   > Aplicação estará disponível em: http://localhost:80

### **Via Python (manualmente)**

1. Criar, acessar e ativar o ambiente virtual Python:
   ```sh
   python -m venv .venv
   cd .venv/Scripts
   activate
   cd ../..
   ```
   > obs: este processo só funciona pelo cmd

2. Instalar as bibliotecas:
   ```sh
   python -m pip install -r requirements.txt
   ```

3. Criar o arquivo `.env` na raiz do projeto copiando o `.env.example`:
   ```sh
   copy .env.example .env
   ```
   3.1 no `.env` descomentar a linha 8 e adicionar:
   ```env
   DATABASE_URL=sqlite:///database.db
   ```
   > para usar o sqlite ao invés do postgresql

4. Aplicar as migrations do banco:
    ```sh
    flask db upgrade
    ```

5. Subir a aplicação:
    ```sh
    python main.py
    ```
    > Aplicação estará disponível em: http://localhost:5000

## Estrutura do projeto <a name="estrutura-projeto"></a>

## Como enviar um alerta de teste <a name="enviar-alerta-teste"></a>
