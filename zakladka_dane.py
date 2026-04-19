import streamlit as st
import pandas as pd
class Dane:
    def wyswietl_zakladke_dane(self):
        st.header("Dane źródłowe")
        st.write("Tutaj moesz przejeć dane, które zostały wykorzystane w tym projekcie: ")
        st.markdown("Wszystkie dane wykorzystane w tym projekcie pochodzą z zasobów **Głównego Urzędu Statystycznego**.")
        st.info("**Oficjalne źródło:** [Bank Danych Lokalnych (BDL)](https://bdl.stat.gov.pl/bdl/dane/podgrup/temat)")
        pliki = {
            "Wskazniki inflacji": "wskazniki_czyste.csv",
            "średnie zarobki": "zarobki_czyste.csv",
            "Ceny za m2": "dane_gus.csv"
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