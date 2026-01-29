# Hackathon Participa DF - Categoria I (Acesso à Informação)

## 🧠 Projeto de Detecção de DPI (Dados Pessoais Identificáveis)

Este projeto foi desenvolvido para o **Hackathon Participa DF**, com o objetivo de identificar automaticamente dados pessoais (DPI - Dados Pessoais Identificáveis) em pedidos de acesso à informação. A solução utiliza uma abordagem multi-camadas (Regex, NLP e Heurísticas de Contexto) de modo a fornecer relatórios detalhados para auditoria.

### 📋 Funcionalidades de Detecção

A solução opera em três camadas de proteção para garantir a privacidade dos dados:

1.  **Camada de Validação Algorítmica (Alta Precisão)**:
    - **CPF**: Detecção via Regex com validação matemática de dígitos verificadores (Checksum).
    - **CNPJ**: Validação de estrutura empresarial e verificação matemática.
    - **E-mails**: Padrões RFC estruturados.
2.  **Camada de Reconhecimento de Entidades (NLP)**:
    - **Nomes Próprios**: Utiliza o modelo `pt_core_news_sm` do Spacy para identificar nomes de pessoas em contextos variados.
    - **Fallback Inteligente**: Caso o modelo Spacy não esteja disponível, o sistema aciona automaticamente uma heurística baseada em padrões de capitalização.
3.  **Camada de Contexto e Heurística**:
    - **Documentos**: RG e Identidade (identifica menções próximas ao número).
    - **Localização**: Identificação de logradouros (Rua, Av, etc).
    - **Financeiro**: Detecção de termos como "Banco", "Agência", "PIX" e "Conta Corrente" seguidos de numeração.
    - **Telefones**: Padrões nacionais (com DDD) filtrados para evitar confusão com números de protocolo (ex: SEI).

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
│   ├── carregador_dados.py    # Carregamento robusto de CSV
│   ├── detectores.py          # Core: Lógica de Regex, NLP e Contexto
│   └── utilitarios.py         # Auxiliares (limpeza de texto)
│
├── /testes
│   └── TestDetectorDPI.py     # Testes unitários abrangentes
│
├── main.py                    # Script principal de execução e auditoria
├── requirements.txt           # Dependências do projeto
├── resultado_dpi.csv          # Exemplo de resultado gerado
└── README.md                  # Documentação (esta aqui)
```

---

### 🛠️ Tecnologias Utilizadas
- **Python 3.9+**
- **Pandas**: Manipulação de dados em CSV.
- **Spacy**: Processamento de Linguagem Natural para NER.
- **Tqdm**: Monitoramento de progresso em tempo real.
- **Regex**: Padrões estruturados otimizados.

---

### 🚀 Instalação e Configuração

#### 1. Pré-requisitos
- Python 3.9 ou superior.
- Pip atualizado.

#### 2. Configuração do Ambiente
```powershell
python -m venv .venv
.\.venv\Scripts\activate  # No Windows
pip install -r requirements.txt
```

---

### 💻 Como Executar

#### 1. Execução Simplificada (Interface Gráfica)
Agora o projeto inicia automaticamente a interface gráfica caso nenhum parâmetro seja passado:
```powershell
python main.py
```

#### 2. Execução da Interface Gráfica (Manual)
Para abrir diretamente via Streamlit:
```powershell
streamlit run interface_gui.py
```

#### 3. Execução via Linha de Comando (CLI)
Para processar arquivos em lote e gerar relatórios automaticamente:
```powershell
python main.py data\AMOSTRA_e-SIC.csv --saida resultado_dpi.csv
```

#### 4. Execução dos Testes
```powershell
python -m unittest testes\TestDetectorDPI.py
```

---

### 📈 Diferenciais e Inteligência

1.  **Suporte Multi-formato**: A interface gráfica agora aceita arquivos **CSV**, **Excel (.xlsx, .xls)** e **Texto (.txt)**.
2.  **Redução de Falsos Positivos**: 
    - Validação matemática (Checksum) para CPF/CNPJ.
    - Filtro de **Entidades Comuns**: Ignora termos técnicos e órgãos públicos (ex: "Governo", "Ministério", "Hospital") que poderiam ser confundidos com nomes.
    - **Análise de Risco**: Um nome isolado em um texto técnico pode não ser DPI, mas um nome acompanhado de um CPF eleva o `nivel_risco` para **"Alto"**.
3.  **Robustez de Carregamento**:
    - Detecção automática de delimitadores em CSV.
    - Suporte a múltiplas codificações (`UTF-8`, `ISO-8859-1`, etc).
4.  **Auditabilidade Total**:
    - Geração de relatório com a coluna `Elementos_Encontrados`, detalhando exatamente o que foi visto.

---
**Autor:** André Acioli (Engenheiro de Software-ucb)
**Hackathon Participa DF 2026**
