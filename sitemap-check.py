import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

def check_urls(urls):
    results = []
    for url in urls:
        try:
            response = requests.get(url)
            status_code = response.status_code
            results.append((url, status_code))
        except Exception as e:
            results.append((url, str(e)))
    return results

def parse_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)
    urls = [child[0].text for child in root]
    return urls

def main():
    st.title("Verificador de Status Code do Sitemap")

    sitemap_url = st.text_input("Insira a URL do sitemap.xml")

    if st.button("Verificar"):
        if sitemap_url:
            try:
                urls = parse_sitemap(sitemap_url)
                results = check_urls(urls)
                df = pd.DataFrame(results, columns=["URL", "Status Code"])
                st.write(df)
            except Exception as e:
                st.error(f"Erro ao processar o sitemap: {e}")
        else:
            st.warning("Por favor, insira uma URL válida do sitemap.xml")

if __name__ == "__main__":
    main()
