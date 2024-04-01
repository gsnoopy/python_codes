import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

vendas = pd.read_csv('./databases/vendas.txt', sep=';', header=None)
pesquisas = pd.read_csv('./databases/pesquisas.txt', sep=';', header=None)

vendas = vendas.rename(columns={0: 'ID',
                                1: 'User',
                                2: 'Data_Venda',
                                3: 'Login',
                                4: 'Password',
                                5: 'Valor',
                                6: 'Cupom'})

pesquisas = pesquisas.rename(columns={0: 'User', 
                                      1: 'Skin'})

i = 0
for item in tqdm(vendas['Valor']):
    vendas.loc[i,'Valor_Taxado'] = round(item * 0.99, 2)
    i+=1

soma_valor = vendas['Valor_Taxado'].sum()
lucro = soma_valor - vendas.shape[0] * 0.50
qtd_cupom = vendas['Cupom'].value_counts()
qtd_skins = pesquisas['Skin'].value_counts().head(20)
users = vendas['User'].value_counts().head(5)

fig, ax = plt.subplots()

valores = qtd_cupom.values
indices = qtd_cupom.index

bars = ax.bar(indices, valores, color='red')

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

ax.set_xlabel('Cupom')
ax.set_ylabel('Quantidade')
ax.set_title('Quantidade de Ocorrências por Cupom')

plt.xticks(rotation=90)

plt.savefig('./saidas/cupom.png', dpi=300, bbox_inches='tight')

vendas['Data_Venda'] = pd.to_datetime(vendas['Data_Venda'])

vendas['Dia'] = vendas['Data_Venda'].dt.date


vendas_por_dia = vendas.groupby('Dia').size()


fig, ax = plt.subplots()
vendas_por_dia.plot(kind='bar', ax=ax)


for i, v in enumerate(vendas_por_dia):
    ax.annotate(str(v), xy=(i, v), xytext=(i, v), ha='center', va='bottom')

ax.set_xlabel('Dia')
ax.set_ylabel('Quantidade de Vendas'.format(int(max(vendas_por_dia))))
ax.set_title('Quantidade de Vendas por Dia')

plt.savefig('./saidas/vendas.png', dpi=300, bbox_inches='tight')

with open('./saidas/dados.txt', 'w') as arquivo:
    
    arquivo.write(f'Lucro do mês: R$ {lucro}\n\n')

    arquivo.write('Vendas por Dia:\n\n')
    for dia, quantidade in vendas_por_dia.items():
        linha = f'{dia}\t{quantidade}\n'
        arquivo.write(linha)


    arquivo.write('\n')

    arquivo.write('Quantidade de Cupons:\n\n')
    for cupom, quantidade in qtd_cupom.items():
        linha = f'{cupom}\t{quantidade}\n'
        arquivo.write(linha)


    arquivo.write('\n')


    arquivo.write('Quantidade de Skins:\n\n')
    for skin, quantidade in qtd_skins.items():
        linha = f'{skin}\t{quantidade}\n'
        arquivo.write(linha)
        
    arquivo.write('\n')


    arquivo.write('Maiores compradores:\n\n')
    for user, quantidade in users.items():
        linha = f'{user}\t{quantidade}\n'
        arquivo.write(linha)