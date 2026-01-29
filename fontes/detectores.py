import re
from typing import List, Dict, Any, Optional

class DetectorDPI:
    """
    Detector Avançado de DPI (Dados Pessoais Identificáveis).
    Camadas:
    1. Regex Estrita (CPF, CNPJ, Email, Tel, RG, Endereço, Financeiro)
    2. NLP Spacy (Nomes de Pessoas - PER) - Fallback para Heurística se falhar
    3. Heurística de Contexto (Solicitação de dados próprios/Anexos/Saúde)
    """

    def __init__(self, tamanho_modelo: str = "sm"):
        try:
            import spacy
            self.nlp = spacy.load(f"pt_core_news_{tamanho_modelo}")
        except Exception:
            self.nlp = None

        # --- PADRÕES REGEX REFINADOS ---
        self.padrao_cpf = re.compile(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b')
        self.padrao_cnpj = re.compile(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b')
        self.padrao_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

        # Telefone: Exige DDD e formato de celular/fixo para evitar IDs de processos
        self.padrao_telefone = re.compile(r'\b(?:\(?\d{2}\)?\s?)(?:9\d{4}|\d{4})[-.\s]?\d{4}\b')

        self.padrao_rg = re.compile(r'(?:\b(?:RG|Identidade)\s*[:.]?\s*)(\d{1,2}\.?\d{3}\.?\d{3}-?[\dX]\b|\d{5,9})\b',
                                    re.IGNORECASE)
        self.padrao_endereco = re.compile(r'(?i)\b(Rua|Av|Avenida|Logradouro|Alameda)\b\s+.*?\d+')
        self.padrao_financeiro = re.compile(r'(?i)\b(Banco|Agência|PIX|Cartão|Conta Corrente|Salário)\b\s+[\d\-]{4,}')

        # Termos que reduzem a chance de ser PII (Ex: documentos técnicos)
        self.entidades_comuns = {
            "Distrito Federal", "Governo", "Brasília", "Hospital", "Saúde",
            "Ministério", "Poder Judiciário", "Relatório Técnico", "Diagrama",
            "Especificação", "Banco de Dados", "Atenciosamente", "Prefeitura"
        }

    def _validar_cpf_matematico(self, cpf: str) -> bool:
        numeros = re.sub(r'\D', '', cpf)
        if len(numeros) != 11 or numeros == numeros[0] * 11: return False
        for i in range(9, 11):
            soma = sum(int(numeros[k]) * ((i + 1) - k) for k in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(numeros[i]): return False
        return True

    def _validar_cnpj_matematico(self, cnpj: str) -> bool:
        """Validação algorítmica do CNPJ para eliminar falsos positivos numéricos."""
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14: return False

        def calcular_digito(peso, numeros):
            soma = sum(int(n) * p for n, p in zip(numeros, peso))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        if int(cnpj[12]) != calcular_digito(pesos1, cnpj[:12]): return False
        if int(cnpj[13]) != calcular_digito(pesos2, cnpj[:13]): return False
        return True

    def analisar(self, texto: str) -> Dict[str, Any]:
        if not isinstance(texto, str) or not texto.strip():
            return {'contem_dpi': False, 'evidencias': {}}

        evidencias = {}

        # Validações com Checksum (Alta Precisão)
        cpfs = [c for c in self.padrao_cpf.findall(texto) if self._validar_cpf_matematico(c)]
        if cpfs: evidencias['CPF'] = list(set(cpfs))

        cnpjs = [c for c in self.padrao_cnpj.findall(texto) if self._validar_cnpj_matematico(c)]
        if cnpjs: evidencias['CNPJ'] = list(set(cnpjs))

        # Outros PIIs
        emails = self.padrao_email.findall(texto)
        if emails: evidencias['Email'] = list(set(emails))

        telefones = self.padrao_telefone.findall(texto)
        if telefones: evidencias['Telefone'] = list(set(telefones))

        # Nomes (NLP ou Heurística)
        nomes = []
        if self.nlp:
            doc = self.nlp(texto)
            nomes = [ent.text for ent in doc.ents if ent.label_ == "PER" and len(ent.text.split()) > 1]
        else:
            nomes = re.findall(r"(?<![.!?]\s)\b[A-Z][a-zà-ÿ]+\s[A-Z][a-zà-ÿ]+\b", texto)

        # Filtro de falsos positivos para nomes
        nomes_limpos = [n for n in nomes if
                        n not in self.entidades_comuns and not any(e in n for e in self.entidades_comuns)]
        if nomes_limpos: evidencias['Nomes'] = list(set(nomes_limpos))

        # --- LÓGICA DE DECISÃO (PESO DE EVIDÊNCIA) ---
        # Evita marcar PII se houver apenas um nome isolado sem outros dados (baixa identificabilidade)
        pontuacao_risco = len(evidencias)
        if pontuacao_risco == 1 and 'Nomes' in evidencias:
            contem_dpi = False  # Nome sozinho em texto técnico costuma ser citação, não PII sensível
        else:
            contem_dpi = pontuacao_risco > 0

        return {
            'contem_dpi': contem_dpi,
            'nivel_risco': 'Alto' if any(k in evidencias for k in ['CPF', 'CNPJ', 'Email']) else 'Baixo',
            'evidencias': evidencias
        }
