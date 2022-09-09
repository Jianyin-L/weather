# %% [markdown]
# # Weather in Austrlia

# %% [markdown]
# 

# %%
# pwd

# %% [markdown]
# ## Directory

# %%
# Specify the location
input_location = "dataset"    # Name of the folder of the dataset
output_location = "result"    # Name of the folder of the result

# %% [markdown]
# ## Import Library
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
path = os.path.join(os.getcwd(),input_location)
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
# Transform data as a dataframe
df = pd.DataFrame(raw_data)
df.head(5)

# %% [markdown]
# ## Exploratory data analysis (EDA)

# %%
df.head()

# %%
df["Temperature"][0]

# %%
# Expand the Temperature column as a new data frame
df2 = pd.json_normalize(df["Temperature"])
df2.head()

# %%
# Combine two dataframes into one

# axis 0 for row and 1 for column
df_full = pd.concat([df, df2], axis = 1)

# %%
# Remove columns that are no use for this exercise. 
df_full = df_full.drop("Temperature", axis = 1)

# %%
# Drop duplicates
df_full = df_full.drop_duplicates()

# %%
# Rename column name
df_full = df_full.rename({"city": "City"}, axis = 1)

# %%
text_cols = ["WeatherText", "PrecipitationType", "City"]

for c in text_cols:
    df_full[c] = df_full[c].str.title()    # Turn the first letter of the column value into capital, and the rest is lower case. 
    df_full[c] = df_full[c].str.strip()    # Remove space of the value in the text column 


# %%
df_full.head()

# %%
df_full.info()

# %%
df_full.describe(include = "all")

# %%
# df[["WeatherText", "WeatherIcon"]].drop_duplicates().sort_values(by=["WeatherIcon"]).reset_index()

# %% [markdown]
# ## The average temperature for each city

# %%
# Select relevant columns
df_temp = df_full[["City", "Metric.Value", "Imperial.Value"]]
df_temp.head()

# %%
temp_c = df_temp.groupby(["City"])["Metric.Value"].mean()
temp_c

# %%
temp_f = df_temp.groupby(["City"])["Imperial.Value"].mean()
temp_f

# %%
# axis 0 for row and 1 for column
temp = pd.concat([temp_c, temp_f], axis = 1).round(2)

# %%
# temp["check"] = (temp["Metric.Value"] * 9/5) + 32 

# %%
# Rename column names
temp = temp.reset_index()
temp = temp.rename(columns={"Metric.Value" : "TemperatureC", "Imperial.Value" : "TemperatureF"})
temp

# %%


# %% [markdown]
# ## The top three most common “weather text” for each city

# %%
weather_df = df_full[["City", "WeatherText"]]
weather_df.head()

# %%
# Group by City and Count the occurance in Weather Text
weather = weather_df.groupby("City")["WeatherText"].value_counts(sort=True).reset_index(name="Count")

# Find top 3 of the weather text in each group
weather = weather.groupby(["City"]).head(3).sort_values(by=['City', 'Count'], ascending=[True, False])

weather

# %% [markdown]
# ## Save results as CSV

# %%
if not os.path.exists(output_location):
    os.makedirs(output_location)

# %%
temp_location = output_location + "/Average_Temperature.csv"
temp.to_csv(temp_location, index=False)

# %%
weather_location = output_location + "/Weather_Text.csv"
weather.to_csv(weather_location, index=False)

# %%



