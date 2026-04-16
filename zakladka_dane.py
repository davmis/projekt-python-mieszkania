import streamlit as st
import pandas as pd
class Dane:
    def wyswietl_zakladke_dane(self):
        st.header("Dane źródłowe")
        st.write("Tutaj moesz przejeć dane, które zostały wykorzystane w tym projekcie: ")
        pliki = {
            "Wskazniki cen mieszkań (GUS)": "wskazniki_czyste.csv",
            "średnie zarobki (GUS)": "zarobki_czyste.csv",
            "Pełne dane GUS (surowe)": "dane_gus.csv"
        }
        for nazwa, sciezka in pliki.items():
            with st.expander(f"Tabela: {nazwa}"):
                try:
                    df = pd.read_csv(sciezka)
                    st.dataframe(df, use_container_width=True)
                    #przycisk pobierania:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"Pobierz {nazwa} jako CSV",
                        data=csv,
                        file_name=sciezka,
                        mime='text/csv',
                        key=sciezka #klucz do streamlit
                    )
                except FileNotFoundError:
                    st.error(f"Nie znaleziono pliku: {sciezka}")