from datetime import date, timedelta

from app.models import LancamentoFinanceiro
from app.financeiro.email_service import enviar_email


def verificar_vencimentos(app):
    with app.app_context():
        amanha = date.today() + timedelta(days=1)

        lancamentos = LancamentoFinanceiro.query.filter_by(status="pendente", data_vencimento = amanha).all()

        for lancamento in lancamentos:
            usuario = lancamento.usuario

            mensagem = f"""
                Olá, {usuario.username}!

                Sua fatura no valor de R$ {lancamento.valor}
                vence amanhã.

                Favorecido: {lancamento.favorecido}

                Não esqueça do pagamento 
            """

            enviar_email(
                destinatario=usuario.email,
                assunto="Fatura próxima do vencimento",
                mensagem=mensagem
            )