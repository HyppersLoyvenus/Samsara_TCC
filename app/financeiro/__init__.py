from flask import Blueprint #init

financeiro_bp = Blueprint("financeiro", __name__, url_prefix="/financeiro")

from app.financeiro import routes