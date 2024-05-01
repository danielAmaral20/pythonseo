import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

# Função para exibir o JSON em formato de árvore
def pretty_print_json(json_str):
    parsed_json = json.loads(json_str)
    st.json(parsed_json)

# Função principal para o scraping
def scrape_json_from_url(url):
    # Fazendo o request para a página
    response = requests.get(url)

    # Parseando o HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrando todos os trechos de código
    code_blocks = soup.find_all("code")

    # Lista para armazenar os trechos de código JSON
    json_blocks = []

    # Iterando sobre os trechos de código
    for code_block in code_blocks:
        # Verificando se o trecho de código parece ser JSON
        try:
            json_data = json.loads(code_block.text)
            # Se o JSON foi carregado corretamente, adiciona à lista
            json_blocks.append(json.dumps(json_data, indent=4))
        except ValueError:
            pass

    return json_blocks

# Interface do usuário com Streamlit
st.title("Scraping de JSON em uma Página Web")
url = st.text_input("Insira a URL da página:")
if st.button("Executar Scraping"):
    if url:
        st.write("Extraindo JSON da URL:", url)
        json_blocks = scrape_json_from_url(url)
        if json_blocks:
            st.write("Trechos JSON encontrados:")
            for json_block in json_blocks:
                pretty_print_json(json_block)
        else:
            st.write("Nenhum trecho JSON encontrado na página.")
    else:
        st.write("Por favor, insira uma URL válida.")
