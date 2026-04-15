import streamlit as st
import pandas as pd
class Kalkulator:
    def __init__(self):
        self.df_ceny = pd.read_csv('dane_gus.csv')
        self.df_zarobki = pd.read_csv('zarobki_czyste.csv')
        self.rok = '2024' #bedziemy liczyc na najswiezszych danych

    def wyswietl_kalkulator(self):
        st.header("Kalkulator Dostępności mieszkań")
        st.write("Na co Cię stać.")
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
            lata=st.number_input("Przez ile lat chcesz oszczędzać?", min_value=1, max_value = 40, value=5)
            #tutaj juz wchodzi matematyka 
            #wyciagamy cene za m2 dla pojedynczych wojwodztw
            cena_m2 = self.df_ceny[self.df_ceny['Wojewodztwo']==wojewodztwo][self.rok].values[0]
            miesieczne_oszczednosci = pensja*(procent/100)
            calkowite_oszczednosci = miesieczne_oszczednosci*12*lata
            metraz = (calkowite_oszczednosci / cena_m2) if cena_m2 > 0 else 0

        with col2:
            st.subheader("Twoje wyniki: ")
            #jezeli ktos zarabia 0, lub odklada 0%
            if miesieczne_oszczednosci ==0:
                st.error("Z gówna bata nie ukręcisz, zarabiaj wiecej albo odkladaj wiecej")
            else:
                st.metric("Średnia cena m2 w tym regionie", f"{cena_m2:,.0f} PLN")
                st.metric(
                    f"Twój kapitał po {lata} latach",
                    f"{calkowite_oszczednosci:,.0f} PLN",
                    delta=f"Odkładasz {miesieczne_oszczednosci:,.0f} zł/msc"
                )
                st.markdown(f"### Za gotówkę kupisz: **{metraz:,.2f} m2**")

                if metraz<25:
                    st.error(f"Bądźmy szczerzy. {metraz:,.1f} m2 to patokawalerka")
                elif metraz<45:
                    st.warning(f"{metraz:,.1f} m2 to ciasna kawalerka!")
                else:
                    st.success(f"{metraz:,.1f} m2 to juz calkiem niezly rozmiar")