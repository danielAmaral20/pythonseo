import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
    
    # Exibe o link de autenticação manual no Streamlit
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url, flow

# Função para buscar a lista de sites conectados
def get_site_list(service):
    site_list = service.sites().list().execute()
    all_sites = [site['siteUrl'] for site in site_list['siteEntry']]
    return all_sites

# Parâmetros de autenticação (insira suas credenciais)
CLIENT_ID = "1034169525900-rst8a3hkncdr2d0kad22an6pvvnvhlin.apps.googleusercontent.com"
CLIENT_SECRET = "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"
OAUTH_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
REDIRECT_URI = "https://seodatainsights.streamlit.app/"

# Interface do Streamlit
st.title("Google Search Console Analyzer")

# Botão para iniciar a autenticação
if "auth_flow" not in st.session_state:
    st.session_state.auth_flow = None

if st.button("Conectar com Google Search Console"):
    auth_url, flow = authenticate_gsc(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    st.session_state.auth_flow = flow
    st.write(f"Autentique-se visitando o seguinte link: [Login Google]({auth_url})")

# Input para o código de autenticação
auth_code = st.text_input("Digite o código de autenticação:")

# Conexão após a autenticação
if auth_code and st.session_state.auth_flow:
    flow = st.session_state.auth_flow
    flow.fetch_token(code=auth_code)
    service = build('searchconsole', 'v1', credentials=flow.credentials)

    # Obtenção da lista de sites
    sites = get_site_list(service)

    # Dropdown para seleção de site
    selected_site = st.selectbox("Selecione um site para análise:", sites)

    st.write(f"Você selecionou: {selected_site}")
