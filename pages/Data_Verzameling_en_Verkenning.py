#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import kaggle
import os
import streamlit as st
import plotly.express as px

api = kaggle.api
api.get_config_value("username")

st.title("Het verzamelen en verkennen van data.")

kaggle.api.dataset_download_file("iamsouravbanerjee/gender-inequality-index-dataset", "gender inequality index.csv")
kaggle.api.dataset_download_file("meeratif/a-worldwide-ranking-of-corruption", "corruption.csv")
kaggle.api.dataset_download_file("sazidthe1/world-gdp-data", "gdp_data.csv")

if os.path.isfile("Gender_Inequality_Index.csv") == False:
    os.rename("Gender%20Inequality%20Index.csv", "Gender_Inequality_Index.csv")


# Importing of the dataset
df = pd.read_csv('Gender_Inequality_Index.csv')
corruption_df = pd.read_csv('corruption.csv')
gdp_df = pd.read_csv('gdp_data.csv')

missing_data = df.isna().sum()

st.write('''
        Data verzameling en verkenning zijn fundamenteel voor het analyseren van data. Zonder deze stappen te nemen is het niet mogelijk om daadwerkelijke inzichten op te doen. 
        De data is aangeroepen door middel van de Kaggle API. Er wordt gebruik gemaakt van drie verschillende datasets:
''')
st.markdown('''
- De Gender Inequality Index Dataset
- De Corruptie Dataset
- De Gross Domestic Product Dataset
            
Aan de hand van de Gender Inequality Index dataset in combinatie met de andere vermelde willen wij onderzoeken welke factoren het meeste invloed heeft.
''')
st.write("Zoals eerder vermeld, deze datasets zijn verkregen van Kaggle, aangeroepen met behulp van de API. De volgende stukken code zijn gebruikt:")
st.code('''
        api = kaggle.api
        api.get_config_value("username")
        kaggle.api.dataset_download_file(dataset,path)
''',language="Python")
st.header("Missing Values")
st.write("We kijken eerst naar onze variabelen, en de hoeveelheid missende waardes van deze variabelen. Dit doen we door")
st.code('''
        missing_data = df.isna().sum()
        st.table(missing_data)''', 
        language="Python")
missingdatatoggle = st.toggle("Show Missing Data Table")

if missingdatatoggle:
     st.table(missing_data)

st.divider()

import matplotlib.pyplot as plt
import seaborn as sns

heatmaptoggle = st.toggle("Show Missing Data as a Heatmap")


# Creates a heatmap of missing data
if heatmaptoggle:
    fig, ax= plt.subplots()
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', ax=ax)
    st.pyplot(fig)

st.divider()

st.header("Cleaning the data")

st.write('''
         Nu we onze data hebben ontvangen en gecheckt hebben op missende waardes, is het tijd om de data op te schonen voor gebruik in onze analyses.
         Ten eerste verwijderen wij de kolommen UNDP Developing Regions en Hemisphere. Onze reden voor onze keuze is [Vul hier de reden in].
         Daarna vullen wij de missende waardes in de Gender Inequality Index met de mean waarde dat correspondeerd met de mean waarde van het continent waar het land zich bevind.
         De volgende aanwijzigingen worden uitgevoerd:
         ''')
st.markdown('''
            - Een inner join van de "ISO3" kolom met de "Country Code" kolom van de GDP dataframe.
            - Een inner join van de Corruption dataframe met de "Country" kolom.
            - Samenvoegen van kolommen "country_name" en "country" op de kolom "country".
            - Redunde kolommen die overblijven na het samenvoegen van kolommen worden gedropt.''')

