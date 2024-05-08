import streamlit as st
import pandas as pd
import advertools as adv

def generate_campaigns(products, words):
    kw_df = adv.kw_generate(products, words)
    return kw_df

def main():
    st.title("Gerador de Sugestões de Campanhas SEM")
    
    st.write("Insira os termos relacionados ao produto:")
    products_input = st.text_area("Termos relacionados ao produto (separados por vírgula)")
    products = [p.strip() for p in products_input.split(",") if p.strip()]
    
    st.write("Insira as palavras relacionadas:")
    words_input = st.text_area("Palavras relacionadas (separadas por vírgula)")
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    
    if st.button("Gerar Sugestões de Campanhas"):
        if not products or not words:
            st.warning("Por favor, insira pelo menos um termo relacionado ao produto e uma palavra.")
        else:
            campaign_df = generate_campaigns(products, words)
            st.write("Sugestões de Campanhas:")
            st.write(campaign_df)

if __name__ == "__main__":
    main()
