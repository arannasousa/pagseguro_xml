# coding=utf-8
# ---------------------------------------------------------------
# Desenvolvedor:    Arannã Sousa Santos
# Mês:              12
# Ano:              2015
# Projeto:          pagseguro_xml
# e-mail:           asousas@live.com
# ---------------------------------------------------------------
import logging

from pagseguro_xml.pagamento import ApiPagSeguroConsulta_v2, CONST_v2

logger = logging.basicConfig(level=logging.DEBUG)


PAGSEGURO_API_AMBIENTE = u'sandbox'
PAGSEGURO_API_EMAIL = u'seu@email.com'
PAGSEGURO_API_TOKEN_PRODUCAO = u''
PAGSEGURO_API_TOKEN_SANDBOX = u''


api = ApiPagSeguroConsulta_v2(ambiente=CONST_v2.AMBIENTE.SANDBOX)
PAGSEGURO_API_TOKEN = PAGSEGURO_API_TOKEN_SANDBOX


def exemploCheckout():

    from pagseguro_xml.pagamento.v2.classes import ClassePagamentoCheckout, Item
    from pagseguro_xml.pagamento.v2.classes.pagamento import CONST as CONST_PAGAMENTO

    xmlRequisicao = ClassePagamentoCheckout()

    print u'Montando xml para checkout'

    xmlRequisicao.redirectURL.valor = u'http://seusite.com.br'
    xmlRequisicao.reference.valor = u'REF0002'

    # prazo maximo de validade do CODIGO_PAGAMENTO que será criado pela PagSeguro (5 minutos)
    xmlRequisicao.maxAge.valor = 5 * 60

    xmlRequisicao.sender.name.valor = u'Cliente de teste'
    xmlRequisicao.sender.email.valor = u'as1234231234e@sandbox.pagseguro.com.br'

    xmlRequisicao.sender.phone.areaCode.valor = u'63'
    xmlRequisicao.sender.phone.number.valor = u'92111111'

    xmlRequisicao.shipping.type.valor = CONST_PAGAMENTO.SHIPPING.TYPE.NAO_ESPECIFICADO
    xmlRequisicao.shipping.address.city.valor = u'Palmas'
    xmlRequisicao.shipping.address.state.valor = u'TO'
    xmlRequisicao.shipping.address.country.valor = u'BRA'     # valor default

    item1 = Item()
    item1.ID.valor = u'ITEM0001'
    item1.description.valor = u'Notebook hehe'
    item1.amount.valor = u'2345.67'
    # item1.quantity.valor = u'1.0'
    item1.quantity.valor = 1
    item1.weight.valor = 1000       # peso em gramas

    xmlRequisicao.items.append(item1)

    print u'Verificando erros no XML checkout: ', len(xmlRequisicao.alertas), u'encontrado(s)'

    if xmlRequisicao.alertas:

        print u'-' * 45, u'ALERTAS', u'' * 46

        for a in xmlRequisicao.alertas:
            print a

        print u'-' * 100

    if not xmlRequisicao.alertas:

        print u'Gerando requisicao'

        ok, retorno = api.checkout_v2(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, xmlRequisicao)

        print u'Resultado da requisicao:', ok and u'OK' or u'FALHA'

        if ok:

            print u'-' * 45, u'RESPOSTA', u'-' * 45
            print retorno.xml
            print u'-' * 100

            if retorno.alertas:

                print u'-' * 45, u'ALERTAS', u'' * 46

                for a in retorno.alertas:
                    print a

                print u'-' * 100

            # >>> retorno ==> ClassePagamentoRetornoCheckout
            CODIGO_REQUISICAO = retorno.code.valor

            url_fluxo = api.gera_url_fluxo_v2(CODIGO_REQUISICAO)
            # >> u'https://[sandbox.]pagseguro.uol.com.br/v2/pre-approvals/request.html?code=CODIGO_REQUISICAO'

            print u'URL para o fluxo:', url_fluxo

            # no final do pagamento, a PagSeguro vai gerar a URL como a de baixo
            REDIRECIONAMENTO=u'http://seusite.com.br/?code=CODIGO_NOTIFICACAO'

        else:
            if type(retorno) in (str, unicode, basestring):
                print u'Motivo do erro:', retorno
            else:
                print u'Motivo do erro:', retorno.xml

print u'*' * 100
exemploCheckout()
print u'*' * 100