pagseguro_xml
==========================

API do PagSeguro, em python, através de XML gerado por classes. Projeto baseado no esquema proposto no projeto [PySPED](https://github.com/aricaldeira/PySPED).

#Instalando

```bash
pip install -e git+https://github.com/arannasousa/pagseguro_xml#egg=pagseguro_xml
```

ou

```
git clone https://github.com/arannasousa/pagseguro_xml
cd pagseguro_xml
pip install -r dependencias.txt
python setup.py install
```

## Se houver problemas com o lxml

Caso encontre problemas na instalação do **lxml** pelo `pip`, tente usar o `easy_install`.

```
easy_install lxml
```

#Como usar

### Exemplos

No diretório [**exemplos**](https://github.com/arannasousa/pagseguro_xml/tree/master/exemplos) possui arquivos com os testes para cada API (pagamento, assinatura, consultas, notificacao) com suas opções de requisição.

## Pagamento / Checkout

Para gerar uma solicitação de pagamento/checkout:

```python 

# criando a classe xml para efetuar o Checkout 
from pagseguro_xml.pagamento.v2.classes.pagamento import CONST as CONST_PAGAMENTO, ClassePagamentoCheckout, Item

checkout = ClassePagamentoCheckout()

# ao final do pagamento, o PagSeguro irá redirecionar para...
checkout.redirectURL.valor = u'http://seusite.com.br'
checkout.reference.valor = u'REF0001'

# prazo maximo de validade do CODIGO_PAGAMENTO que será criado pela PagSeguro (5 minutos)
checkout.maxAge.valor = 5 * 60

checkout.sender.name.valor = u'Cliente de teste'
checkout.sender.email.valor = u'as1234231234e@sandbox.pagseguro.com.br'

checkout.sender.phone.areaCode.valor = u'63'
checkout.sender.phone.number.valor = u'92111111'

checkout.shipping.type.valor = CONST_PAGAMENTO.SHIPPING.TYPE.NAO_ESPECIFICADO
checkout.shipping.address.city.valor = u'Palmas'
checkout.shipping.address.state.valor = u'TO'
checkout.shipping.address.country.valor = u'BRA'     # valor default

# criando o item para o Checkout, quantos desejar    
item1 = Item()
item1.ID.valor = u'ITEM0001'
item1.description.valor = u'Notebook Preto'
item1.amount.valor = u'2345.67'
item1.quantity.valor = 1
item1.weight.valor = 1000       # peso em gramas

# adicionando o Item ao Checkout
checkout.items.append(item1)

# apos preencher o Checkout, vamos verificar se houve algum erro 
# como: campos obrigatorios, passaram do limite, opcao nao disponivel, valores incorretos
    
if xmlRequisicao.alertas:

    print u'-' * 45, u'ALERTAS', u'' * 46

    for a in checkout.alertas:
        print a

    print u'-' * 100
    
    
if not xmlRequisicao.alertas:

    # variaveis
    
    TOKEN_API = u''
    EMAIL_API = u''
        
    # importando a Classe que irá gerar a requisição e retonar o CODIGO para a url de pagamento (se tudo ok)
    from pagseguro_xml.pagamento import ApiPagSeguroConsulta_v2, CONST_v2
    
    # se nao informado, por padrão, o ambiente é SANDBOX
    api = ApiPagSeguroPagamento_v2(ambiente=CONST_v2.AMBIENTE.SANDBOX)
    
    # iniciando processo de ENVIO e RETORNO à PagSeguro
    ok, retorno = api.checkout_v2(EMAIL_API, TOKEN_API, checkout)
    # podera acontecer os seguintes retorno:
    #   
    # sucesso -> True, instância da classe ClassePagamentoRetornoCheckout
    #
    # falha   -> False, instância da classe ClassePagamentoErros (quando o status da requisicao for 400)
    # falha   -> False, texto (unicode) contendo o motivo do erro
    #
    
    if ok:
    
        print u'-' * 45, u'RESPOSTA', u'-' * 45
        # visualizando o XML retornado
        print retorno.xml
        print u'-' * 100
    
        # checando erros no XML retornado
        if retorno.alertas:
    
            print u'-' * 45, u'ALERTAS', u'' * 46
    
            for a in retorno.alertas:
                print a
    
            print u'-' * 100
    
        # pegando o CODIGO retornado no XML (ClassePagamentoRetornoCheckout)
        #   Exemplo da PagSeguro:
        #
        #   <?xml version="1.0" encoding="ISO-8859-1"?>  
        #    <checkout>  
        #        <code>8CF4BE7DCECEF0F004A6DFA0A8243412</code>     <- este codigo  
        #        <date>2010-12-02T10:11:28.000-02:00</date>  
        #    </checkout>
        #
        CODIGO_REQUISICAO = retorno.code.valor
    
        # gerando a URL para REDIRECIONAMENTO do CLIENTE para efetuar o PAGAMENTO na PagSeguro
        url_fluxo = api.gera_url_fluxo_v2(CODIGO_REQUISICAO)    
        # >> u'https://[sandbox.]pagseguro.uol.com.br/v2/pre-approvals/request.html?code=CODIGO_REQUISICAO'
    
        print u'URL para o fluxo:', url_fluxo
    
        # no final do pagamento a PagSeguro vai gerar a URL como a de baixo, 
        # conforme informado na tag 'checkout.redirectURL.valor'
        # 
        # u'http://seusite.com.br/?code=CODIGO_NOTIFICACAO'
    
    else:
    
        # https://pagseguro.uol.com.br/v2/guia-de-integracao/api-de-pagamentos.html#v2-item-api-de-pagamentos-resposta
        
        # exibindo o erro 
        
        if hasattr(retorno, u'xml'):
            print u'Motivo do erro:', retorno.xml
        else:
            print u'Motivo do erro:', retorno

```


## Notificações

Consultando uma notificação de transação:

> https://pagseguro.uol.com.br/v3/guia-de-integracao/api-de-notificacoes.html

```python 


from pagseguro_xml.notificacao import ApiPagSeguroNotificacao_v3, CONST_v3

# variaveis
TOKEN_API = u''
EMAIL_API = u''

CHAVE_NOTIFICACAO = u''

# se nao informado, por padrão, o ambiente é SANDBOX
api = ApiPagSeguroNotificacao_v3(ambiente=CONST_v3.AMBIENTE.SANDBOX)

# consultando a TRANSACAO através da chave_de_notificacao
ok, retorno = api.consulta_notificacao_transacao_v3(EMAIL_API, TOKEN_API, CHAVE_NOTIFICACAO)

# podera acontecer os seguintes retorno:
#   
# sucesso -> True, instância da classe ClasseNotificacaoTransacao
# falha   -> False, texto (unicode) contendo o motivo do erro
#

if ok:
    
    print u'-' * 45, u'RESPOSTA', u'-' * 45
    # visualizando o XML retornado
    print retorno.xml
    print u'-' * 100

    # checando erros no XML retornado
    if retorno.alertas:

        print u'-' * 45, u'ALERTAS', u'' * 46

        for a in retorno.alertas:
            print a

        print u'-' * 100

else:
    print u'Motivo do erro:', retorno

```


## Consultas

Conforme o [guia da PagSeguro](https://pagseguro.uol.com.br/v2/guia-de-integracao/consultas.html), existem 3 formas de fazer consulta de transação financeira:

### 1. DETALHES da transação (versão 3)

> https://pagseguro.uol.com.br/v3/guia-de-integracao/consulta-de-transacoes-por-codigo.html

```python

# variaveis
TOKEN_API = u''
EMAIL_API = u'seu@email.com'

# codigo da transação que deseja consultar
CODIGO_TRANSACAO = u''

from pagseguro_xml.consultas import ApiPagSeguroConsulta_v3, CONST_v3

# se nao informado, por padrão, o ambiente é SANDBOX
api = ApiPagSeguroConsulta_v3(ambiente=CONST_v3.AMBIENTE.SANDBOX)

# realiza a consulta do CODIGO da TRANSACAO, se sucesso, retorna uma CLASSE que representa o XML
ok, retorno = api.detalhes_v3(EMAIL_API, TOKEN_API, CODIGO_TRANSACAO)

#
# podera acontecer os seguintes retorno:
#   
# sucesso -> True, instância da classe ClasseTransacaoDetalhes
# falha   -> False, texto (unicode) contendo o motivo do erro
#

if ok:

    print u'-' * 45, u'RESPOSTA', u'-' * 45
    
    # visualizando o XML retornado
    print retorno.xml
    
    print u'-' * 100

    # acessando o STATUS da transacao
    print u'Status da TRANSACAO', retorno.status.valor

    # checando erros no XML retornado
    if retorno.alertas:

        print u'-' * 45, u'ALERTAS', u'' * 46

        for a in retorno.alertas:
            print a

        print u'-' * 100

else:
    print u'Motivo do erro:', retorno

```

### 2. CONSULTA de transações por INTERVALO DE DATAS (versão 2)

> https://pagseguro.uol.com.br/v2/guia-de-integracao/consulta-de-transacoes-por-intervalo-de-datas.html

```python

# variaveis
TOKEN_API = u''
EMAIL_API = u'seu@email.com'

# codigo da transação que deseja consultar
CODIGO_TRANSACAO = u''

from pagseguro_xml.consultas import ApiPagSeguroConsulta_v3, CONST_v3

# se nao informado, por padrão, o ambiente é SANDBOX
api = ApiPagSeguroConsulta_v3(ambiente=CONST_v3.AMBIENTE.SANDBOX)

from datetime import datetime

# Gera um periodo para consulta
#
# Obs.: Cuidado com as limitações da PAGSEGURO
#
# 1. 'data_inicial' NÃO pode ser maior que 6 meses, contados de HOJE
# 2. 'data_final - data_inicial' NÃO pode ser maior que 30 dias
#
data_inicial = datetime(2015, 12, 9)
data_final = datetime(2015, 12, 12)

# realiza a consulta das TRANSACOES no período especificado acima
# se sucesso, retorna uma CLASSE que representa o XML
ok, retorno = api.historico_v2(EMAIL_API, TOKEN_API, data_inicia, data_final)

#
# podera acontecer os seguintes retorno:
#   
# sucesso -> True, instância da classe ClasseTransacaoHistorico
# falha   -> False, texto (unicode) contendo o motivo do erro
#

if ok:

    print u'-' * 45, u'RESPOSTA', u'-' * 45
    
    # visualizando o XML retornado
    print retorno.xml
    
    print u'-' * 100

    print u'Total de transações localizadas:', retorno.resultsInThisPage.valor, len(retorno.transactions) 
    
    # acessando o STATUS de cada transacao
    for i, transacao in enumerate(retorno.transactions, start=1):
            print u' - Transacao No "%s", STATUS: %s ' % (i, transacao.status.valor)

    # checando erros no XML retornado
    if retorno.alertas:

        print u'-' * 45, u'ALERTAS', u'' * 46

        for a in retorno.alertas:
            print a

        print u'-' * 100

else:
    print u'Motivo do erro:', retorno

```

### 3. CONSULTA de transações ABANDONADAS (versão 2)

> https://pagseguro.uol.com.br/v2/guia-de-integracao/consulta-de-transacoes-abandonadas.html

```python

# variaveis
TOKEN_API = u''
EMAIL_API = u'seu@email.com'

# codigo da transação que deseja consultar
CODIGO_TRANSACAO = u''

from pagseguro_xml.consultas import ApiPagSeguroConsulta_v3, CONST_v3

# se nao informado, por padrão, o ambiente é SANDBOX
api = ApiPagSeguroConsulta_v3(ambiente=CONST_v3.AMBIENTE.SANDBOX)

from datetime import datetime

# Gera um periodo para consulta
#
# Obs.: Cuidado com as limitações da PAGSEGURO
#
# 1. 'data_inicial' NÃO pode ser maior que 6 meses, contados de HOJE
# 2. 'data_final - data_inicial' NÃO pode ser maior que 30 dias
#
data_inicial = datetime(2015, 12, 9)
data_final = datetime(2015, 12, 12)

# realiza a consulta das TRANSACOES no período especificado acima
# se sucesso, retorna uma CLASSE que representa o XML
ok, retorno = api.abandonadas_v2(EMAIL_API, TOKEN_API, data_inicia, data_final)

#
# podera acontecer os seguintes retorno:
#   
# sucesso -> True, instância da classe ClasseTransacaoAbandonadas
# falha   -> False, texto (unicode) contendo o motivo do erro
#

if ok:

    print u'-' * 45, u'RESPOSTA', u'-' * 45
    
    # visualizando o XML retornado
    print retorno.xml
    
    print u'-' * 100

    print u'Total de transações localizadas:', retorno.resultsInThisPage.valor, len(retorno.transactions) 
    
    # acessando a REFERENCIA de cada transacao
    for i, transacao in enumerate(retorno.transactions, start=1):
            print u' - Transacao No "%s", REFERENCIA: %s ' % (i, transacao.reference.valor)

    # checando erros no XML retornado
    if retorno.alertas:

        print u'-' * 45, u'ALERTAS', u'' * 46

        for a in retorno.alertas:
            print a

        print u'-' * 100

else:
    print u'Motivo do erro:', retorno

```

## Assinaturas

> Aguardando tempo para concluir a documentação

