# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

from pyspark.sql import SparkSession


spark = (SparkSession.builder
         .appName("SQLDataFramesExample")
         .getOrCreate())
sc = spark.sparkContext

rdd = sc.parallelize([("Javier", 35), ("Susana", 19), ("Mateo", 25)])
personas = spark.createDataFrame(rdd, ["name", "age"])
print(personas.collect())
personas.show()

spark.stop()
