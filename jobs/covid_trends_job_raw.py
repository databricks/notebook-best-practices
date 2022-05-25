import urllib.request
import pyspark.pandas as ps
import pandas as pd

urllib.request.urlretrieve("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/hospitalizations/covid-hospitalizations.csv", "/tmp/covid-hospitalizations.csv")

# read from /tmp, subset for USA, pivot and fill missing values
df = pd.read_csv("/tmp/covid-hospitalizations.csv")
df = df[df.iso_code == 'USA']\
     .pivot_table(values='value', columns='indicator', index='date')\
     .fillna(0)

clean_cols = df.columns.str.replace(' ', '_')

# Create pandas on Spark dataframe
psdf = ps.from_pandas(df)

psdf.columns = clean_cols
psdf['date'] = psdf.index

# Write to Delta table, overwrite with latest data each time
psdf.to_table(name='dev_covid_analysis', mode='overwrite')