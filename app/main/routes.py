from flask import current_app, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text

from app.extensions import db
from app.main import main_bp


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("financeiro.dashboard"))

    return redirect(url_for("auth.login"))


@main_bp.route("/perfil/")
@login_required
def perfil():
    return render_template("main/perfil.html")


@main_bp.get("/health")
def health():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        current_app.logger.exception("Healthcheck failed")
        return {"status": "unhealthy"}, 503

    return {"status": "ok"}, 200
