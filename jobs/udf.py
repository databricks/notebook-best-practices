from pyspark.sql import SparkSession
from pyspark.sql.types import LongType

from covid_analysis.udf import *

# tell Python the type of the spark global so code completion works
spark: SparkSession = spark

print(squared_typed_lib(12))
spark.udf.register("squaredWithPython", squared_typed_lib, LongType())

spark.range(1, 20).createOrReplaceTempView("test")
spark.sql("select id, squaredWithPython(id) as id_squared from test").show()
