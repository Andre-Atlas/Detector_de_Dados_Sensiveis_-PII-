import streamlit as st
import pandas as pd
import os
import io
from fontes.detectores import DetectorDPI
from fontes.utilitarios import limpar_texto

def formatar_elementos_gui(dicionario_evidencias):
    """Converte o dicionário de evidências em uma string legível para a interface."""
    if not dicionario_evidencias:
        return ""
    itens = []
    for k, v in dicionario_evidencias.items():
        if isinstance(v, list):
            itens.append(f"{k}: {', '.join(map(str, v))}")
        else:
            itens.append(f"{k}: {v}")
    return " | ".join(itens)

def main():
    st.set_page_config(page_title="Detector de DPI - Participa DF", layout="wide")
    
    st.title("Detector Inteligente de Dados Pessoais (DPI)")
    st.markdown("""
    Esta ferramenta analisa pedidos de acesso à informação e identifica dados sensíveis automaticamente 
    utilizando múltiplas camadas de detecção (Regex, NLP e Heurísticas).
    """)

    # Sidebar - Configurações
    st.sidebar.header("Configurações")
    modelo = st.sidebar.selectbox(
        "Tamanho do Modelo NLP (Spacy)", 
        ["sm", "md", "lg"], 
        index=0,
        help="Modelos maiores são mais precisos, mas requerem mais memória e tempo de processamento."
    )

    estrito = st.sidebar.checkbox(
        "Filtragem Estrita",
        value=True,
        help="Se marcado, qualquer dado pessoal (incluindo nomes isolados) marcará o texto como PRIVADO. Se desmarcado, nomes isolados sem outros dados podem ser considerados PUBLICO."
    )
    
    # Inicializa o Detector com Cache para evitar recarregamento pesado do modelo NLP
    @st.cache_resource
    def carregar_detector(tamanho):
        return DetectorDPI(tamanho_modelo=tamanho)
    
    with st.spinner("Carregando inteligência de detecção..."):
        detector = carregar_detector(modelo)

    # Upload do Arquivo
    st.divider()
    st.subheader("1. Entrada de Dados")
    arquivo_upload = st.file_uploader("Selecione o arquivo (CSV, Excel ou TXT) para análise", type=["csv", "xlsx", "xls", "txt"])

    if arquivo_upload is not None:
        try:
            extensao = arquivo_upload.name.split('.')[-1].lower()
            
            if extensao in ['xlsx', 'xls']:
                df = pd.read_excel(arquivo_upload)
            elif extensao == 'txt':
                content = arquivo_upload.getvalue().decode('utf-8', errors='ignore')
                # Para TXT, tratamos cada linha como um registro
                linhas = [l.strip() for l in content.split('\n') if l.strip()]
                df = pd.DataFrame(linhas, columns=['Texto'])
            else:
                # CSV
                content = arquivo_upload.getvalue()
                try:
                    df = pd.read_csv(io.BytesIO(content), sep=None, engine='python', encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(io.BytesIO(content), sep=None, engine='python', encoding='iso-8859-1')
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return

        st.info(f"Arquivo carregado: **{len(df)}** registros encontrados.")
        
        # Seleção da coluna de texto
        colunas = df.columns.tolist()
        coluna_padrao = next((c for c in ['Texto Mascarado', 'Texto', 'texto', 'TEXTO'] if c in colunas), colunas[0])
        coluna_texto = st.selectbox("Selecione a coluna que contém o texto para análise:", colunas, index=colunas.index(coluna_padrao))

        if st.button("Iniciar Análise de Privacidade", type="primary"):
            resultados = []
            progresso_bar = st.progress(0)
            status_text = st.empty()
            
            for i, (idx, linha) in enumerate(df.iterrows()):
                texto = str(linha.get(coluna_texto, ''))
                texto_limpo = limpar_texto(texto)
                
                # Executa a detecção
                analise = detector.analisar(texto_limpo, estrito=estrito)
                
                # Lógica de Classificação
                classificacao = "PRIVADO" if analise['contem_dpi'] else "PUBLICO"
                
                # Formata evidências usando a lógica do projeto
                evidencias = formatar_elementos_gui(analise['evidencias'])
                
                nova_linha = linha.to_dict()
                nova_linha['Classificacao'] = classificacao
                nova_linha['Elementos_Encontrados'] = evidencias
                resultados.append(nova_linha)
                
                # Atualiza progresso
                percentual = (i + 1) / len(df)
                progresso_bar.progress(percentual)
                status_text.text(f"Processando: {i+1}/{len(df)}")

            status_text.success("Análise concluída com sucesso!")
            df_final = pd.DataFrame(resultados)
            
            # --- DASHBOARD DE RESULTADOS ---
            st.divider()
            st.subheader("2. Resumo da Análise")
            
            col1, col2, col3 = st.columns(3)
            total = len(df_final)
            privados = len(df_final[df_final['Classificacao'] == "PRIVADO"])
            publicos = total - privados
            
            col1.metric("Total de Pedidos", total)
            col2.metric("Pedidos com DPI", privados, delta=f"{(privados/total*100):.1f}%", delta_color="inverse")
            col3.metric("Pedidos Públicos", publicos, delta=f"{(publicos/total*100):.1f}%")

            # --- TABELA INTERATIVA ---
            st.subheader("3. Visualização Detalhada")
            st.dataframe(
                df_final, 
                use_container_width=True,
                column_config={
                    "Classificacao": st.column_config.TextColumn("Status", help="Privado se houver DPI, Público caso contrário"),
                    "Elementos_Encontrados": st.column_config.TextColumn("Evidências", width="large")
                }
            )

            # --- DOWNLOAD ---
            st.divider()
            csv_saida = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar Relatório de Auditoria (CSV)",
                data=csv_saida,
                file_name="resultado_dpi_gui.csv",
                mime="text/csv",
                help="Clique para baixar o arquivo com as classificações e evidências."
            )

if __name__ == "__main__":
    main()
