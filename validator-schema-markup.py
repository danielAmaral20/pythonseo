import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import spacy
from collections import Counter
import matplotlib.pyplot as plt

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load("pt_core_news_sm")

# Função para extrair entidades do texto usando spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ != '']
    return entities

# Função para exibir o JSON em formato de árvore
def pretty_print_json(json_str):
    try:
        parsed_json = json.loads(json_str)
        st.json(parsed_json)
    except json.JSONDecodeError as e:
        st.error(f"Erro ao analisar JSON: {e}")

# Função principal para o scraping
def scrape_json_from_url(url):
    # Fazendo o request para a página
    response = requests.get(url)

    # Parseando o HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrando todos os trechos de código
    code_blocks = soup.find_all("script", type="application/ld+json")

    # Lista para armazenar os trechos de código JSON
    json_blocks = []

    # Iterando sobre os trechos de código
    for code_block in code_blocks:
        # Verificando se o trecho de código parece ser JSON
        try:
            json_data = json.loads(code_block.string)
            # Se o JSON foi carregado corretamente, adiciona à lista
            json_blocks.append(json.dumps(json_data, indent=4))
        except ValueError:
            pass

    return json_blocks

# Função para validar e corrigir a sintaxe do JSON
def validate_json_syntax(json_str):
    try:
        json.loads(json_str)
        return "A sintaxe do JSON está correta."
    except json.JSONDecodeError as e:
        return f"Erro ao analisar JSON: {e}"

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
                st.write("Dicas de correção de sintaxe:")
                st.write(validate_json_syntax(json_block))

            # Processar entidades NLP e gerar gráfico e tabela
            st.write("Analisando entidades do JSON:")
            all_entities = []
            for json_block in json_blocks:
                parsed_json = json.loads(json_block)
                for key, value in parsed_json.items():
                    if isinstance(value, str):
                        all_entities.extend(extract_entities(value))

            # Contagem de entidades
            entity_counter = Counter(all_entities)
            entities, counts = zip(*entity_counter.most_common(10))

            # Gerar gráfico de barras
            plt.barh(entities, counts)
            plt.xlabel('Frequência')
            plt.ylabel('Entidades')
            plt.title('Entidades mais frequentes no JSON')
            st.pyplot()

            # Gerar tabela de entidades
            st.write("Tabela de entidades mais frequentes:")
            st.write("| Entidade | Frequência |")
            st.write("| -------- | ---------- |")
            for entity, count in zip(entities, counts):
                st.write(f"| {entity} | {count} |")

        else:
            st.write("Nenhum trecho JSON encontrado na página.")
    else:
        st.write("Por favor, insira uma URL válida.")
