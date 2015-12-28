# coding=utf-8
# ---------------------------------------------------------------
# Desenvolvedor:    Arannã Sousa Santos
# Mês:              12
# Ano:              2015
# Projeto:          pagseguro_xml
# e-mail:           asousas@live.com
# ---------------------------------------------------------------

import logging
from pagseguro_xml.notificacao import ApiPagSeguroNotificacao_v3, CONST_v3


logger = logging.basicConfig(level=logging.DEBUG)


PAGSEGURO_API_AMBIENTE = u'sandbox'
PAGSEGURO_API_EMAIL = u'seu@email.com'
PAGSEGURO_API_TOKEN_PRODUCAO = u''
PAGSEGURO_API_TOKEN_SANDBOX = u''


CHAVE_NOTIFICACAO = u'AA0000-AA00A0A0AA00-AA00AA000000-AA0000'      # ela éh de producao


api = ApiPagSeguroNotificacao_v3(ambiente=CONST_v3.AMBIENTE.SANDBOX)
PAGSEGURO_API_TOKEN = PAGSEGURO_API_TOKEN_PRODUCAO


ok, retorno = api.consulta_notificacao_transacao_v3(PAGSEGURO_API_EMAIL, PAGSEGURO_API_TOKEN, CHAVE_NOTIFICACAO)

if ok:

    print u'-' * 50
    print retorno.xml
    print u'-' * 50

    for a in retorno.alertas:
        print a

else:
    print u'Motivo do erro:', retorno

