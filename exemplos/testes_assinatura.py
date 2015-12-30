# coding=utf-8
# ---------------------------------------------------------------
# Desenvolvedor:    Arannã Sousa Santos
# Mês:              12
# Ano:              2015
# Projeto:          pagseguro_xml
# e-mail:           asousas@live.com
# ---------------------------------------------------------------

import logging

from pagseguro_xml.assinatura import ApiPagSeguroAssinatura_v2, CONST_v2

logger = logging.basicConfig(level=logging.DEBUG)


PAGSEGURO_API_AMBIENTE = u'sandbox'
PAGSEGURO_API_EMAIL = u'seu@email.com'
PAGSEGURO_API_TOKEN_PRODUCAO = u''
PAGSEGURO_API_TOKEN_SANDBOX = u''

api = ApiPagSeguroAssinatura_v2(ambiente=CONST_v2.AMBIENTE.SANDBOX)

PAGSEGURO_API_TOKEN = PAGSEGURO_API_TOKEN_SANDBOX


def exemploRequisicaoAssinatura():

    from pagseguro_xml.assinatura.v2.classes.requisicao import ClasseAssinaturaRequisicao, CONST as CONST_REQUISICAO

    xmlRequisicao = ClasseAssinaturaRequisicao()

    xmlRequisicao.redirectURL.valor = u'http://seusite.com.br'
    xmlRequisicao.reference.valor = u'REF0002'

    xmlRequisicao.sender.name.valor = u'Cliente de teste'
    xmlRequisicao.sender.email.valor = u'as1234231234e@sandbox.pagseguro.com.br'

    xmlRequisicao.sender.address.state.valor = u'TO'

    xmlRequisicao.preApproval.charge.valor = CONST_REQUISICAO.PREAPPROVAL.CHARGE.AUTO
    xmlRequisicao.preApproval.name.valor = u'Assinatura de 1 mes'
    xmlRequisicao.preApproval.amountPerPayment.valor = u'10.00'
    xmlRequisicao.preApproval.period.valor = CONST_REQUISICAO.PREAPPROVAL.PERIOD.MONTHLY
    from datetime import datetime
    xmlRequisicao.preApproval.finalDate.valor = datetime(2016, 01, 23)
    xmlRequisicao.preApproval.maxTotalAmount.valor = u'10.00'

    if xmlRequisicao.alertas:
        print u'erros antes de enviar'
        for a in xmlRequisicao.alertas:
            print a

    if not xmlRequisicao.alertas:

        ok, retorno = api.requisicao_assinatura_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, xmlRequisicao)

        if ok:

            print u'-' * 45, u'RESPOSTA', u'-' * 45
            # visualizando o XML retornado
            print retorno.xml
            print u'-' * 100

            # checando erros no XML retornado
            if retorno.alertas:

                print u'-' * 45, u'ALERTAS', u'-' * 46

                for a in retorno.alertas:
                    print a

                print u'-' * 100

            CODIGO_REQUISICAO_PAGAMENTO = retorno.code.valor

            url_fluxo = api.gera_url_fluxo_v2(CODIGO_REQUISICAO_PAGAMENTO)
            # >> u'https://[sandbox.]pagseguro.uol.com.br/v2/pre-approvals/request.html?code=CODIGO-RETORNADO'

            print u'URL para o fluxo:', url_fluxo

            # --------------------------------------------------------------------------------
            # no final do pagamento, a PagSeguro vai gerar a URL como a de baixo
            #
            # u'http://seusite.com.br/?code=CODIGO-NOTIFICACAO'
            # --------------------------------------------------------------------------------

        else:

            if hasattr(retorno, u'xml'):
                print u'Motivo do erro:', retorno.xml
            else:
                print u'Motivo do erro:', retorno


def exemploConsultaAssinaturaNotificacao():
    CODIGO_NOTIFICACAO = u''

    ok, retorno = api.consulta_assinatura_notificacao_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, CODIGO_NOTIFICACAO)

    if ok:

        print u'-' * 45, u'RESPOSTA', u'-' * 45

        # visualizando o XML retornado
        print retorno.xml

        print u'-' * 100

        print u'Status da Assinatura', retorno.status.valor

        # checando erros no XML retornado
        if retorno.alertas:

            print u'-' * 45, u'ALERTAS', u'-' * 46

            for a in retorno.alertas:
                print a

            print u'-' * 100

    else:
        print u'Motivo do erro:', retorno

def exemploConsultaAssinatura():
    # CODIGO_ASSINATURA = u''
    CODIGO_ASSINATURA = u''

    ok, retorno = api.consulta_assinatura_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, CODIGO_ASSINATURA)

    if ok:

        print u'-' * 45, u'RESPOSTA', u'-' * 45

        # visualizando o XML retornado
        print retorno.xml

        print u'-' * 100

        print u'Status da Assinatura', retorno.status.valor

        # checando erros no XML retornado
        if retorno.alertas:

            print u'-' * 45, u'ALERTAS', u'-' * 46

            for a in retorno.alertas:
                print a

            print u'-' * 100

    else:
        print u'Motivo do erro:', retorno

def exemploConsultaNotificacaoPorDias():

    ok, retorno = api.consulta_notificacao_por_dias_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, 30)

    if ok:

        print u'-' * 50
        print retorno.xml
        print u'-' * 50

        for preApproval in retorno.preApprovals:
            print preApproval.xml

        for a in retorno.alertas:
            print a

    else:
        if type(retorno) in (str, unicode, basestring):
            print u'Motivo do erro:', retorno
        else:
            print u'Motivo do erro:', retorno.xml

def exemploConsultaPorData():
    from datetime import datetime

    inicial = datetime(2015, 12, 9)
    final = datetime(2015, 12, 12)

    ok, retorno = api.consulta_por_data_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, inicial, final)

    if ok:

        print u'-' * 50
        print retorno.xml
        print u'-' * 50

        for preApproval in retorno.preApprovals:
            print preApproval.xml

        for a in retorno.alertas:
            print a

    else:
        if type(retorno) in (str, unicode, basestring):
            print u'Motivo do erro:', retorno
        else:
            print u'Motivo do erro:', retorno.xml

def exemploCancelar():

    codigo = u''
    # codigo = u''

    ok, retorno = api.cancela_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, codigo)

    if ok:

        print u'-' * 50
        print retorno.xml
        print u'-' * 50

        for a in retorno.alertas:
            print a

    else:
        if type(retorno) in (str, unicode, basestring):
            print u'Motivo do erro:', retorno
        else:
            print u'Motivo do erro:', retorno.xml

print u'#' * 50
exemploRequisicaoAssinatura()
print u'*' * 50
exemploConsultaAssinaturaNotificacao()
print u'*' * 50
exemploConsultaAssinatura()
print u'*' * 50
exemploConsultaNotificacaoPorDias()
print u'*' * 50
exemploConsultaPorData()
print u'*' * 50
exemploCancelar()
print u'#' * 50