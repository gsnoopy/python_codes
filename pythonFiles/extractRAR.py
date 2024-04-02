import os
import rarfile

def extrair_arquivo_rar(arquivo_rar):
    try:
        destino = os.path.dirname(arquivo_rar)
        with rarfile.RarFile(arquivo_rar, 'r') as rf:
            rf.extractall(destino)
        print(f"Arquivo {arquivo_rar} extraído com sucesso para {destino}.")
    except Exception as e:
        print(f"Erro ao extrair arquivo {arquivo_rar}: {e}")

arquivo_rar = "Guitar Hero III Brazucas 2.rar"
extrair_arquivo_rar(arquivo_rar)    
