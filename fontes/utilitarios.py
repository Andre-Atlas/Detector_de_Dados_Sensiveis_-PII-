import re
import unicodedata

def limpar_texto(texto: str) -> str:
    """
    Limpa e normaliza o texto para facilitar a detecção de DPI.
    
    Args:
        texto (str): Texto original.
        
    Returns:
        str: Texto limpo.
    """
    if not isinstance(texto, str):
        return ""
    
    # Remove quebras de linha e espaços extras
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def normalizar_acentos(texto: str) -> str:
    """
    Remove acentos do texto.
    
    Args:
        texto (str): Texto com acentos.
        
    Returns:
        str: Texto sem acentos.
    """
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn')
