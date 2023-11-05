import json
import scrapy

class TJCEScrapper(scrapy.Spider):
    name = 'tjalcrapper'

    def __init__(self, numero_processo='', **kwargs):
        self.start_urls = [f'https://www2.tjal.jus.br/cpopg/show.do?processo.numero={numero_processo}']
        super().__init__(**kwargs)
        
    def parse(self, response):
        participantes = []
        movimentacoes = []
        tabela = response.css('#tablePartesPrincipais')
        linhas = tabela.css('tr')
        for linha in linhas:
            tipo_participacao = linha.css('.tipoDeParticipacao::text').get()
            nome_parte = linha.css('.nomeParteEAdvogado::text').get()

            if tipo_participacao and nome_parte:
                tipo_participacao = tipo_participacao.strip()
                nome_parte = nome_parte.strip()

                participante = {
                    'tipo_participacao': tipo_participacao,
                    'nome_parte': nome_parte
                }

                participantes.append(participante)
        tabela_movimentacoes = response.css('#tabelaTodasMovimentacoes')
        linhas_movimentacoes = tabela_movimentacoes.css('tr')
        for linha_movimentacao in linhas_movimentacoes:
            data_movimentacao = linha_movimentacao.css('.dataMovimentacao::text').get()
            descricao_movimentacao = linha_movimentacao.css('.descricaoMovimentacao::text').get()

            if data_movimentacao and descricao_movimentacao:
                data_movimentacao = data_movimentacao.strip()
                descricao_movimentacao = descricao_movimentacao.strip()

                participante = {
                    'data_movimentacao': data_movimentacao,
                    'descricao_movimentacao': descricao_movimentacao
                }

                movimentacoes.append(participante)
        
        yield {
            'classe' :response.css('span#classeProcesso::text').get(),
            'area' :response.css('#areaProcesso span::text').get(),
            'assunto' :response.css('#assuntoProcesso::text').get(),
            'data_de_distribuicao' :response.css('#dataHoraDistribuicaoProcesso::text').get(),
            'juiz' :response.css('#juizProcesso::text').get(),
            'valor_da_acao' :response.css('#valorAcaoProcesso::text').get(),
            'partes_do_processo' :participantes,
            'lista_das_movimentacoes' :movimentacoes,
        }

