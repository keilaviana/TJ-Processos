import scrapy

class TJCEScrapper(scrapy.Spider):
    name = 'tjcecrapper2'
    allowed_domains = ['esaj.tjce.jus.br']

    def __init__(self, numero_processo='', **kwargs):
        super().__init__(**kwargs)
        partes_numero_processo = numero_processo.split('.')
        self.start_urls = [f'https://esaj.tjce.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={partes_numero_processo[0]}.{partes_numero_processo[1]}&foroNumeroUnificado={partes_numero_processo[3]}&dePesquisaNuUnificado={numero_processo}&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO']

    def parse(self, response):
        self.log(f'Resposta recebida do URL: {response.url}')
        valor_input = response.css('input#processoSelecionado::attr(value)').get()
        if valor_input:
            nova_url = f'https://esaj.tjce.jus.br/cposg5/show.do?processo.codigo={valor_input}'
            print('-----------------------------')
            print(nova_url)
            yield scrapy.Request(nova_url, callback=self.parse_nova_pagina)
        yield {}

    def parse_nova_pagina(self, response): 
        self.log(f'Resposta recebida do URL: {response.url}')
        movimentacoes = []
        participantes = []
        partes_ativas = response.css('#tablePartesPrincipais .fundoClaro.poloAtivo .nomeParteEAdvogado')
        partes_passivas = response.css('#tablePartesPrincipais .fundoClaro.poloPassivo .nomeParteEAdvogado')

        partes_ativas_texto = partes_ativas.css('::text').getall()
        partes_ativas_texto = [parte.replace('Advogado:&nbsp', '').strip() for parte in partes_ativas_texto if parte.strip()]

        partes_passivas_texto = partes_passivas.css('::text').getall()
        partes_passivas_texto = [parte.replace('Advogado:&nbsp', '').strip() for parte in partes_passivas_texto if parte.strip()]

        partes = {
            "partes_ativas": partes_ativas_texto,
            "partes_passivas": partes_passivas_texto,
        }

        participantes.append(partes)
        
        tabela_movimentacoes = response.css('#tabelaUltimasMovimentacoes .movimentacaoProcesso')
        linhas_movimentacoes = tabela_movimentacoes.css('tr')
        for linha_movimentacao in linhas_movimentacoes:
            data_movimentacao = linha_movimentacao.css('td.dataMovimentacaoProcesso::text').get()
            descricao_movimentacao = linha_movimentacao.css('td.descricaoMovimentacaoProcesso::text').get()

            if data_movimentacao and descricao_movimentacao:
                data_movimentacao = data_movimentacao.strip()
                descricao_movimentacao = descricao_movimentacao.strip()

                participante = {
                    'data_movimentacao': data_movimentacao,
                    'descricao_movimentacao': descricao_movimentacao
                }
                movimentacoes.append(participante)
        
        yield {
            'classe' :response.css('#classeProcesso span::text').get(),
            'area' :response.css('#areaProcesso span::text').get(),
            'assunto' :response.css('#assuntoProcesso span::text').get(),
            'data_de_distribuicao' :response.css('#dataHoraDistribuicaoProcesso::text').get(),
            'juiz' :response.css('#juizProcesso span::text').get(),
            'valor_da_acao' :response.css('#valorAcaoProcesso span::text').get(),
            'partes_do_processo' :participantes,
            'lista_das_movimentacoes' :movimentacoes,
        }