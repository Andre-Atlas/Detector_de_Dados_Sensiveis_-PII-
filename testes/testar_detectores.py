import unittest
import sys
import os

# Adiciona o diretório fontes ao path para os imports funcionarem
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'fontes'))

from detectores import DetectorDPI

class TestarDetectorDPI(unittest.TestCase):
    """
    Testes unitários para validar a detecção de DPI via Regex e lógica de negócio.
    """
    
    def setUp(self):
        self.detector = DetectorDPI()

    def testar_deteccao_cpf(self):
        self.assertTrue(self.detector.tem_dpi("Meu CPF é 123.456.789-00"))
        self.assertTrue(self.detector.tem_dpi("CPF 12345678900 sem pontos"))
        self.assertFalse(self.detector.tem_dpi("Número aleatório 12345"))

    def testar_deteccao_email(self):
        self.assertTrue(self.detector.tem_dpi("Contato via teste@exemplo.com.br"))
        self.assertTrue(self.detector.tem_dpi("email: joao.silva@gmail.com"))

    def testar_deteccao_telefone(self):
        self.assertTrue(self.detector.tem_dpi("Ligue para (61) 98888-7777"))
        self.assertTrue(self.detector.tem_dpi("Telefone 6133221100"))

    def testar_deteccao_rg(self):
        # Padrão simplificado de RG que definimos
        self.assertTrue(self.detector.tem_dpi("RG 1.234.567-X"))
        self.assertTrue(self.detector.tem_dpi("Identidade 1234567"))

    def testar_deteccao_cnpj(self):
        self.assertTrue(self.detector.tem_dpi("Empresa CNPJ 12.345.678/0001-99"))

    def testar_sem_dpi(self):
        self.assertFalse(self.detector.tem_dpi("Gostaria de solicitar informações sobre o orçamento da transparência."))
        self.assertFalse(self.detector.tem_dpi("Como faço para acessar o portal da transparência?"))

    def testar_deteccao_endereco(self):
        self.assertTrue(self.detector.tem_dpi("Moro na Rua das Flores, 123"))
        self.assertTrue(self.detector.tem_dpi("Local: Avenida Central nº 500"))

    def testar_deteccao_saude_sensivel(self):
        self.assertTrue(self.detector.tem_dpi("Solicito meu laudo médico de ontem"))
        self.assertTrue(self.detector.tem_dpi("Preciso de informações sobre meu tratamento de saúde"))

    def testar_deteccao_financeiro(self):
        self.assertTrue(self.detector.tem_dpi("Minha conta bancária é 12345-6"))
        self.assertTrue(self.detector.tem_dpi("O valor do meu salário é R$ 5000"))

    def testar_deteccao_nome_pessoa(self):
        self.assertTrue(self.detector.tem_dpi("João Silva solicitou este documento"))
        # Não deve detectar se for início de frase isolado (heurística conservadora)
        self.assertFalse(self.detector.tem_dpi("Gostaria de saber o prazo."))

if __name__ == "__main__":
    unittest.main()
