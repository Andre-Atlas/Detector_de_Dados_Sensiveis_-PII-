import pandas as pd
from typing import Optional
import os

def carregar_dados(caminho_arquivo: str) -> Optional[pd.DataFrame]:
    """
    Carrega o arquivo CSV com tratamento de erros para quebras de linha internas.
    
    Args:
        caminho_arquivo (str): Caminho do arquivo CSV.
        
    Returns:
        Optional[pd.DataFrame]: DataFrame carregado ou None em caso de erro.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo não encontrado em {caminho_arquivo}")
        return None
        
    codificacoes = ['utf-8', 'iso-8859-1', 'latin1', 'cp1252']
    
    for codificacao in codificacoes:
        try:
            # LÓGICA COMPLEXA: sep=None com engine='python' detecta o separador 
            # automaticamente (vírgula, ponto e vírgula, etc). Isso é crucial para
            # datasets brasileiros que variam o padrão de exportação.
            # on_bad_lines='warn' evita que o script pare caso haja linhas mal formatadas.
            df = pd.read_csv(
                caminho_arquivo, 
                sep=None, 
                encoding=codificacao, 
                engine='python',
                on_bad_lines='warn'
            )
            print(f"Arquivo carregado com sucesso usando codificação: {codificacao}")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Erro ao carregar CSV com codificação {codificacao}: {e}")
            continue
            
    print("Erro: Não foi possível ler o arquivo com nenhuma das codificações testadas.")
    return None

def salvar_dados(df: pd.DataFrame, caminho_saida: str) -> bool:
    """
    Salva o DataFrame em um arquivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        caminho_saida (str): Caminho do arquivo de saída.
        
    Returns:
        bool: True se salvo com sucesso, False caso contrário.
    """
    try:
        df.to_csv(caminho_saida, index=False, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
        return False
