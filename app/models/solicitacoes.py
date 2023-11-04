from app import db

class Solicitacoes(db.Model):
    id_solicitacao = db.Column(db.Integer, primary_key=True)
    status_solicitacao = db.Column(db.String(50))
    json_resposta = db.Column(db.JSON)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    data_atualizacao = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())