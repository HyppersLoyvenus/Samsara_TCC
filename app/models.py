from app import BancoDeDados
from datetime import datetime, timezone

class Produto(BancoDeDados.Model):
    id = BancoDeDados.Column(BancoDeDados.Integer, primary_key=True)
    nome = BancoDeDados.Column(BancoDeDados.String(100), nullable=False, unique=True)

    lancamentos = BancoDeDados.relationship('LancamentoFinanceiro', backref='produto_ref')

class Fornecedor(BancoDeDados.Model):
    id = BancoDeDados.Column(BancoDeDados.Integer, primary_key=True)
    nome = BancoDeDados.Column(BancoDeDados.String(100), nullable=False, unique=True)

    lancamentos = BancoDeDados.relationship('LancamentoFinanceiro', backref='fornecedor_ref')
    
class LancamentoFinanceiro(BancoDeDados.Model):

    id = BancoDeDados.Column(BancoDeDados.Integer, primary_key=True)
    data = BancoDeDados.Column(BancoDeDados.DateTime, default=datetime.now(timezone.utc))

    produto_id = BancoDeDados.Column(
        BancoDeDados.Integer,
        BancoDeDados.ForeignKey('produto.id'),
        nullable=False
    )
    fornecedor_id = BancoDeDados.Column(
        BancoDeDados.Integer,
        BancoDeDados.ForeignKey('fornecedor.id'),
        nullable=False
    )
    tipo_custo = BancoDeDados.Column(BancoDeDados.String(50), nullable=False)
    conta_origem = BancoDeDados.Column(BancoDeDados.String(50), nullable=False)
    forma_pagamento = BancoDeDados.Column(BancoDeDados.String(50), nullable=False)
    status = BancoDeDados.Column(BancoDeDados.String(20), default="Pendente")
    valor = BancoDeDados.Column(BancoDeDados.Numeric(10, 2), nullable=False)

    produto = BancoDeDados.relationship('Produto')
    fornecedor = BancoDeDados.relationship('Fornecedor')

class User(BancoDeDados.Model):
    id = BancoDeDados.Column(BancoDeDados.Integer, primary_key=True)
    email = BancoDeDados.Column(BancoDeDados.String(120), unique=True, nullable=False)
    password = BancoDeDados.Column(BancoDeDados.String(255), nullable=False)