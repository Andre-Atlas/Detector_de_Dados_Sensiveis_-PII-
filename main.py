import sys
import os
import argparse
import pandas as pd
from tqdm import tqdm
from fontes.carregador_dados import carregar_dados, salvar_dados
from fontes.detectores import DetectorDPI
from fontes.utilitarios import limpar_texto

def formatar_elementos(dicionario_evidencias):
    """
    LÓGICA COMPLEXA: Converte o dicionário de evidências em uma string legível.
    Agrupa os achados por tipo (CPF, Nome, etc) para facilitar a auditoria.
    """
    if not dicionario_evidencias:
        return ""
    itens = []
    for k, v in dicionario_evidencias.items():
        if isinstance(v, list):
            itens.append(f"{k}: {', '.join(map(str, v))}")
        else:
            itens.append(f"{k}: {v}")
    return " | ".join(itens)

import subprocess

def principal():
    """
    Função principal de execução do pipeline de detecção de DPI com relatório detalhado.
    Implementa a lógica de auditoria solicitada (Classificação + Justificativa).
    """
    parser = argparse.ArgumentParser(description='Hackathon Participa DF - Detector de DPI Avançado')
    parser.add_argument('entrada', nargs='?', help='Caminho do arquivo CSV de entrada (opcional se usar --gui)')
    parser.add_argument('--saida', default='resultado_analise_completa.csv', help='Caminho do arquivo de saída')
    parser.add_argument('--gui', action='store_true', help='Inicia a interface gráfica (Streamlit)')
    
    argumentos = parser.parse_args()

    # Se --gui for passado ou se não houver argumentos de entrada, inicia a GUI
    if argumentos.gui or not argumentos.entrada:
        print("\n--- Iniciando Interface Gráfica (Streamlit) ---")
        try:
            subprocess.run(["streamlit", "run", "interface_gui.py"])
        except FileNotFoundError:
            print("Erro: Streamlit não encontrado. Instale com 'pip install streamlit'.")
        return
    
    print("\n--- Iniciando Análise Otimizada (Junie AI) ---")
    print(f"Lendo dados de: {argumentos.entrada}")
    
    df = carregar_dados(argumentos.entrada)
    
    if df is None:
        sys.exit(1)
        
    # Tenta encontrar a coluna de texto
    coluna_texto = None
    colunas_possiveis = ['Texto Mascarado', 'Texto', 'texto', 'TEXTO']
    for col in colunas_possiveis:
        if col in df.columns:
            coluna_texto = col
            break
            
    if coluna_texto is None:
        print(f"Erro: Coluna de texto não encontrada. Colunas disponíveis: {df.columns.tolist()}")
        sys.exit(1)
        
    detector = DetectorDPI()
    
    print(f"Processando textos da coluna '{coluna_texto}' e gerando justificativas...")
    
    resultados = []
    
    for idx, linha in tqdm(df.iterrows(), total=len(df), desc="Analisando"):
        texto_original = str(linha.get(coluna_texto, ''))
        texto_limpo = limpar_texto(texto_original)
        
        analise = detector.analisar(texto_limpo)
        
        # Colunas pedidas: Classificação (PRIVADO/PUBLICO) e Elementos_Encontrados
        classificacao = "PRIVADO" if analise['contem_dpi'] else "PUBLICO"
        justificativa = formatar_elementos(analise['evidencias'])
        
        # Mantém colunas originais e adiciona as novas para o relatório de auditoria
        nova_linha = linha.to_dict()
        nova_linha['Classificacao'] = classificacao
        nova_linha['Elementos_Encontrados'] = justificativa
        
        # Remove coluna antiga se existir para manter o CSV limpo
        if 'Contem_DPI' in nova_linha:
            del nova_linha['Contem_DPI']
            
        resultados.append(nova_linha)

    df_final = pd.DataFrame(resultados)
    
    print(f"Salvando resultados em: {argumentos.saida}")
    if salvar_dados(df_final, argumentos.saida):
        print("\n--- Relatório Gerado ---")
        if 'Classificacao' in df_final.columns:
            print(df_final['Classificacao'].value_counts())
        print(f"\nArquivo salvo com sucesso em: {argumentos.saida}")
    else:
        print("Falha ao salvar os resultados.")
        sys.exit(1)

if __name__ == "__main__":
    principal()
