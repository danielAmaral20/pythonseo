import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup

def check_urls(urls):
    try:
        response = requests.get(urls[0])
        main_status_code = response.status_code
    except Exception as e:
        main_status_code = str(e)

    results = []
    for url in urls:
        try:
            response = requests.get(url)
            status_code = response.status_code
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_index_tag = soup.find("meta", {"name": "robots", "content": "noindex"})
            canonical_tag = soup.find("link", {"rel": "canonical"})
            
            if meta_index_tag:
                has_noindex_tag = True
            else:
                has_noindex_tag = False
                
            if canonical_tag:
                canonical_url = canonical_tag.get("href")
                canonical_match = canonical_url == url
                if not canonical_match:
                    canonical_url_diff = canonical_url
                else:
                    canonical_url_diff = ""
            else:
                canonical_match = False
                canonical_url_diff = ""

            results.append((url, status_code, has_noindex_tag, canonical_match, canonical_url_diff))
        except Exception as e:
            results.append((url, str(e), False, False, ""))
    return main_status_code, results

def parse_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)
    urls = [child[0].text for child in root]
    return urls

def main():
    st.title("Verificador de Status Code, Meta Noindex e Canonical do Sitemap")

    sitemap_url = st.text_input("Insira a URL do sitemap.xml")

    if st.button("Verificar"):
        if sitemap_url:
            try:
                urls = parse_sitemap(sitemap_url)
                main_status_code, results = check_urls(urls)
                df = pd.DataFrame(results, columns=["URL", "Status Code", "Possui Noindex", "Canonical Correspondente", "Canonical Diferente"])
                
                # Mapeando valores booleanos para strings descritivas
                df["Possui Noindex"] = df["Possui Noindex"].map({True: "Possui Noindex", False: "Não possui Noindex"})
                df["Canonical Correspondente"] = df["Canonical Correspondente"].map({True: "Correspondente", False: "Diferente"})
                
                st.write("Status Code encontrados:", main_status_code)
                st.write(df)
            except Exception as e:
                st.error(f"Erro ao processar o sitemap: {e}")
        else:
            st.warning("Por favor, insira uma URL válida do sitemap.xml")

if __name__ == "__main__":
    main()
