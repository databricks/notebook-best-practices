'''
Python Spark job that imports the latest COVID-19 hospitalization data
'''
import sys
import urllib.request
import pandas as pd
from pyspark.sql import SparkSession

from covid_analysis.transforms import *

# tell Python the type of the spark global so code completion works
spark: SparkSession = spark

# check if job is running in production mode
is_prod = len(sys.argv) >= 2 and sys.argv[1] == "--prod"

urllib.request.urlretrieve("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/hospitalizations/covid-hospitalizations.csv", "/tmp/covid-hospitalizations.csv")
 
# read from /tmp, subset for USA, pivot and fill missing values
df = pd.read_csv("/tmp/covid-hospitalizations.csv")
df = filter_country(df, country='DZA')
df = pivot_and_clean(df, fillna=0)  
df = clean_spark_cols(df)
df = index_to_col(df, colname='date')

# Convert from Pandas to a pyspark sql DataFrame.
df = spark.createDataFrame(df)

print("Covid data successfully imported.")

# only write table in production mode
if is_prod:
    # Write to Delta Lake
    df.write.mode('overwrite').saveAsTable('covid_stats')

    # display sample data
    spark.sql('select * from covid_stats').show(10)



