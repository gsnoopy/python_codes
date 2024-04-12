import re

with open('message.txt', 'r') as arquivo:
    sales = arquivo.read()

padrao = re.compile(r'Subtotal: R\$ (\d+,\d+) Status')

valores = padrao.findall(sales)

soma = 0

with open('salesGGMAX.txt', 'w') as resultFile:
    for valor in valores:

        resultFile.write("R$ " + valor + "\n")
        valor_float = float(valor.replace(',', '.'))
        soma += valor_float
        
    resultFile.write("\nSoma total: R$ {:.2f}".format(soma))
