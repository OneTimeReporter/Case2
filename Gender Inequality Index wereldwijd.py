
import pandas as pd
import kaggle
import os
import streamlit as st
import matplotlib.pyplot as plt

api = kaggle.api
api.get_config_value("username")

kaggle.api.dataset_download_file("iamsouravbanerjee/gender-inequality-index-dataset", "gender inequality index.csv")
kaggle.api.dataset_download_file("meeratif/a-worldwide-ranking-of-corruption", "corruption.csv")
kaggle.api.dataset_download_file("sazidthe1/world-gdp-data", "gdp_data.csv")

if os.path.isfile("Gender_Inequality_Index.csv") == False:
    os.rename("Gender%20Inequality%20Index.csv", "Gender_Inequality_Index.csv")

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

import plotly.express as px
st.header("Scatterplot Human Development Index tegen Gender Inequality Index")

scatterfig = px.scatter(df, x="HDI Rank (2021)", y="Gender Inequality Index (2021)", color="Continent")
st.plotly_chart(scatterfig)
st.write("Een simpele scatterplot tussen de Human Development Index en Gender Inequality Index van het jaar 2021. Er is een vrij duidelijke correlatie tussen een land's HDI rank en GII score.")
st.divider()
continent_avg_gii = df.groupby('Continent')['Gender Inequality Index (2021)'].mean().reset_index()
print(continent_avg_gii)

st.header("Histogram Gender Inequality Index per Continent")
unique_continents = df['Continent'].unique()
selected_continents = st.multiselect("Select Continents", unique_continents, default=unique_continents)
filtered_df = df[df['Continent'].isin(selected_continents)]
if len(selected_continents) > 0:
    # Create the histogram plot using filtered data
    histofig = px.histogram(filtered_df, facet_col='Continent', y="Gender Inequality Index (2021)", color="Continent")

    # Display the histogram plot using Streamlit
    st.plotly_chart(histofig)
    st.write("Een histogram om de verdeling van GII scores te bekijken per continent. In Europa zijn de waardes laag en geclusterd, wat aangeeft dat in Europa discriminatie tegen geslacht relatief laag is")
    st.write("In Azie zijn de waardes veel meer verspreid.")

st.divider()

import geopandas as gpd

countries = gpd.read_file(
               gpd.datasets.get_path("naturalearth_lowres"))
countries.head()
continentkeuze = st.selectbox("Kies het continent dat u wilt plotten",("Asia","Africa","North America","South America","Oceania","Europe", "World"))
if continentkeuze == "World":
    countries = countries.sort_values(by='name', ascending=True)
else:
    countries = countries.sort_values(by='name', ascending=True)[countries["continent"]== f"{continentkeuze}"]

df = countries.join(df.set_index('Country'), on='name')
print(df)

st.header("Gender Inequality Index gevisualiseerd op een wereldkaart.")
st.write("Een wereldkaart helpt met het visualiseren van de datapunten. U heeft de mogelijkheid om het jaar en continent te kiezen.")
mapfig, ax = plt.subplots(1,1,figsize=(16,5))
mapjaar = st.slider("Kies Jaar", 1990, 2021, 2021)
ax.set_axis_off()
ax.set_title("GII Indexes op de wereldkaart")
df.plot(cmap='OrRd', column=df[f'Gender Inequality Index ({mapjaar})'],ax=ax, missing_kwds={'color': 'lightgrey'}, legend=True)
st.pyplot(mapfig)

