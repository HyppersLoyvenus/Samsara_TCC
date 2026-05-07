from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, PasswordField
from wtforms.validators import DataRequired, Email
from app import BancoDeDados
from app.models import LancamentoFinanceiro, Produto, Fornecedor

class LancamentoForm(FlaskForm):
    produto = SelectField('Produto', coerce=int, validators=[DataRequired()])
    fornecedor = SelectField('Fornecedor', coerce=int, validators=[DataRequired()])

    tipo_custo = SelectField(
        'Tipo de Custo',
        choices=[('Fixo', 'Fixo'), ('Variável', 'Variável')],
        validators=[DataRequired()]
    )
    conta_origem = SelectField(
        'Conta de Origem',
        choices=[('Dinheiro', 'Dinheiro'), ('Stone', 'Stone'), ('Itaú', 'Itaú')],
        validators=[DataRequired()]
    )
    forma_pagamento = SelectField(
        'Forma de Pagamento',
        choices=[('Pix', 'Pix'), ('Boleto', 'Boleto'), ('Débito', 'Débito')],
        validators=[DataRequired()]
    )
    status = SelectField(
        'Status',
        choices=[('Pendente', 'Pendente'), ('Pago', 'Pago')],
        validators=[DataRequired()]
    )
    valor = DecimalField('Valor (R$)', places=2, validators=[DataRequired()])
    btnSubmit = SubmitField('Registrar')

    def save(self):
        lancamento = LancamentoFinanceiro(
            produto_id=self.produto.data,
            fornecedor_id=self.fornecedor.data,
            tipo_custo=self.tipo_custo.data,
            conta_origem=self.conta_origem.data,
            forma_pagamento=self.forma_pagamento.data,
            status=self.status.data,
            valor=self.valor.data
        )
        BancoDeDados.session.add(lancamento)
        BancoDeDados.session.commit()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

    def save(self):
        login = LoginForm(
            email=self.email.data,
            password=self.password.data,

        )
        BancoDeDados.session.add(login)
        BancoDeDados.session.commit()