import streamlit as st
import pandas as pd
class Kalkulator:
    def __init__(self):
        self.df_ceny = pd.read_csv('dane_gus.csv')
        self.df_zarobki = pd.read_csv('zarobki_czyste.csv')
        self.rok = '2024' #bedziemy liczyc na najswiezszych danych

    def wyswietl_kalkulator(self):
        st.header("Kalkulator Dostępności mieszkań")
        st.write("Sprawdźmy, ile lat oszdzędzania Cię czeka.")
        #dzielimy ekran na dwie kolumny (lewa na wpisywanie rzeczy, a prawa na wyniki)
        col1, col2 = st.columns(2)
        with col1:
            #wybor wojewodztwa
            lista_wojewodztw = self.df_ceny['Wojewodztwo'].unique()
            wojewodztwo = st.selectbox("Wybierz województwo: ", lista_wojewodztw)
            #pobieramy srednie zarobki dla wojewodztwa
            sr_zarobki = self.df_zarobki[self.df_zarobki['Wojewodztwo'] == wojewodztwo][self.rok].values[0]
            #pola do wpisania danych przez uzytkownika
            pensja = st.number_input(
                f"Twoja miesięczna pensja netto (PLN): ",
                min_value=0,
                value=int(sr_zarobki), #domyslnie wpisujemy srednia dla regionu
                step = 500
            )
            st.caption(f"Średnia w tym regionie to ok. {sr_zarobki:,.0f} zł")
            procent = st.slider("Ile procent swojej pensji odkładasz co miesiąc?", 0,100,20)
            docelowy_metraz = st.number_input(
                "Ile metrów kwadratowych chcesz kupić?", 
                min_value=15, 
                max_value=300, 
                value=50, 
                step=5
            )
            #tutaj juz wchodzi matematyka 
            #wyciagamy cene za m2 dla pojedynczych wojwodztw
            cena_m2 = self.df_ceny[self.df_ceny['Wojewodztwo']==wojewodztwo][self.rok].values[0]
            koszt_calkowity = cena_m2 * docelowy_metraz
            miesieczne_oszczednosci = pensja * (procent / 100)

        with col2:
            st.subheader("Twoje wyniki: ")
            #jezeli ktos zarabia 0, lub odklada 0%
            if miesieczne_oszczednosci ==0:
                st.error("Z gówna bata nie ukręcisz, zarabiaj wiecej albo odkladaj wiecej")
            else:
                # Wyliczamy ile lat zajmie uzbieranie pełnej kwoty
                lata_oszczedzania = koszt_calkowity / (miesieczne_oszczednosci * 12)
                
                st.metric("Całkowity koszt mieszkania", f"{koszt_calkowity:,.0f} PLN", delta=f"Cena za m²: {cena_m2:,.0f} zł", delta_color="off")
                st.metric("Odkładasz miesięcznie", f"{miesieczne_oszczednosci:,.0f} PLN")
                
                
                st.markdown(f"### Czas zbierania: **{lata_oszczedzania:.1f} lat**")
                
                # diagnoza czasu oszczędzania
                if lata_oszczedzania > 35:
                    st.error(f"Bądźmy szczerzy. {lata_oszczedzania:.1f} lat oszczędzania to wyrok. Kupisz to mieszkanie na emeryturze albo wcale, a inflacja i tak Cię pożre. Zmień metraż, poszukaj lepszej pracy albo tańszego województwa.")
                elif lata_oszczedzania > 15:
                    st.warning(f"⚠️ {lata_oszczedzania:.1f} lat to kupa czasu i zamrożony kapitał. Zastanów się nad mniejszym metrażem na start, żeby szybciej być na swoim.")
                else:
                    st.success(f"{lata_oszczedzania:.1f} lat to całkiem realny horyzont! Trzymaj się planu, zaciskaj zęby, a wkrótce odbierzesz klucze bez kredytu na karku.")