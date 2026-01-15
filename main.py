import sys
import os
import argparse
from fontes.carregador_dados import carregar_dados, salvar_dados
from fontes.detectores import DetectorDPI
from fontes.utilitarios import limpar_texto

def principal():
    """
    Função principal de execução do pipeline de detecção de DPI.
    """
    parser = argparse.ArgumentParser(description='Hackathon Participa DF - Detector de DPI')
    parser.add_argument('entrada', help='Caminho do arquivo CSV de entrada (ex: data/AMOSTRA_e-SIC.csv)')
    parser.add_argument('--saida', default='resultado_dpi.csv', help='Caminho do arquivo de saída (default: resultado_dpi.csv)')
    
    argumentos = parser.parse_args()
    
    print("--- Hackathon Participa DF: Categoria I (Acesso à Informação) ---")
    print(f"Lendo dados de: {argumentos.entrada}")
    
    df = carregar_dados(argumentos.entrada)
    
    if df is None:
        sys.exit(1)
        
    # Tenta encontrar a coluna de texto, aceitando variações de nome
    coluna_texto = None
    colunas_possiveis = ['Texto', 'Texto Mascarado', 'texto', 'TEXTO']
    for col in colunas_possiveis:
        if col in df.columns:
            coluna_texto = col
            break
            
    if coluna_texto is None:
        print(f"Erro: Coluna de texto não encontrada. Colunas disponíveis: {df.columns.tolist()}")
        sys.exit(1)
        
    detector = DetectorDPI()
    
    print(f"Processando textos da coluna '{coluna_texto}' e detectando DPI...")
    
    # Aplicando limpeza e detecção
    df['Contem_DPI'] = df[coluna_texto].apply(lambda x: "Sim" if detector.tem_dpi(limpar_texto(str(x))) else "Não")
    
    print(f"Salvando resultados em: {argumentos.saida}")
    if salvar_dados(df, argumentos.saida):
        print("Processo concluído com sucesso!")
    else:
        print("Falha ao salvar os resultados.")
        sys.exit(1)

if __name__ == "__main__":
    principal()
