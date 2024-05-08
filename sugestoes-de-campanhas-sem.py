import streamlit as st
import pandas as pd
import advertools as adv

def generate_campaigns(products, words):
    kw_df = adv.kw_generate(products, words)
    return kw_df

def main():
    st.title("Gerador de Sugestões de Campanhas SEM - Mídia Paga")
    
    st.write("Insira os termos relacionados ao produto foco da campanha:")
    products_input = st.text_area("Termos relacionados ao produto (separados por vírgula)")
    products = [p.strip() for p in products_input.split(",") if p.strip()]
    
    st.write("Insira as palavras semanticamente relacionadas:")
    words_input = st.text_area("Palavras relacionadas (separadas por vírgula)")
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    
  if st.button("Gerar Sugestões de Campanhas"):
        if not products or not words:
            st.warning("Por favor, insira pelo menos um termo relacionado ao produto e uma palavra.")
        else:
            campaign_df = generate_campaigns(products, words)
            
            # Definindo um mapeamento de cores para cada grupo de anúncios único
            ad_group_colors = {}
            unique_ad_groups = campaign_df['Ad Group'].unique()
            for i, ad_group in enumerate(unique_ad_groups):
                ad_group_colors[ad_group] = f"#{i%256:02x}{(i*7)%256:02x}{(i*13)%256:02x}"
            
            # Função para aplicar cores diferentes para cada linha com base no grupo de anúncios
            def apply_row_colors(row):
                ad_group = row['Ad Group']
                color = ad_group_colors.get(ad_group, "#ffffff")  # Use branco se o grupo de anúncios não estiver mapeado
                return [f"background-color: {color}"] * len(row)
            
            # Aplicando cores diferentes para cada linha
            styled_campaign_df = campaign_df.style.apply(apply_row_colors, axis=1)
            
            st.write("Sugestões de Campanhas:")
            st.dataframe(styled_campaign_df, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
