from app import app, BancoDeDados
from flask import render_template, url_for, request, redirect, flash

from app.models import LancamentoFinanceiro, Produto, Fornecedor
from app.forms import LancamentoForm, LoginForm
from app.models import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import make_response
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Email ou senha inválidos', 'PRERIGU')

    return render_template('login.html', form=form)

@app.route('/register')
def register():
    hashed = bcrypt.generate_password_hash('123456').decode('utf-8')

    user = User(email='teste@email.com', password=hashed)

    BancoDeDados.session.add(user)
    BancoDeDados.session.commit()

    return "Usuário criado!"

@app.route('/home/')
def homepage():

    return render_template('index.html')

@app.route('/seed/')
def seed():
    from app.models import Produto, Fornecedor

    BancoDeDados.session.add(Produto(nome="Bebida"))
    BancoDeDados.session.add(Produto(nome="Cigarro"))
    BancoDeDados.session.add(Fornecedor(nome="Coca Cola"))
    BancoDeDados.session.add(Fornecedor(nome="Phillip Morris"))

    BancoDeDados.session.commit()

    return "Dados inseridos!"

# Criar Lançamentos Financeiros 
@app.route('/lancamento/novo', methods=['GET', 'POST'])
def novo_lancamento():
    form = LancamentoForm()

    form.produto.choices = [(p.id, p.nome) for p in Produto.query.all()]
    form.fornecedor.choices = [(f.id, f.nome) for f in Fornecedor.query.all()]

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('listar_lancamento'))

    return render_template('lancamento_form.html', form=form)

# Listar
@app.route('/lancamentos')
def listar_lancamento():
    lancamentos = LancamentoFinanceiro.query.all()
    return render_template('lancamento_lista.html', lancamentos=lancamentos)

# Editar
@app.route('/lancamento/<int:id>/editar', methods=['GET', 'POST'])
def editar_lancamento(id):
    lancamento = LancamentoFinanceiro.query.get_or_404(id)
    form = LancamentoForm(obj=lancamento)

    form.produto.choices = [(p.id, p.nome) for p in Produto.query.all()]
    form.fornecedor.choices = [(f.id, f.nome) for f in Fornecedor.query.all()]

    if form.validate_on_submit():
        lancamento.produto_id = form.produto.data
        lancamento.fornecedor_id = form.fornecedor.data
        lancamento.tipo_custo = form.tipo_custo.data
        lancamento.conta_origem = form.conta_origem.data
        lancamento.forma_pagamento = form.forma_pagamento.data
        lancamento.status = form.status.data
        lancamento.valor = form.valor.data

        BancoDeDados.session.commit()
        return redirect(url_for('listar_lancamento'))

    return render_template('lancamento_form.html', form=form)

# Deletar
@app.route('/lancamento/<int:id>/deletar', methods=['POST'])
def deletar_lancamento(id):
    lancamento = LancamentoFinanceiro.query.get_or_404(id)

    BancoDeDados.session.delete(lancamento)
    BancoDeDados.session.commit()

    return redirect(url_for('listar_lancamento'))

@app.route('/agenda/')
def agenda():

    return render_template('agenda.html')

@app.route('/relatorios')
def relatorios():

    return render_template('relatorios.html')

@app.route('/relatorio/<int:mes>')
def gerar_relatorio(mes):

    lancamentos = LancamentoFinanceiro.query.filter(
        BancoDeDados.extract('month', LancamentoFinanceiro.data) == mes
    ).all()

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Relatório Financeiro")

    # TÍTULO
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "Relatório Financeiro")

    # TEXO
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 760, "Para:")
    pdf.drawString(50, 740, "Cliente Exemplo")
    pdf.drawString(50, 720, "Empresa Exemplo")

    pdf.drawString(50, 680, "De:")
    pdf.drawString(50, 660, "Samsara")

    pdf.drawString(50, 620, f"Data de emissão: {datetime.now().strftime('%d/%m/%Y')}")

    pdf.drawString(50, 580, "Sumário:")
    pdf.drawString(
        50,
        560,
        "Este relatório apresenta o faturamento total do período."
    )

    # LISTA DE LANÇAMENTOS
    altura = 500

    total = 0

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, altura, "Vendas Realizadas:")

    altura -= 30

    pdf.setFont("Helvetica", 12)

    for l in lancamentos:

        texto = f"{l.produto.nome} - R$ {l.valor}"

        pdf.drawString(60, altura, texto)

        altura -= 20

        total += float(l.valor)

    # TOTAL
    altura -= 20

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, altura, f"Total do mês: R$ {total:.2f}")

    pdf.save()

    buffer.seek(0)

    response = make_response(buffer.getvalue())

    response.headers['Content-Type'] = 'application/pdf'

    response.headers['Content-Disposition'] = (
        f'inline; filename=relatorio_mes_{mes}.pdf'
    )

    return response