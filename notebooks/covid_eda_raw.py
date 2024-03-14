# Databricks notebook source
# MAGIC %md
# MAGIC #### Get latest COVID-19 hospitalization data

# COMMAND ----------

# MAGIC %md #### Transform

# COMMAND ----------

df = spark.sql("select * from aml_development.sample.covid_hospitalizations").toPandas()
print(df.head())

# COMMAND ----------

# read from /tmp, subset for USA, pivot and fill missing values
df = df[df.iso_code == 'USA']\
     .pivot_table(values='value', columns='indicator', index='date')\
     .fillna(0)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Visualize 

# COMMAND ----------

df.plot(figsize=(13,6), grid=True).legend(loc='upper left')

# COMMAND ----------

# MAGIC  %md
# MAGIC #### Save to Delta Lake
# MAGIC The current schema has spaces in the column names, which are incompatible with Delta Lake.  To save our data as a table, we'll replace the spaces with underscores.  We also need to add the date index as its own column or it won't be available to others who might query this table.

# COMMAND ----------

import pyspark.pandas as ps

clean_cols = df.columns.str.replace(' ', '_')

# Create pandas on Spark dataframe
psdf = ps.from_pandas(df)

psdf.columns = clean_cols
psdf['date'] = psdf.index

# Write to Delta table, overwrite with latest data each time
psdf.to_table(name='dev_covid_analysis', mode='overwrite')

# COMMAND ----------

# MAGIC %md
# MAGIC #### View table

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dev_covid_analysis
