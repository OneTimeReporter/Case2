import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
os.environ['KAGGLE_CONFIG_DIR'] = '.kaggle/kaggle.json'
import kaggle.api

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
print(missing_data)

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

# Drop the specified columns
columns_to_drop = ['value', 'year']
df.drop(columns=columns_to_drop, inplace=True)

# # Stel dat je DataFrame df heet en een rij 'Afghanistan' bevat met gegevens over de tijd.
# # Laten we aannemen dat de kolommen de jaren voorstellen (bijvoorbeeld '1991', '1992', '1993', enz.).
# # We zullen alleen kolommen 7 t/m 37 selecteren uit de eerste rij (Afghanistan) om te plotten.

# # Selecteer de eerste rij voor Afghanistan
# afghanistan_data = df.iloc[0]

# # Selecteer alleen kolommen 7 t/m 37 (gebaseerd op nul-indexing)
# afghanistan_data = afghanistan_data.iloc[6:37]

# # Maak een lijst van de jaren (kolomnamen)
# jaren = [str(1991 + i) for i in range(31)]  # Maak een lijst van 1991 tot en met 2021

# # Maak een lijst van de datapunten voor elk jaar
# datapunten = afghanistan_data.tolist()

# # Plot de gegevens over de tijd (jaar)
# plt.figure(figsize=(10, 6))
# plt.plot(jaren, datapunten, marker='o', linestyle='-')
# plt.title('Gegevens over de tijd voor Afghanistan (kolommen 7 t/m 37)')
# plt.xlabel('Jaar')
# plt.ylabel('Waarde')
# plt.grid(True)
# plt.xticks(rotation=45)  # Roteren van x-as labels voor leesbaarheid
# plt.tight_layout()
# plt.show()

df = df.drop_duplicates(subset='Country')
df = df.reset_index(drop=True)
# df
st.header("Lineplot vergelijking van GII tussen twee landen")
unique_countries = df['Country'].unique()

land1 = st.selectbox('Select the first Country for comparison', unique_countries,index = 7)
land2 = st.selectbox('Select the second Country for comparison', unique_countries,index= 69)

land1_index = unique_countries.tolist().index(land1)
land2_index = unique_countries.tolist().index(land2)

land1_data = df[df['Country'] == f'{land1}']
land2_data = df[df['Country'] == f'{land2}']

land1_data = df.loc[land1_index, 'Gender Inequality Index (1990)':'Gender Inequality Index (2021)']
land2_data = df.loc[land2_index, 'Gender Inequality Index (1990)':'Gender Inequality Index (2021)']


# Maak een lijst van de jaren (kolomnamen)
years = [str(year) for year in range(1990, 2022)]

# Converteer de gegevens naar lijsten
land2_values = land2_data.values
land1_values = land1_data.values

# Maak de lineplot met Matplotlib voor België en Nederland
plt.figure(figsize=(10, 6))
plt.plot(years, land1_values, marker='o', linestyle='-', label=f'{land1}')
plt.plot(years, land2_values, marker='o', linestyle='-', label=f'{land2}')
plt.title(f'Gender Inequality Index {land1} en {land2} van 1990 tot en met 2021')
plt.xlabel('Jaar')
plt.ylabel('Gender Inequality Index')
plt.grid(True)
plt.xticks(rotation=45)  # Roteren van x-as labels voor leesbaarheid
plt.legend()  # Voeg een legende toe om de landen te onderscheiden
plt.tight_layout()
st.pyplot(plt)

st.write("Twee landen direct met elkaar vergelijken kan enorm veel inzicht aanbieden. Een lagere GII waarde betekent dat discriminatie op basis van geslacht relatief minder voorkomt.")
