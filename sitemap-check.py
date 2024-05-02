import streamlit as st
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# Função para verificar o status code de uma URL
def verificar_status(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException:
        return "Erro ao acessar a URL"

# Função para analisar o sitemap e verificar conformidade
def analisar_sitemap(xml_content):
    try:
        conformidade_global = True
        ajustes_globais = []

        root = ET.fromstring(xml_content)
        urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")

        for u in urls:
            # Verificar status code
            status_code = verificar_status(u.text)
            if status_code != 200:
                conformidade_global = False
                ajustes_globais.append(f"A URL {u.text} retornou o status code {status_code}")

            # Verificar canonical
            page_response = requests.get(u.text)
            page_soup = BeautifulSoup(page_response.content, "html.parser")
            canonical_tag = page_soup.find("link", rel="canonical")
            if canonical_tag:
                canonical_url = canonical_tag.get("href")
                if canonical_url != u.text:
                    ajustes_globais.append(f"A URL {u.text} não possui a versão canônica da URL informada no sitemap")

            # Verificar se há tag noindex
            noindex_tag = page_soup.find("meta", attrs={"name": "robots", "content": "noindex"})
            if noindex_tag:
                ajustes_globais.append(f"A URL {u.text} está no sitemap, mas possui a tag noindex para impedir a indexação")

        return conformidade_global, ajustes_globais

    except requests.exceptions.RequestException:
        return False, ["Erro ao acessar o sitemap"]

# Interface do Streamlit
st.title("Analisador de Sitemap")

uploaded_file = st.file_uploader("Carregar arquivo XML do sitemap", type="xml")

if uploaded_file is not None:
    xml_content = uploaded_file.read().decode("utf-8")
    st.write(f"Analisando sitemap...")

    conformidade_global, ajustes_globais = analisar_sitemap(xml_content)

    if conformidade_global:
        st.success("O sitemap está em conformidade!")
    else:
        st.error("O sitemap não está em conformidade. Ajustes necessários:")
        for ajuste in ajustes_globais:
            st.write(ajuste)
