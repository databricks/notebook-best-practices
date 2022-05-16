import wget
import pandas as pd
import pyspark.pandas as ps
import sys

# Get the latest data.
def get_data(url, path):
  sys.stdout.fileno = lambda: False
  wget.download(url, path)

# Filter by country code.
def filter_country(pdf, country='USA'):
  pdf = pdf[pdf.iso_code == country]
  return pdf

# Pivot by indicator, and fill missing values.
def pivot_and_clean(pdf, fillna):
  pdf['value'] = pd.to_numeric(pdf['value'])
  pdf = pdf.fillna(fillna).pivot_table(values='value', columns='indicator', index='date')
  return pdf

# Create column names that are compatible with Delta tables.
def clean_spark_cols(pdf):
  clean_cols = pdf.columns.str.replace(' ', '_')
  pdf.columns = clean_cols
  psdf = ps.from_pandas(pdf)
  return psdf

# Convert index to column (works with pandas API on Spark, too).
def index_to_col(df, colname):
  df[colname] = df.index
  return df