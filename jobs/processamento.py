import json
import os
import re
import subprocess
import sys
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.solicitacoes import Solicitacoes

from app import app
from app import db
from datetime import datetime

def consultar_solicitacoes_solicitadas():
    with app.app_context():
        solicitacoes = Solicitacoes.query.filter_by(status_solicitacao='SOLICITADA').all()
        return solicitacoes

def executa_scrapy(estado, numero_processo, grau):
    try:
        if estado == "ce":
            data = None
            if grau == 1: 
                current_directory = os.path.dirname(os.path.abspath(__file__))
                route_script = os.path.join(current_directory, '..', 'app', 'utils', 'tj_crawler', 'tj_crawler', 'spiders', 'tjce_scrapper.py')

                subprocess.run(['scrapy', 'runspider', route_script, '-a', f'numero_processo={numero_processo}', '-o', 'output.json'])
                with open('./output.json', 'r') as file:
                    data = json.load(file)
                os.remove('./output.json')
            else:
                current_directory = os.path.dirname(os.path.abspath(__file__))
                route_script = os.path.join(current_directory, '..', 'app', 'utils', 'tj_crawler', 'tj_crawler', 'spiders', 'tjce_scrapper_2.py')

                subprocess.run(['scrapy', 'runspider', route_script, '-a', f'numero_processo={numero_processo}', '-o', 'output.json'])
                with open('./output.json', 'r') as file:
                    data = json.load(file)
                os.remove('./output.json')

            return data
        elif estado == "al":
            data = None
            if grau == 1: 
                current_directory = os.path.dirname(os.path.abspath(__file__))
                route_script = os.path.join(current_directory, '..', 'app', 'utils', 'tj_crawler', 'tj_crawler', 'spiders', 'tjal_scrapper.py')

                subprocess.run(['scrapy', 'runspider', route_script, '-a', f'numero_processo={numero_processo}', '-o', 'output.json'])
                with open('./output.json', 'r') as file:
                    data = json.load(file)
                os.remove('./output.json')
            else:
                current_directory = os.path.dirname(os.path.abspath(__file__))
                route_script = os.path.join(current_directory, '..', 'app', 'utils', 'tj_crawler', 'tj_crawler', 'spiders', 'tjal_scrapper_2.py')

                subprocess.run(['scrapy', 'runspider', route_script, '-a', f'numero_processo={numero_processo}', '-o', 'output.json'])
                with open('./output.json', 'r') as file:
                    data = json.load(file)
                os.remove('./output.json')

            return data

    except Exception as e:
        print("Erro ao executar crawler", e)

def identificar_estado(numero_processo):

    regex_num_processo = r'^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$'

    if re.match(regex_num_processo, numero_processo):
        codigo_tribunal = numero_processo.split('.')[3] 

        if codigo_tribunal == '06':
            return "ce"
        if codigo_tribunal == '02':
            return "al"
        
        raise ValueError('Tribunal não identificado')
        
    raise ValueError('Formato de número de processo inválido')



def processar_solucitacao(numero_processo, solicitacao):
    with app.app_context():
        solicitacao = Solicitacoes.query.filter_by(id_solicitacao=numero_processo).first()
        if solicitacao:
            solicitacao.status_solicitacao = "EM ANDAMENTO"
            db.session.commit()
        try:
            estado = identificar_estado(numero_processo)
            resultados = {}
            resultados.update({'grau_1': executa_scrapy(estado, numero_processo, 1)})
            resultados.update({'grau_2': executa_scrapy(estado, numero_processo, 2)})

            with app.app_context():
                solicitacao = Solicitacoes.query.filter_by(id_solicitacao=numero_processo).first()
                if solicitacao:
                    solicitacao.json_resposta = resultados
                    solicitacao.status_solicitacao = "FINALIZADA"
                    db.session.commit()
        except Exception as error:
            solicitacao.status_solicitacao = "ERRO"
            solicitacao.json_resposta = {'erro': str(error)}
            db.session.commit()
            print(error)


def executar_job():
    print("Iniciando o job...")

    solicitacoes = consultar_solicitacoes_solicitadas()

    if solicitacoes:
        print(f"Encontradas {len(solicitacoes)} solicitações 'SOLICITADA' para processar.")
        for solicitacao in solicitacoes:
            numero_processo = solicitacao.id_solicitacao
            print(f"Processando solicitação para o processo {numero_processo}...")
            resultado_crawler = processar_solucitacao(numero_processo, solicitacao)
    else:
        print("Nenhuma solicitação com o status 'SOLICITADA' para processar.")

    print("Job concluído.")
