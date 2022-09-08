# %% [markdown]
# # Cuusoo Technical Assessment - Mantel Group Future Associates Program

# %% [markdown]
# 

# %%
# pwd

# %%
# Import library
import os

# %% [markdown]
# ## Read Files

# %%
path = os.getcwd()
        
file_path = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".json")]

# %%
file_path

# %%
import json

# %%
raw_data = []

for f in file_path:
    
    with open(f, 'r') as myfile:
        data = myfile.read()

    # parse file
    raw_data += json.loads(data)
    

# %%
len(raw_data)

# %%
# !pip install pandas
import pandas as pd

# %%
# pd.__version__

# %%
df = pd.DataFrame(raw_data)

# %%
df.head(5)

# %%
df.info()

# %%
df.describe(include = "all")

# %%
df["Temperature"][0]

# %%
df2 = pd.json_normalize(df["Temperature"])

# %%
df2.head()

# %%
# axis 0 for row and 1 for column
df_full = pd.concat([df, df2], axis = 1)

# %%
df_full

# %%
# Remove columns that are no use for this exercise. 
df_full = df_full.drop("Temperature", axis = 1)

# %%
df_full

# %%
df_full = df_full.drop_duplicates()

# %%
df_full

# %%
df = df_full

# %%
df.dtypes

# %%
df[["WeatherText", "WeatherIcon"]].drop_duplicates().sort_values(by=["WeatherIcon"]).reset_index()

# %%


# %%


# %%


# %%
df["Metric.Unit"].value_counts()

# %%
df["Imperial.Unit"].value_counts()

# %%
text_cols = ["WeatherText", "PrecipitationType", "city"]

for c in text_cols:
    df[c] = df[c].str.title()

# %%
df

# %%
df["city"].value_counts()

# %%
temp_c = df.groupby(["city"])["Metric.Value"].mean()
temp_c

# %%
temp_f = df.groupby(["city"])["Imperial.Value"].mean()
temp_f

# %%
# axis 0 for row and 1 for column
temp = pd.concat([temp_c, temp_f], axis = 1)

# %%
temp

# %%
# temp["check"] = (temp["Metric.Value"] * 9/5) + 32 

# %%
temp

# %%
temp = temp.reset_index()
temp

# %%
temp = temp.rename(columns={"city": "City", "Metric.Value" : "TemperatureC", "Imperial.Value" : "TemperatureF"})

# %%
temp

# %%
weather = df.groupby("city")["WeatherText"].value_counts(sort=True).reset_index(name="Count")
weather

# %%
weather = weather.rename({"city": "City"}, axis = 1)

# %%
weather_output = weather.groupby(["City"]).head(3).sort_values(by=['City', 'Count'], ascending=[True, False])
weather_output

# %%
temp.to_csv("Average_Temperature.csv", index=False)

# %%
weather_output.to_csv("Weather_text.csv", index=False)

# %%


# %%


# %%


# %%
# !pip list


