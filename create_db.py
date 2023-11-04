from app import app, db
from app.models.solicitacoes import Solicitacoes

with app.app_context():
    db.create_all()