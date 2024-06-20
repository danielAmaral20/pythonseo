import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Carregar os dados da planilha
@st.cache
def load_data(file_path):
    xl = pd.ExcelFile(file_path)
    sheets = {sheet_name: xl.parse(sheet_name) for sheet_name in xl.sheet_names}
    return sheets

def main():
    st.title('Análise de Dados de Rastreamento')

    file_path = st.file_uploader('Carregar planilha Excel', type=['xlsx'])
    if file_path is not None:
        sheets = load_data(file_path)
       
        # Análise da aba "Table"
        if 'Table' in sheets:
            table_df = sheets['Table']
           
            # Top 10 URLs mais requisitadas
            top_urls = table_df['URL'].value_counts().head(10)
            st.subheader('Top 10 URLs mais requisitadas:')
            st.write(top_urls)
           
            # Dia com mais solicitações
            table_df['Time'] = pd.to_datetime(table_df['Time'])
            day_with_most_requests = table_df['Time'].dt.date.value_counts().idxmax()
            st.subheader(f'Dia com mais solicitações: {day_with_most_requests}')

            # Intervalo horário com mais requisições
            table_df['Hour'] = table_df['Time'].dt.hour
            popular_hours = table_df['Hour'].value_counts().idxmax()
            st.subheader(f'Intervalo horário com mais requisições: {popular_hours}h')

        # Análise da aba "Chart"
        if 'Chart' in sheets:
            chart_df = sheets['Chart']
            chart_df['Date'] = pd.to_datetime(chart_df['Date'])
           
            # Melhor dia para atualizar ou publicar conteúdo
            best_day_for_content = chart_df.loc[chart_df['Total crawl requests'].idxmax(), 'Date'].date()
            st.subheader(f'Melhor dia para atualizar/publicar conteúdo: {best_day_for_content}')

            # Dia com pico em Total Crawl Requests
            peak_crawl_requests_day = chart_df.loc[chart_df['Total crawl requests'].idxmax(), 'Date'].date()
            st.subheader(f'Dia com pico em Total Crawl Requests: {peak_crawl_requests_day}')

            # Dia com pico em Total download size (Bytes)
            peak_download_size_day = chart_df.loc[chart_df['Total download size (Bytes)'].idxmax(), 'Date'].date()
            st.subheader(f'Dia com pico em Total download size (Bytes): {peak_download_size_day}')

            # Dia com pico em Average response time (ms)
            peak_response_time_day = chart_df.loc[chart_df['Average response time (ms)'].idxmax(), 'Date'].date()
            st.subheader(f'Dia com pico em Average response time (ms): {peak_response_time_day}')

    else:
        st.write('Por favor, carregue um arquivo Excel.')

if __name__ == "__main__":
    main()
