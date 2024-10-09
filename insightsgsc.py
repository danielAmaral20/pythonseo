import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import httplib2

# Função para autenticação e conexão com o Google Search Console
def authenticate_gsc(client_id, client_secret, oauth_scope, redirect_uri):
    flow = InstalledAppFlow.from_client_config({
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "scopes": [oauth_scope]
        }
    }, [oauth_scope])
    
    credentials = flow.run_local_server(port=0)
    service = build('searchconsole', 'v1', credentials=credentials)
    
    return service

# Função para buscar a lista de sites conectados
def get_site_list(service):
    site_list = service.sites().list().execute()
    all_sites = [site['siteUrl'] for site in site_list['siteEntry']]
    return all_sites

# Parâmetros de autenticação (insira suas credenciais)
CLIENT_ID = "seu_client_id"
CLIENT_SECRET = "seu_client_secret"
OAUTH_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

# Interface do Streamlit
st.title("Google Search Console Analyzer")

# Autenticação e conexão com a API
with st.spinner("Autenticando com o Google Search Console..."):
    service = authenticate_gsc(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)

# Obtenção da lista de sites
sites = get_site_list(service)

# Dropdown para seleção de site
selected_site = st.selectbox("Selecione um site para análise:", sites)

st.write(f"Você selecionou: {selected_site}")
