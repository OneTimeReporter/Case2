#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import kaggle

#NS Logo aanroepen
response = requests.get("https://blog.vantagecircle.com/content/images/2021/12/gender-inequality-in-the-workplace.jpg")
nsheader = Image.open(BytesIO(response.content))

st.title("Case 2 - Gender Inequality Analyse")
st.subheader("Team 1: Ryan Achternaam, Luuk Koppen, Timo Jansen, Tarik Kiliç")
st.image(nsheader, caption="Gender Inequality is een probleem dat wereldwijd geobserveerd kan worden.")


st.write('''Discriminatie op basis van geslacht is een probleem dat wereldwijd geobserveerd word. In deze blog nemen wij een kijk naar verschillende datasets. Ons doel is om onze publiek
         een beter begrip te geven op deze complexe wereldwijde fenomeen. Met behulp van de Kaggle API voor het aanroepen van data, en onze vaardigheden in het maken van data analyzes 
         en visualisaties, hopen wij ons doel te bereiken. Deze blog is opgebouwd met behulp van de Streamlit applicatie.''')