cleaningtoggle = st.toggle("Show Code used for cleaning")
if cleaningtoggle:
    st.code(''' 
            # Drop the specified columns
            df = df.drop(['UNDP Developing Regions', 'Hemisphere'], axis=1)

            # Verify that the columns have been dropped
            print(df.columns)

            # Columns with missing GII values
            columns_to_impute = df.columns[df.columns.str.contains('Gender Inequality Index')]

            # Corresponding continent column
            continent_column = 'Continent'

            # Calculate the mean GII value for each continent
            continent_mean_GII = df.groupby(continent_column)[columns_to_impute].mean()

            # Fill missing GII values with the mean GII value of their respective continent
            df[columns_to_impute] = df.groupby(continent_column)[columns_to_impute].transform(lambda x: x.fillna(x.mean()))

            # Merge df with gdp_df on 'ISO3' column from df and 'Country Code' column from gdp_df
            df = df.merge(gdp_df, left_on='ISO3', right_on='country_code', how='inner')

            # Merge the result with corruption_df on 'Country' column
            df = df.merge(corruption_df, on='Country', how='inner')

            # Optionally, you can drop the 'Country Code' and 'ISO3' columns as they are no longer needed
            df.drop(['country_code', 'ISO3'], axis=1, inplace=True)

            # Check for missing data in the merged DataFrame 'df'
            missing_data = df.isna().sum()

            # Print the count of missing values for each column
            print(missing_data)

            # Merge 'country_name' with 'Country' column and keep the result in 'Country'
            df['Country'] = df['Country'].combine_first(df['country_name'])

            # Now, you can drop the 'country_name' column if it's no longer needed
            df.drop(['country_name'], axis=1, inplace=True)

            print(missing_data)

            # Drop the specified columns
            columns_to_drop = ['value', 'year']
            df.drop(columns=columns_to_drop, inplace=True)

            # Print the existing column names in the DataFrame
            print(df.columns)

            # Check for missing data in the merged DataFrame 'df'
            missing_data = df.isna().sum()

            # Print the count of missing values for each column
            print(missing_data)
''', language="Python")
    
# Drop the specified columns
df = df.drop(['UNDP Developing Regions', 'Hemisphere'], axis=1)

# Verify that the columns have been dropped
print(df.columns)

# Columns with missing GII values
columns_to_impute = df.columns[df.columns.str.contains('Gender Inequality Index')]

# Corresponding continent column
continent_column = 'Continent'

# Calculate the mean GII value for each continent
continent_mean_GII = df.groupby(continent_column)[columns_to_impute].mean()

# Fill missing GII values with the mean GII value of their respective continent
df[columns_to_impute] = df.groupby(continent_column)[columns_to_impute].transform(lambda x: x.fillna(x.mean()))

# Merge df with gdp_df on 'ISO3' column from df and 'Country Code' column from gdp_df
df = df.merge(gdp_df, left_on='ISO3', right_on='country_code', how='inner')

# Merge the result with corruption_df on 'Country' column
df = df.merge(corruption_df, on='Country', how='inner')

# Optionally, you can drop the 'Country Code' and 'ISO3' columns as they are no longer needed
df.drop(['country_code', 'ISO3'], axis=1, inplace=True)

# Check for missing data in the merged DataFrame 'df'
missing_data = df.isna().sum()

# Print the count of missing values for each column
print(missing_data)

# Merge 'country_name' with 'Country' column and keep the result in 'Country'
df['Country'] = df['Country'].combine_first(df['country_name'])

# Now, you can drop the 'country_name' column if it's no longer needed
df.drop(['country_name'], axis=1, inplace=True)

print(missing_data)

# Drop the specified columns
columns_to_drop = ['value', 'year']
df.drop(columns=columns_to_drop, inplace=True)


# Print the existing column names in the DataFrame
print(df.columns)

# Check for missing data in the merged DataFrame 'df'
missing_data_2 = df.isna().sum()

# Print the count of missing values for each column
print(missing_data_2)

missingdatatoggle_2= st.toggle("Show Missing Data Table after cleaning")

if missingdatatoggle_2:
     st.table(missing_data_2)

st.divider()
st.header("Visualising the data")

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter(df['Corruption index'], df['Gender Inequality Index (2021)'], c=df['Gender Inequality Index (2021)'], cmap='viridis', alpha=0.5)
ax.set_title('Scatter Plot: Corruption Index vs Gender Inequality Index (2021)')
ax.set_xlabel('Corruption index')
ax.set_ylabel('Gender Inequality Index (2021)')
ax.grid(True)

# Add a colorbar
cbar = plt.colorbar(sc)
cbar.set_label('Gender Inequality Index (2021)')

# Show the plot using Streamlit
st.pyplot(fig)

st.divider()
jaarselectie = st.slider("Kies Jaar", 1990, 2021, 2021)
fig = px.histogram(df, facet_col='Continent', y=f"Gender Inequality Index ({jaarselectie})", color="Continent")
st.plotly_chart(fig, use_contrainer_width=True)
