from apscheduler.schedulers.background import BackgroundScheduler
from app.financeiro.notificacoes import verificar_vencimentos

def iniciar_agendador(app):
        scheduler = BackgroundScheduler()

        scheduler.add_job(
            func=verificar_vencimentos,
            trigger="interval",
            minutes=1,
            args=[app]
        )

        scheduler.start()