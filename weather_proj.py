# %% [markdown]
# # Weather in Austrlia

# %% [markdown]
# 

# %%
# pwd

# %% [markdown]
# # Import Library
# 

# %%
import os
import json
# !pip install pandas
import pandas as pd


# %% [markdown]
# ## Read Files

# %%
# Read dataset files
path = os.path.join(os.getcwd(),"dataset")
file_path = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".json")]

print(file_path)

# %%
# Read dataset as a list of dictionaries 
raw_data = []

for f in file_path:
    
    with open(f, 'r') as myfile:
        data = myfile.read()

    # parse file
    raw_data += json.loads(data)
    

# %%
len(raw_data)

# %%
df = pd.DataFrame(raw_data)
df.head(5)

# %% [markdown]
# # Exploratory data analysis (EDA)

# %%
df.info()

# %%
df.describe(include = "all")

# %%
df["Temperature"][0]

# %%
# Expand the Temperature column as a new data frame
df2 = pd.json_normalize(df["Temperature"])

# %%
df2.head()

# %%
# Combine two dataframes into one

# axis 0 for row and 1 for column
df_full = pd.concat([df, df2], axis = 1)

# %%
df_full.head()

# %%
# Remove columns that are no use for this exercise. 
df_full = df_full.drop("Temperature", axis = 1)

# %%
df_full = df_full.drop_duplicates()

# %%
df_full

# %%
df = df_full

# %%
df.dtypes

# %%
# df[["WeatherText", "WeatherIcon"]].drop_duplicates().sort_values(by=["WeatherIcon"]).reset_index()

# %%


# %% [markdown]
# # The average temperature for each city

# %%
# Turn the first letter of the column value into capital, and the rest is lower case. 
text_cols = ["WeatherText", "PrecipitationType", "city"]

for c in text_cols:
    df[c] = df[c].str.title()

# %%
df.head()

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
temp = pd.concat([temp_c, temp_f], axis = 1).round(2)

# %%
# temp["check"] = (temp["Metric.Value"] * 9/5) + 32 

# %%
# Rename column names
temp = temp.reset_index()
temp = temp.rename(columns={"city": "City", "Metric.Value" : "TemperatureC", "Imperial.Value" : "TemperatureF"})
temp

# %%


# %% [markdown]
# # The top three most common “weather text” for each city

# %%
weather = df.groupby("city")["WeatherText"].value_counts(sort=True).reset_index(name="Count")
weather

# %%
weather = weather.rename({"city": "City"}, axis = 1)

# %%
weather_output = weather.groupby(["City"]).head(3).sort_values(by=['City', 'Count'], ascending=[True, False])
weather_output

# %%


# %% [markdown]
# # Save results as CSV

# %%
temp.to_csv("Average_Temperature.csv", index=False)

# %%
weather_output.to_csv("Weather_Text.csv", index=False)

# %%



