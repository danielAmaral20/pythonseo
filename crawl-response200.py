import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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
            
            # Top 10 URLs mais requisitadas com botão para visualização
            top_urls = table_df['URL'].value_counts().head(10)
            st.subheader('Top 10 URLs mais requisitadas:')
            for idx, (url, count) in enumerate(top_urls.items(), start=1):
                show_url = st.button(f'{idx}. Clique para mostrar a URL')
                if show_url:
                    st.write(url)

            # Dia com mais solicitações
            table_df['Time'] = pd.to_datetime(table_df['Time'])
            day_with_most_requests = table_df['Time'].dt.date.value_counts().idxmax()
            st.subheader(f'Dia com mais solicitações: {day_with_most_requests}')
            
            # Gráfico de desempenho dos dias em torno do dia com mais solicitações
            fig, ax = plt.subplots()
            request_counts = table_df['Time'].dt.date.value_counts()
            start_date = day_with_most_requests - timedelta(days=7)
            end_date = day_with_most_requests + timedelta(days=7)
            ax.bar(request_counts.index, request_counts.values, color='skyblue')
            ax.axvline(x=day_with_most_requests, color='red', linestyle='--', label='Dia com mais solicitações')
            ax.set_xlabel('Data')
            ax.set_ylabel('Número de solicitações')
            ax.set_title('Desempenho dos dias em torno do dia com mais solicitações')
            ax.legend()
            st.pyplot(fig)

        # Análise da aba "Chart"
        if 'Chart' in sheets:
            chart_df = sheets['Chart']
            chart_df['Date'] = pd.to_datetime(chart_df['Date'])
            
            # Melhor dia para atualizar ou publicar conteúdo
            best_day_index = chart_df['Total crawl requests'].idxmax()
            best_day = chart_df.loc[best_day_index, 'Date']
            best_day_weekday = best_day.strftime('%A')  # Dia da semana
            st.subheader(f'Melhor dia para atualizar/publicar conteúdo: {best_day.strftime("%d/%m/%Y")} ({best_day_weekday})')

            # Gráfico de desempenho em torno dos dias de pico
            metrics = ['Total crawl requests', 'Total download size (Bytes)', 'Average response time (ms)']
            for metric in metrics:
                peak_day_index = chart_df[metric].idxmax()
                peak_day = chart_df.loc[peak_day_index, 'Date']
                
                fig, ax = plt.subplots()
                ax.plot(chart_df['Date'], chart_df[metric], marker='o', linestyle='-', color='b', label=metric)
                ax.axvline(x=peak_day, color='red', linestyle='--', label=f'Dia com pico em {metric}')
                ax.set_xlabel('Data')
                ax.set_ylabel(metric)
                ax.set_title(f'Desempenho em torno do pico em {metric}')
                ax.legend()
                st.pyplot(fig)

    else:
        st.write('Por favor, carregue um arquivo Excel.')

if __name__ == "__main__":
    main()
