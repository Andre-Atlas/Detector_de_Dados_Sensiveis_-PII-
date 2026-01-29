import unittest
import sys
import os

# Adiciona o diretório raiz ao path para encontrar o módulo 'fontes'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fontes.detectores import DetectorDPI


class TestDetectorDPI(unittest.TestCase):
    def setUp(self):
        self.detector = DetectorDPI()

    def test_falsos_positivos_tecnicos(self):
        """Testa se o código ignora números que parecem PII mas são técnicos."""
        textos_seguros = [
            "O processo SEI nº 00001-00005678/2023-11 foi atualizado.",  # Formato similar a telefone/CPF
            "A temperatura da caldeira atingiu 120.345.678 graus.",  # Número grande formatado
            "Relatório técnico assinado por João Silva.",  # Nome isolado (Citação)
            "Acesse o banco de dados da Prefeitura de Brasília."  # Entidade comum
        ]
        for texto in textos_seguros:
            resultado = self.detector.analisar(texto)
            self.assertFalse(resultado['contem_dpi'], f"Falso positivo detectado em: {texto}")

    def test_positivos_reais(self):
        """Testa se o código detecta PIIs reais com validação matemática."""
        # CPF e CNPJ válidos (gerados para teste)
        casos_reais = [
            ("O CPF do cliente é 123.456.789-09.", 'CPF'),
            ("Entre em contato pelo e-mail suporte@empresa.com.br", 'Email'),
            ("A empresa detentora é o CNPJ 11.222.333/0001-81.", 'CNPJ'),
            ("Ligar para (61) 98888-7777 para confirmar os dados.", 'Telefone')
        ]
        for texto, tipo in casos_reais:
            resultado = self.detector.analisar(texto)
            self.assertTrue(resultado['contem_dpi'], f"Deveria detectar DPI em: {texto}")
            self.assertIn(tipo, resultado['evidencias'], f"Deveria identificar {tipo} em: {texto}")

    def test_validacao_matematica(self):
        """Garante que números aleatórios com formato de CPF/CNPJ sejam ignorados."""
        cpf_valido = "123.456.789-09"
        self.assertTrue(self.detector._validar_cpf_matematico(cpf_valido))
        
        cpf_invalido = "111.111.111-11"  # Passa na Regex, mas falha no Checksum
        self.assertFalse(self.detector._validar_cpf_matematico(cpf_invalido))

        cnpj_valido = "11.222.333/0001-81"
        self.assertTrue(self.detector._validar_cnpj_matematico(cnpj_valido))

        cnpj_invalido = "00.000.000/0000-00"
        self.assertFalse(self.detector._validar_cnpj_matematico(cnpj_invalido))

    def test_combinacao_de_alto_risco(self):
        """Testa se a lógica de 'Nível de Risco' funciona."""
        texto = "O usuário João Silva, portador do CPF 123.456.789-09, solicitou acesso."
        resultado = self.detector.analisar(texto)
        self.assertTrue(resultado['contem_dpi'])
        self.assertEqual(resultado['nivel_risco'], 'Alto')


if __name__ == '__main__':
    print("Iniciando bateria de testes para redução de falsos positivos...")
    unittest.main()