# Hackathon Participa DF - Categoria I (Acesso à Informação)

## 🧠 Projeto de Detecção de DPI (Dados Pessoais Identificáveis)

Este projeto foi desenvolvido para o **Hackathon Participa DF**, com o objetivo de identificar automaticamente dados pessoais (DPI - Dados Pessoais Identificáveis) em pedidos de acesso à informação. A solução utiliza uma abordagem multi-camadas (Regex, NLP e Heurísticas de Contexto) para maximizar o **F1-Score** e fornecer relatórios detalhados para auditoria.

### 📋 Funcionalidades de Detecção
- **Validação Matemática de CPF**: Reduz falsos positivos validando dígitos verificadores.
- **Contexto Semântico**: Identifica solicitações de anexos (CNH, RG, CPF) e menções a "meus dados", "minha conta", etc.
- **Dados Sensíveis (Saúde/Financeiro)**: Detecção de termos relacionados a laudos, exames, tratamentos e dados bancários.
- **Nome Completo**: Detectado via NLP (Spacy) com fallback para heurísticas em ambientes restritos.
- **Documentos e Contatos**: CPF, CNPJ, RG, Telefones e E-mails.
- **Localização**: Identificação de logradouros e endereços.

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
│   └── testar_detectores.py   # Testes unitários abrangentes
│
├── main.py                    # Script principal de execução e auditoria
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação (esta aqui)
```

---

### 🛠️ Tecnologias Utilizadas
- **Python 3.9+**
- **Pandas & Numpy**: Manipulação de dados em larga escala.
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
python -m venv venv
.\venv\Scripts\activate  # No Windows
pip install -r requirements.txt
```

---

### 💻 Como Executar

#### 1. Execução do Detector (Com Auditoria)
O script gera um relatório completo com classificação e as evidências encontradas.

**Comando:**
```bash
python main.py data/AMOSTRA_e-SIC.csv --saida resultado_analise.csv
```

#### 2. Execução dos Testes
```bash
python testes/testar_detectores.py
```

---

### 📊 Formato dos Dados

#### Saída (CSV)
O arquivo gerado contém as colunas originais e duas novas colunas cruciais para auditoria:
- **`Classificacao`**: "PRIVADO" (se contiver DPI) ou "PUBLICO".
- **`Elementos_Encontrados`**: Justificativa detalhada listando os tipos de dados e os valores detectados (ex: `CPF: 123... | Contexto: saúde`).

---

### 📈 Diferenciais da Solução
1. **Detecção de Contexto**: Captura casos onde o dado não está explícito mas o documento é sensível (ex: "segue anexo meu RG").
2. **Precisão Matemática**: Validação de CPF evita que números aleatórios de protocolos sejam marcados como dados pessoais.
3. **Resiliência**: Fallback automático para heurísticas caso modelos de NLP pesados não possam ser carregados no ambiente.

---
**Autor:** André Acioli (Engenheiro de Software-ucb)
**Hackathon Participa DF 2026**
