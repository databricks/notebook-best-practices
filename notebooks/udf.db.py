# Databricks notebook source
# MAGIC %md
# MAGIC # UDF Example

# COMMAND ----------

# MAGIC %md
# MAGIC ## Using inline code
# MAGIC 
# MAGIC Inline UDFs work fine both in Databricks and from VSCode.

# COMMAND ----------

from pyspark.sql.types import LongType

def squared_typed(s):
  return s * s

print(squared_typed(12))
spark.udf.register("squaredWithPython", squared_typed, LongType())

spark.range(1, 20).createOrReplaceTempView("test")
display(spark.sql("select id, squaredWithPython(id) as id_squared from test"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Using a library function
# MAGIC 
# MAGIC This code works in the web UI but not from VSCode.
# MAGIC 
# MAGIC It appears that the Python path for resolving the UDF is not set correctly when using the run command API.

# COMMAND ----------

from pyspark.sql.types import LongType
from covid_analysis.udf import *

print(squared_typed_lib(12))
spark.udf.register("squaredWithPython", squared_typed_lib, LongType())

spark.range(1, 20).createOrReplaceTempView("test")
display(spark.sql("select id, squaredWithPython(id) as id_squared from test"))