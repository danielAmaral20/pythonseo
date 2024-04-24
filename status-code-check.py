import streamlit as st
import requests

def check_https_status(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return "Online e seguro"
        elif response.status_code == 301 or response.status_code == 302:
            return "Redirecionado"
        else:
            return "Offline ou não seguro"
    except requests.exceptions.RequestException:
        return "Erro de conexão"

def main():
    st.title("Validador de status HTTPS")

    st.write("Este aplicativo verifica o status HTTPS de uma lista de URLs.")

    urls = st.text_area("Insira as URLs uma por linha")

    if st.button("Verificar"):
        urls_list = urls.split("\n")
        for url in urls_list:
            if url.strip():
                status = check_https_status(url.strip())
                st.write(f"{url}: {status}")

if __name__ == "__main__":
    main()
