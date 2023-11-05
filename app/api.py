from flask import request, jsonify
from app import app, db 

from app.models.solicitacoes import Solicitacoes 

@app.route('/cadastrar-numero-processo', methods=['POST'])
def cadastrar_processo():
    data = request.get_json()
    numero_processo = data.get('numero_processo')

    processo_existente = Solicitacoes.query.filter_by(id_solicitacao=numero_processo).first()
    if processo_existente:
        return jsonify({'message': 'Solicitação ja cadastrada'})

    novo_processo = Solicitacoes(id_solicitacao=numero_processo,
                                status_solicitacao= "SOLICITADA",

                                )
    db.session.add(novo_processo)
    db.session.commit()
    return jsonify({'message': 'Solicitação cadastrada com sucesso!'})

@app.route('/ler-processo/<numero>', methods=['GET'])
def ler_processo(numero):
    processo = Solicitacoes.query.filter_by(id_solicitacao=numero).first()
    if not processo:
        return jsonify({'message': 'Solicitação não encontrada'})

    if processo.status_solicitacao == "SOLICITADA":
        return jsonify({'message': f'A consulta do número do processo: {processo.id_solicitacao}, ainda está fila. Tente novamente em alguns instantes.'})
    dados_do_processo = {
        'id_solicitacao': processo.id_solicitacao,
        'result': processo.json_resposta,
    }
    return jsonify(dados_do_processo)

if __name__ == '__main__':
    app.run(debug=True)
