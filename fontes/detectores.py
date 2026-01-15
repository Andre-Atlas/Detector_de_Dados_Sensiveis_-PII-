import re
from typing import List, Dict, Any, Optional

class DetectorDPI:
    """
    Classe responsável pela detecção de Dados Pessoais (PII) em textos.
    Utiliza uma combinação de Expressões Regulares (Regex) e Processamento de Linguagem Natural (NLP).
    """

    def __init__(self):
        # Padrões de Regex
        self.padroes = {
            "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
            "RG": r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dX]?\b|\b\d{7,9}\b",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "TELEFONE": r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}\b",
            "CNPJ": r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b",
            "ENDERECO": r"(?i)\b(Rua|Av|Avenida|Logradouro|Quadra|Bloco|Apartamento|Casa|Lote)\b.*?\d+",
            "FINANCEIRO": r"(?i)\b(Banco|Agência|Conta|PIX|Cartão|Salário|Vencimento)\b.*?\d+"
        }

    def detectar_com_regex(self, texto: str) -> Dict[str, List[str]]:
        """
        Detecta DPIs baseados em padrões estruturados (Regex).

        Args:
            texto (str): O texto a ser analisado.

        Returns:
            Dict[str, List[str]]: Um dicionário mapeando o tipo de dado para a lista de ocorrências.
        """
        resultados = {}
        for tipo_dpi, padrao in self.padroes.items():
            ocorrencias = re.findall(padrao, texto)
            if ocorrencias:
                resultados[tipo_dpi] = ocorrencias
        return resultados

    def detectar_com_ner(self, texto: str) -> Dict[str, List[str]]:
        """
        Detecta DPIs baseados em Entidades Nomeadas (NER) como nomes de pessoas e locais.
        Nota: Esta implementação utiliza heurísticas para identificar nomes próprios e 
        palavras-chave sensíveis (saúde, financeiro) conforme solicitado no edital.

        Args:
            texto (str): O texto a ser analisado.

        Returns:
            Dict[str, List[str]]: Um dicionário com entidades detectadas.
        """
        resultados = {"PESSOA": [], "SENSIVEL": []}
        
        # LÓGICA COMPLEXA: Heurística para nomes próprios (ex: João Silva, Maria Oliveira)
        # O lookbehind negativo (?<![.!?]\s) garante que não capturamos uma palavra 
        # capitalizada apenas porque está no início de uma frase (ex: "Gostaria de...").
        # Exige ao menos dois nomes capitalizados em sequência.
        padrao_nome = r"(?<![.!?]\s)\b[A-Z][a-zà-ÿ]+\s[A-Z][a-zà-ÿ]+\b"
        ocorrencias_nomes = re.findall(padrao_nome, texto)
        if ocorrencias_nomes:
            resultados["PESSOA"] = ocorrencias_nomes

        # Detecção de dados sensíveis (Saúde) via palavras-chave
        palavras_chave_saude = r"(?i)\b(Exame|Laudo|Médico|Hospital|Saúde|Doença|Tratamento|Receita|Prontuário)\b"
        ocorrencias_saude = re.findall(palavras_chave_saude, texto)
        if ocorrencias_saude:
            resultados["SENSIVEL"] = ocorrencias_saude
            
        return {k: v for k, v in resultados.items() if v}

    def tem_dpi(self, texto: str) -> bool:
        """
        Verifica se o texto contém qualquer tipo de dado pessoal.

        Args:
            texto (str): O texto a ser analisado.

        Returns:
            bool: True se contiver DPI, False caso contrário.
        """
        if not texto or not isinstance(texto, str):
            return False
            
        resultados_regex = self.detectar_com_regex(texto)
        if resultados_regex:
            return True
            
        resultados_ner = self.detectar_com_ner(texto)
        if resultados_ner:
            # Consideramos relevante para DPI: Pessoa ou dados Sensíveis (Saúde/Financeiro detectado via Regex ou NER)
            if "PESSOA" in resultados_ner or "SENSIVEL" in resultados_ner:
                return True
                
        return False

    def obter_todos_dpi(self, texto: str) -> Dict[str, Any]:
        """
        Retorna todos os detalhes das DPIs encontradas.

        Args:
            texto (str): O texto a ser analisado.

        Returns:
            Dict[str, Any]: Detalhes das DPIs encontradas.
        """
        res = self.detectar_com_regex(texto)
        res.update(self.detectar_com_ner(texto))
        return res
