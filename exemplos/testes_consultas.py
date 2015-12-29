# coding=utf-8
# ---------------------------------------------------------------
# Desenvolvedor:    Arannã Sousa Santos
# Mês:              12
# Ano:              2015
# Projeto:          pagseguro_xml
# e-mail:           asousas@live.com
# ---------------------------------------------------------------

import logging
from pagseguro_xml.consultas import ApiPagSeguroConsulta_v3, CONST_v3

logger = logging.basicConfig(level=logging.DEBUG)


PAGSEGURO_API_AMBIENTE = u'sandbox'
PAGSEGURO_API_EMAIL = u'seu@email.com'
PAGSEGURO_API_TOKEN_PRODUCAO = u''
PAGSEGURO_API_TOKEN_SANDBOX = u''


api = ApiPagSeguroConsulta_v3(ambiente=CONST_v3.AMBIENTE.SANDBOX)
PAGSEGURO_API_TOKEN = PAGSEGURO_API_TOKEN_SANDBOX


CHAVE_TRANSACAO = u''       # primeiro teste
# CHAVE_TRANSACAO = u''     # segundo teste


def exemploDetalhes():
    # retorno pode ser uma mensagem ou a Classe que representa
    # os Detalhes [pagseguro_xml.consultas.classes.ClasseTransacaoDetalhes]
    ok, retorno = api.detalhes_v3(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, CHAVE_TRANSACAO)

    if ok:

        print u'-' * 50
        print retorno.xml
        print u'-' * 50

        for a in retorno.alertas:
            print a

    else:
        print u'Motivo do erro:', retorno


def exemploHistorico():
    from datetime import datetime

    inicial = datetime(2015, 12, 9)
    final = datetime(2015, 12, 12)

    ok, retorno = api.historico_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, inicial, final)

    if ok:

        print u'-' * 50
        print retorno.xml
        print u'-' * 50

        for i, transacao in enumerate(retorno.transactions, start=1):
            print transacao.xml

        for a in retorno.alertas:
            print a

    else:
        print u'Motivo do erro:', retorno


def exemploAbandonadas():
    from datetime import datetime

    inicial = datetime(2015, 12, 9)
    final = datetime(2015, 12, 12)

    ok, retorno = api.abandonadas_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, inicial, final)

    if ok:

        print u'-' * 50
        print retorno.xml
        print u'-' * 50

        for transacao in retorno.transactions:
            print transacao.xml

        for a in retorno.alertas:
            print a

    else:
        print u'Motivo do erro:', retorno

print u'#' * 50
exemploDetalhes()
print u'*' * 50
exemploHistorico()
print u'*' * 50
exemploAbandonadas()
print u'#' * 50