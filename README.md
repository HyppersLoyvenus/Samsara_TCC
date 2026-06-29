# Samsara - Agenda Financeira

Um sistema web que serve como uma agenda para acompanhar despesas financeiras, gerar relatórios e enviar alertas automatizados por e-mail de contas a vencer.
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

1. Crie o arquivo `.env` na raiz do projeto copiando o `.env.example`:
   ```sh
   # No Windows:
   copy .env.example .env
   
   # No Linux / macOS:
   cp .env.example .env
   ```
   1.1 se necessário, abra o arquivo `.env` recém criado e verefique se os campos abaixo estão preenchidos (se não, preencher):
   ```env
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   ```

3. Suba a infraestrutura orchestrada com Docker Compose:
   ```sh
   docker compose up --build -d
   ```
   > obs: o ecossistema possui healthchecks inteligentes. O flask aguardará o postgresql iniciar, aplicará as migrações automaticamente (flask db upgrade) e o nginx liberará o acesso.
   * Aplicação estará disponível em: http://localhost (porta 80)

### **Via Python (manualmente)**

1. Crie, acesse e ative o ambiente virtual Python:
   ```sh
   python -m venv .venv
   cd .venv/Scripts
   activate
   cd ../..
   ```
   > obs: este processo de ativação específico acima só funciona pelo cmd

2. Instale as dependências do projeto:
   ```sh
   python -m pip install -r requirements.txt
   ```

3. Crie o arquivo `.env` na raiz do projeto copiando o `.env.example`:
   ```sh
   # No Windows:
   copy .env.example .env
   
   # No Linux / macOS:
   cp .env.example .env
   ```
   3.1 No arquivo `.env`, descomente a linha do `DATABASE_URL` para apontar para o SQLite local:
   ```env
   DATABASE_URL=sqlite:///database.db
   ```
   > isso faz com que o flask ignore as variáveis do postgresql e inicialize o banco de dados em arquivo local.

4. Aplique as migrações para estruturar o banco de dados:
    ```sh
    flask db upgrade
    ```

5. Inicie o servidor de desenvolvimento do Flask:
    ```sh
    python main.py
    ```
   * A aplicação estará disponível em: http://localhost:5000

## Estrutura do projeto <a name="estrutura-projeto"></a>
O projeto segue o padrão arquitetural **MVC (Model, View, Controller)** adaptado para o Flask através do uso de **Blueprints**, separando claramente as responsabilidades de cada módulo:

```text
Samsara_TCC/
├── app/                  # Diretório principal da aplicação
│   ├── auth/             # Módulo de autenticação (rotas e lógica para: cadastro, login e logout)
│   ├── financeiro/       # Módulo financeiro (dashboard, lançamentos, agenda, relatórios e alertas)
│   ├── main/             # Módulo raiz (rota base / e perfil de usuário)
│   ├── static/           # Arquivos estáticos (CSS, imagens e ícones)
│   ├── templates/        # Telas da aplicação (HTML utilizando Jinja2)
│   ├── utils/            # Classes auxiliares (formatação de texto, datas e valores)
│   ├── config.py         # Parâmetros globais para a configuração e inicialização do app
│   ├── extensions.py     # Gerenciamento e inicialização das bibliotecas externas
│   ├── models.py         # Modelagem do banco de dados (SQLAlchemy)
│   └── __init__.py       # Configuração da application factory (create_app)
├── migrations/           # Histórico de versionamento e evolução estrutural do banco de dados
├── .env.example          # Modelo das variáveis de ambiente
├── docker-compose.yml    # Orquestrador dos serviços (Nginx, Flask, PostgreSQL)
├── Dockerfile            # Configuração da imagem Python do backend
├── main.py               # Ponto de entrada oficial para execução da aplicação
├── nginx.conf            # Configuração do proxy reverso e servidor de estáticos
├── requirements.txt      # Bibliotecas e dependências do ecossistema Python necessárias
└── setup_up.sh           # Script de inicialização automatizada
```

## Como enviar um alerta de teste <a name="enviar-alerta-teste"></a>
1. No arquivo `.env` edite as seguintes linhas para configurar o serviço de e-mail:
   ```env
   MAIL_USERNAME=
   MAIL_PASSWORD=
   MAIL_DEFAULT_SENDER=
   ```
   * Coloque em `MAIL_USERNAME` & `MAIL_DEFAULT_SENDER` o endereço de e-mail que será responsável por disparar as notificações.
   * Em `MAIL_PASSWORD` insira uma **Senha de App do Google**. Para criá-la:
      * Acesse as configurações de "gerenciar sua conta google" do e-mail remetente;
      * Ative a "verificação em duas etapas" (caso não esteja ativa);
      * Pesquise na barra de busca por "senhas de app" e acesse;
      * Dê um nome ao aplicativo (ex: Samsara TCC) e clique em criar;
      * Copie a senha de 16 letras gerada, remova os espaços, e cole em `MAIL_PASSWORD`.
   > obs: após salvar o arquivo `.env`, lembre-se de reiniciar os containers ou o servidor local para que o sistema carregue as novas credenciais

2. Com a aplicação rodando, acesse a tela de cadastro e crie um usuário utilizando o e-mail destinatário (onde você deseja receber o alerta de teste).
3. Faça login com esse usuário, vá em lançamentos e crie uma despesa com o status **"pendente"** e coloque a data de vencimento para **amanhã**.
4. Acesse a aba Agenda e, no canto superior direito da tela, clique no botão "enviar alertas por email"

O sistema processará a fila de pendências em segundo plano e enviará a notificação. O resultado esperado na sua caixa de entrada do e-mail cadastrado será semelhante a este:

![Exemplo de alerta no e-mail](https://i.imgur.com/V8tRAaG.png)
