import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Função para carregar e processar dados
@st.cache
def load_data(file):
    df = pd.read_excel(file)
    return df

# Função para realizar a clusterização
def cluster_data(df, num_clusters):
    # Vetorização dos textos
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df.iloc[:, 0])
    
    # Aplicação do KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    df['Cluster'] = kmeans.fit_predict(X)
    
    return df

# Função para calcular os volumes totais por cluster
def calculate_cluster_volumes(df):
    clusters = df['Cluster'].unique()
    cluster_info = []
    
    for cluster in clusters:
        cluster_df = df[df['Cluster'] == cluster]
        total_clicks = cluster_df['Cliques'].sum()
        total_impressions = cluster_df['Impressões'].sum()
        cluster_name = f"Cluster {cluster}"
        
        cluster_info.append({
            'Nome do Cluster': cluster_name,
            'Volume Total de Cliques': total_clicks,
            'Volume Total de Impressões': total_impressions,
            'Dados': cluster_df
        })
    
    return cluster_info

# Interface Streamlit
st.title('Análise de Clusters de Consultas')

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha a planilha Excel", type="xlsx")

if uploaded_file:
    # Carregar os dados
    df = load_data(uploaded_file)
    
    # Número de clusters (pode ser ajustado ou tornar uma entrada do usuário)
    num_clusters = st.slider("Número de clusters", min_value=2, max_value=20, value=5)
    
    # Clusterizar dados
    df_clustered = cluster_data(df, num_clusters)
    
    # Calcular volumes por cluster
    cluster_info = calculate_cluster_volumes(df_clustered)
    
    # Exibir informações de clusters
    for cluster in cluster_info:
        st.header(cluster['Nome do Cluster'])
        st.write(f"Volume Total de Cliques: {cluster['Volume Total de Cliques']}")
        st.write(f"Volume Total de Impressões: {cluster['Volume Total de Impressões']}")
        st.write("Dados do Cluster:")
        st.dataframe(cluster['Dados'])

# Executar o app com 'streamlit run nome_do_script.py'
