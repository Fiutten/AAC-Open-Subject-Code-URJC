# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

from pyspark import SparkContext
import itertools

sc = SparkContext.getOrCreate()
rdd1 = sc.parallelize([1, 2, 3, 4])
rdd2 = sc.parallelize([1, 2, 3, 4])

# Suma no paralela.
lista = []
for i in range(0, len(rdd1.collect())):
   lista.append(rdd1.collect()[i] + rdd2.collect()[i])
rdd3 = sc.parallelize(lista)
print(rdd3.collect())

# Suma paralela
rdd4 = rdd1.zip(rdd2).map(lambda x: x[0] + x[1])
print(rdd4.collect())

# Suma paralela con rdd de distinto tamaño
rdd5 = sc.parallelize([1, 2, 3])
rdd6 = sc.parallelize([1, 2, 3, 6, 7, 9, 10, 10, 22, 34, 45])
rdd7 = sc.parallelize(list(itertools.zip_longest(rdd5.collect(), rdd6.collect(), fillvalue=0))).map(lambda x: x[0] + x[1])
print(rdd6.collect())
