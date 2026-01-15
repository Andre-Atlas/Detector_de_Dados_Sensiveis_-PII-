# Hackathon Participa DF - Categoria I (Acesso à Informação)

## 🧠 Projeto de Detecção de DPI (Dados Pessoais Identificáveis)

Este projeto foi desenvolvido para o **Hackathon Participa DF**, com o objetivo de identificar automaticamente dados pessoais (DPI - Dados Pessoais Identificáveis) em pedidos de acesso à informação. A solução foca em maximizar o **F1-Score**, equilibrando Precisão e Sensibilidade (Recall) para garantir a conformidade com a LGPD sem gerar excesso de falsos positivos.

### 📋 Definição de Dados Pessoais Cobertos
- **Nome Completo**: Detectado via heurística de Entidade Nomeada (NER).
- **Documentos**: CPF, CNPJ e RG (vários formatos).
- **Contatos**: Telefones (celular e fixo) e E-mail.
- **Localização**: Endereços (Ruas, Avenidas, Quadras, etc).
- **Dados Sensíveis**: Identificação de termos relacionados a Saúde e Financeiro (exames, bancos, contas).

---

### 📂 Estrutura do Projeto

```text
/projeto-acesso-informacao
│
├── /data
│   └── AMOSTRA_e-SIC.csv      # Base de dados de entrada
│
├── /fontes
│   ├── __init__.py
│   ├── carregador_dados.py    # Carregamento e limpeza do CSV
│   ├── detectores.py          # Core: Lógica de Regex e NER
│   └── utilitarios.py         # Auxiliares (limpeza de texto, formatação)
│
├── /testes
│   └── testar_detectores.py   # Testes automatizados para validação
│
├── main.py                    # Script principal de execução
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação (esta aqui)
```

---

### 🛠️ Tecnologias Utilizadas
- **Python 3.9+** (Recomendado 3.12)
- **Pandas**: Manipulação eficiente de grandes volumes de dados.
- **Regex**: Padrões estruturados de alta performance para documentos brasileiros.
- **Unittest**: Garantia de qualidade e regressão.

---

### 🚀 Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e executar o projeto:

#### 1. Pré-requisitos
- **Python 3.9** ou superior instalado.
- Gerenciador de pacotes **pip** atualizado.

#### 2. Criação do Ambiente Virtual (Recomendado)
Para evitar conflitos com outras bibliotecas do sistema:
```powershell
# No Windows
python -m venv venv
.\venv\Scripts\activate

# No Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalação das Dependências
```bash
pip install -r requirements.txt
```

---

### 💻 Como Executar

#### 1. Execução do Detector
O script principal aceita o caminho do arquivo de entrada e opcionalmente o nome do arquivo de saída.

**Comando:**
```bash
python main.py data/AMOSTRA_e-SIC.csv --saida resultado_dpi.csv
```

**Parâmetros:**
- `entrada`: (Obrigatório) Caminho para o arquivo CSV contendo os textos a serem analisados.
- `--saida`: (Opcional) Nome do arquivo CSV que será gerado com os resultados (Padrão: `resultado_dpi.csv`).

#### 2. Execução dos Testes
Para validar a precisão dos detectores:
```bash
python testes/testar_detectores.py
```

---

### 📊 Formato dos Dados

#### Entrada (CSV)
O arquivo de entrada deve ser um CSV (separado por vírgula ou ponto e vírgula) contendo ao menos uma das seguintes colunas de texto:
- `Texto`
- `Texto Mascarado`
- `texto`
- `TEXTO`

#### Saída (CSV)
O script gera um novo arquivo CSV contendo todas as colunas originais acrescidas de uma nova coluna:
- `Contem_DPI`: Indica "Sim" se o texto contém dados pessoais identificáveis ou sensíveis, e "Não" caso contrário.

---

### 📈 Diferenciais da Solução
1. **Robustez no Carregamento**: O `carregador_dados.py` trata CSVs com quebras de linha internas e caracteres especiais, comuns em pedidos de informação informais.
2. **Máxima Sensibilidade (P1)**: Implementação de múltiplas camadas de detecção (Regex + Heurísticas NER) para garantir que nenhum dado sensível (Saúde, Financeiro) ou identificador pessoal passe despercebido.
3. **Qualidade de Código (P2)**: Código modular, extensível, com 100% de cobertura de testes nos detectores principais e documentação detalhada em todas as funções.

---
**Autor:** André Acioli (Engenheiro de Software-ucb)
**Hackathon Participa DF 2026**
