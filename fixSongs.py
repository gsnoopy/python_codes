import os
import random

diretorio = os.path.dirname(os.path.abspath(__file__))
link = 'spotifydown.com - '

def removeDownloadLink(diretorio,link):
    
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)

        if nome_arquivo.endswith('.mp3'):
            novo_nome = nome_arquivo.replace(link, '')
            os.rename(caminho_arquivo, os.path.join(diretorio, novo_nome))
            print(f"Arquivo renomeado: {nome_arquivo} -> {novo_nome}")


def addNumber(diretorio,quantidade):
    
    arquivos_mp3 = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith('.mp3')]
    numeros_aleatorios = random.sample(range(1, quantidade+1), len(arquivos_mp3))

    for numero, nome_arquivo in zip(numeros_aleatorios, arquivos_mp3):
        novo_nome = f"{numero} - {nome_arquivo}"
        caminho_arquivo_antigo = os.path.join(diretorio, nome_arquivo)
        caminho_arquivo_novo = os.path.join(diretorio, novo_nome)
        
        os.rename(caminho_arquivo_antigo, caminho_arquivo_novo)
        print(f"Arquivo renomeado: {nome_arquivo} -> {novo_nome}")

print("----------REMOVENDO LINKS----------")

removeDownloadLink(diretorio,link)

print("----------ADICIONANDO NÚMEROS----------")

addNumber(diretorio,5) # Alterar para a quantidade de músicas no diretório