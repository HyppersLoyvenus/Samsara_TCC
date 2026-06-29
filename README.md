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

   Windows:
   ```sh
   copy .env.example .env
   ```
   Linux/MacOS:
   ```sh
   cp .env.example .env
   ```
   1.1 se necessário, abrir o arquivo `.env` recém criado e verificar se os campos abaixo estão preenchidos (se não, preencher):
   ```env
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   ```

3. Subir a aplicação com Docker Compose:
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

   Windows:
   ```sh
   copy .env.example .env
   ```
   Linux/MacOS:
   ```sh
   cp .env.example .env
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
O projeto segue o padrão arquitetural **MVC (Model, View, Controller)** adaptado para o Flask através do uso de **Blueprints**:

```text
Samsara_TCC/
├── app/                  # Diretório principal da aplicação
│   ├── auth/             # Módulo de autenticação (rotas e lógica para: cadastro, login e logout de usuários)
│   ├── financeiro/       # Módulo financeiro (cobre toda a parte de: dashboard, lançamentos, agenda, relatórios e alertas)
│   ├── main/             # Módulo raiz (rota base / e perfil de usuário)
│   ├── static/           # Arquivos estáticos (CSS, imagens e ícones)
│   ├── templates/        # Telas da aplicação (HTML utilizando Jinja2)
│   ├── utils/            # Classes auxiliares (formatação de texto e valores)
│   ├── config.py         # Parâmetros globais para a configuração da aplicação
│   ├── extensions.py     # Gerenciamento e inicialização das bibliotecas externas
│   ├── models.py         # Modelagem do banco de dados (SQLAlchemy)
│   └── __init__.py       # Configuração da application factory (create_app)
├── migrations/           # Versionamento da estrutura do banco de dados
├── .env.example          # Modelo das variáveis de ambiente
├── docker-compose.yml    # Orquestrador dos serviços (Nginx, Flask, PostgreSQL)
├── Dockerfile            # Configuração da imagem Python do backend
├── main.py               # Ponto de entrada para execução da aplicação
├── nginx.conf            # Configuração do proxy reverso e servidor de estáticos
├── requirements.txt      # Bibliotecas do ecossistema Python necessárias
└── setup_up.sh           # Script de inicialização automatizada
```

## Como enviar um alerta de teste <a name="enviar-alerta-teste"></a>
