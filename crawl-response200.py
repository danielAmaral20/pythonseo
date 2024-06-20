import streamlit as st
import pandas as pd

# Função para carregar os dados da planilha
@st.cache
def load_data(file_path):
    # Carregar dados das duas abas
    chart_data = pd.read_excel(file_path, sheet_name='Chart Date')
    table_data = pd.read_excel(file_path, sheet_name='Table Time')
    return chart_data, table_data

# Função para gerar insights
def generate_insights(chart_data, table_data):
    # Convertendo a coluna de datas para datetime
    table_data['Date'] = pd.to_datetime(table_data['Date'])
    chart_data['Chart Date'] = pd.to_datetime(chart_data['Chart Date'])
    
    # Top 10 URLs mais requisitadas
    top_10_urls = table_data['URL'].value_counts().head(10).reset_index()
    top_10_urls.columns = ['URL', 'Requisições']
    
    # Dia com mais solicitações
    dia_mais_solicitacoes = table_data['Date'].dt.date.value_counts().idxmax()
    
    # Intervalo horário com mais requisições
    table_data['Hour'] = table_data['Date'].dt.hour
    intervalo_mais_requisicoes = table_data['Hour'].value_counts().idxmax()
    
    # Melhor dia para atualizar ou publicar conteúdo
    melhor_dia_publicar = dia_mais_solicitacoes
    
    # Picos das métricas
    pico_crawl_requests = chart_data.loc[chart_data['Total crawl requests'].idxmax()]
    pico_download_size = chart_data.loc[chart_data['Total download size (Bytes)'].idxmax()]
    pico_response_time = chart_data.loc[chart_data['Average response time (ms)'].idxmax()]
    
    return top_10_urls, dia_mais_solicitacoes, intervalo_mais_requisicoes, melhor_dia_publicar, pico_crawl_requests, pico_download_size, pico_response_time

# Configuração do Streamlit
st.title("Análise de Rastreamento de URLs")
file_upload = st.file_uploader("Faça upload da planilha Excel", type=["xlsx"])

if file_upload is not None:
    chart_data, table_data = load_data(file_upload)
    top_10_urls, dia_mais_solicitacoes, intervalo_mais_requisicoes, melhor_dia_publicar, pico_crawl_requests, pico_download_size, pico_response_time = generate_insights(chart_data, table_data)
    
    st.header("Top 10 URLs mais requisitadas")
    st.table(top_10_urls)
    
    st.header("Dia com mais solicitações")
    st.write(dia_mais_solicitacoes)
    
    st.header("Intervalo horário com mais requisições")
    st.write(f"{intervalo_mais_requisicoes}:00 - {intervalo_mais_requisicoes}:59")
    
    st.header("Melhor dia para atualizar ou publicar conteúdo")
    st.write(melhor_dia_publicar)
    
    st.header("Picos das métricas")
    st.write("Pico de Total Crawl Requests:", pico_crawl_requests['Chart Date'], "com", pico_crawl_requests['Total crawl requests'], "requisições")
    st.write("Pico de Total Download Size:", pico_download_size['Chart Date'], "com", pico_download_size['Total download size (Bytes)'], "Bytes")
    st.write("Pico de Average Response Time:", pico_response_time['Chart Date'], "com", pico_response_time['Average response time (ms)'], "ms")
