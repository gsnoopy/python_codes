import xlwings as xw
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import math
import os

api = Flask(__name__)

@api.route("/simulador", methods=['POST'])
def getDate():
    
    data = request.get_json()
    fornecedor = data.get("fornecedor")
    tipo_pessoa = data.get("tipo_pessoa")
    #cpf_cnpj = data.get("cnp_cnpj")
    nascimento = data.get("nascimento")
    valor_imovel = data.get("valor_imovel")
    valor_financiamento = data.get("valor_financiamento")
    #valor_entrada = data.get("valor_entrada")
    valor_despesas = data.get("valor_despesas")
    #uf = data.get("uf")
    #cidade = data.get("cidade")
    uso_imovel = data.get("uso_imovel")
    #situacao_imovel = data.get("situacao_imovel")
    prazo_pagamento_meses = data.get("prazo_pagamento_meses")
    indexador = data.get("indexador")
    amortizacao = data.get("amortizacao")
    #valor_renda_liquida_mensal = data.get("valor_renda_liquida_mensal")
    #valor_renda_liquida_mensal_adicional = data.get("valor_renda_liquida_mensal_adicional")
    financiar_despesas = data.get("financiar_despesas")

    if fornecedor == 'Bradesco':
        
        indexador = {'tr': 'Repasse/Aquisição', 'poupanca': 'Poupança+'}.get(indexador, indexador)
        tipo_pessoa = {'pf': 'PESSOA FÍSICA', 'pj': 'PESSOA JURÍDICA'}.get(tipo_pessoa, tipo_pessoa)
        financiar_despesas = {True: 'SIM', False: 'NÃO'}.get(financiar_despesas, financiar_despesas)
        uso_imovel = {'terreno': 'LOTE'}.get(uso_imovel, uso_imovel)
        nascimento_formatado = datetime.strptime(nascimento, "%Y-%m-%d").date()
        valor_imovel = math.ceil(valor_imovel)
        valor_imovel = str(valor_imovel).replace(".", ",")
        valor_financiamento = str(valor_financiamento).replace(".", ",")
        valor_despesas = str(valor_despesas).replace(".", ",")
        prazo_pagamento_meses = str(prazo_pagamento_meses)
        
        app = xw.apps.add()
        app.visible = False
        with xw.App(visible=False, add_book=False) as app:
            wk = app.books.open('Bradesco.xls')
            ws = wk.sheets('Simulador Bradesco')
                        
            #inputs
            ws["D9"].value = indexador
            ws["D13"].value = tipo_pessoa
            ws["D15"].value = uso_imovel
            ws["D17"].value = financiar_despesas
            ws["D19"].value = amortizacao
            ws["D21"].value = nascimento_formatado
            ws["I13"].value = 'PRIME'
            ws["I15"].value = valor_imovel
            ws["I19"].value = valor_despesas if financiar_despesas == 'SIM' else 0
            ws["I17"].value = valor_financiamento   
            ws["I21"].value = prazo_pagamento_meses

            calculo_celula = 38 + int(prazo_pagamento_meses)
            ultima_celula = "R" + str(calculo_celula)   
 
            #outputs
            primeira_prestacao = round(float(ws["Q10"].value),2)
            ultima_prestacao = round(float(ws[ultima_celula].value),2)
            juros = 0   
            juros_efetivo = round(ws["Q25"].value * 100, 2)
            cet = round(ws["Q27"].value * 100, 2)
            cesh = 1.00
            
            results = {
                "primeira_prestacao": primeira_prestacao,
                "ultima_prestacao": ultima_prestacao,
                "juros": juros,
                "juros_efetivo": juros_efetivo,
                "cet": cet,
                "cesh": cesh
            }
            
            return jsonify(results)

    if fornecedor == 'Itaú' or fornecedor == 'Itau':
        
        app = xw.apps.add()
        app.visible = False
        with xw.App(visible=False, add_book=False) as app:
            wk = app.books.open('Itau.xls')
            ws = wk.sheets('SIMULADOR')
            data_atual = datetime.now()
            data_futura = data_atual + timedelta(days=90)
            data_contrato = str(data_futura.strftime('%d/%m/%Y').replace('/', ''))
            valor_imovel = str(valor_imovel).replace(".", ",")
            valor_financiamento = str(valor_financiamento).replace(".", ",")
            valor_despesas = str(valor_despesas).replace(".", ",")
            prazo_pagamento_meses = str(prazo_pagamento_meses)
            amortizacao = 'MIX' if amortizacao.lower() == 'price' else amortizacao
            nascimento_formatado = datetime.strptime(nascimento, "%Y-%m-%d").strftime("%d%m%Y")
            
            #inputs
            ws["D12"].value = data_contrato
            ws["D15"].value = uso_imovel
            ws["D20"].value = nascimento_formatado
            ws["F20"].value = 100000
            ws["I6"].value = 0
            ws["I8"].value = "CH"
            ws["I10"].value = "Personnalité"
            ws["I14"].value = valor_imovel
            ws["I17"].value = valor_financiamento
            ws["I21"].value = prazo_pagamento_meses
            ws["I25"].value = amortizacao
            #outputs
            primeira_prestacao = round(float(ws["D43"].value),2)
            ultima_prestacao = round(float(ws["F43"].value),2)
            juros = round(ws["H43"].value * 100, 2)
            juros_efetivo = round(ws["I43"].value * 100, 2)
            cet = round(ws["J43"].value * 100, 2)
            cesh = round(ws["K43"].value * 100, 2)
            
            if((ws["C27"].value).startswith("Tudo certo!")):
                
                results = {
                    "primeira_prestacao": primeira_prestacao,
                    "ultima_prestacao": ultima_prestacao,
                    "juros": juros,
                    "juros_efetivo": juros_efetivo,
                    "cet": cet,
                    "cesh": cesh
                }
                
                return jsonify(results)
            
            else:
                
                return "Por favor insira valores válidos para a Simulação Itaú"
            
            

@api.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if (__name__ == "__main__"):
    CORS(api)
    api.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 5555)))
    #CORS(api)  