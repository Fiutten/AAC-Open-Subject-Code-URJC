# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

from pyspark.sql import SparkSession


def main() -> None:
    spark = (SparkSession.builder
             .appName("RDDFilterExample")
             .getOrCreate())
    sc = spark.sparkContext

    # Ejemplo autocontenido: filtrado de un RDD creado en memoria.
    lines = sc.parallelize(["pandas", "I like pandas", "spark", "data engineering"])
    result = lines.filter(lambda line: "pandas" in line)
    print(result.collect())

    spark.stop()


if __name__ == "__main__":
    main()
