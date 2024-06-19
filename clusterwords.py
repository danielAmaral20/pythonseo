import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Lista de stop words em português
stop_words_pt = [
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com",
    "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como",
    "mas", "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser",
    "quando", "muito", "há", "nos", "já", "está", "eu", "também", "só", "pelo",
    "pela", "até", "isso", "ela", "entre", "depois", "sem", "mesmo", "aos",
    "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha",
    "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa",
    "pelos", "elas", "havia", "seja", "qual", "será", "nós", "tenho", "lhe",
    "deles", "essas", "esses", "pelas", "este", "fosse", "dele", "tu", "te",
    "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas",
    "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes",
    "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou",
    "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram",
    "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja",
    "estejamos", "estejam", "estivesse", "estivéssemos", "estivessem", "estiver",
    "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos",
    "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse",
    "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei",
    "houverá", "houveremos", "houverão", "houveria", "houveríamos", "houveriam",
    "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram",
    "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem",
    "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria", "seríamos",
    "seriam", "tenho", "tem", "temos", "têm", "tinha", "tínhamos", "tinham", "tive",
    "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham",
    "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei",
    "terá", "teremos", "terão", "teria", "teríamos", "teriam"
]

# Função para carregar e processar dados
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    return df

# Função para realizar a clusterização
def cluster_data(df, num_clusters):
    # Vetorização dos textos
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt)
    X = vectorizer.fit_transform(df.iloc[:, 0])
    
    # Aplicação do KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    df['Cluster'] = kmeans.fit_predict(X)
    
    return df, kmeans, vectorizer

# Função para calcular os volumes totais por cluster e identificar o termo agregador
def calculate_cluster_volumes(df, kmeans, vectorizer):
    clusters = df['Cluster'].unique()
    cluster_info = []
    
    # Obter os termos mais representativos para cada cluster
    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    for cluster in clusters:
        cluster_df = df[df['Cluster'] == cluster]
        total_clicks = cluster_df['Cliques'].sum()
        total_impressions = cluster_df['Impressões'].sum()
        
        # Identificar os principais termos para o cluster
        top_terms = [terms[ind] for ind in order_centroids[cluster, :10]]
        cluster_name = f"Cluster {cluster} - Termo Agregador: {top_terms[0]}"
        
        cluster_info.append({
            'Nome do Cluster': cluster_name,
            'Volume Total de Cliques': total_clicks,
            'Volume Total de Impressões': total_impressions,
            'Dados': cluster_df,
            'Termos': top_terms
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
    df_clustered, kmeans, vectorizer = cluster_data(df, num_clusters)
    
    # Calcular volumes por cluster e identificar o termo agregador
    cluster_info = calculate_cluster_volumes(df_clustered, kmeans, vectorizer)
    
    # Exibir informações de clusters
    for cluster in cluster_info:
        st.header(cluster['Nome do Cluster'])
        st.write(f"Volume Total de Cliques: {cluster['Volume Total de Cliques']}")
        st.write(f"Volume Total de Impressões: {cluster['Volume Total de Impressões']}")
        st.write(f"Principais Termos: {', '.join(cluster['Termos'])}")
        st.write("Dados do Cluster:")
        st.dataframe(cluster['Dados'])

# Executar o app com 'streamlit run nome_do_script.py'
