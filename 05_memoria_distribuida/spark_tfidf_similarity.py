# Copyright (c) 2026 Alberto Fernández Isabel
# SPDX-License-Identifier: MIT

from pyspark.ml.feature import HashingTF, IDF, Normalizer, Tokenizer
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix
import pandas as pd
from scipy import sparse

def get_similar_indexes(sim_matrix, number_of_similar_items, item_index):
    sim_matrix_pd = pd.DataFrame(sim_matrix)
    similar_items = sim_matrix_pd.nlargest(number_of_similar_items, item_index)
    indexes = list(similar_items.index.values)
    values = list(similar_items[item_index].values)

    similar_indexes = []

    for i in range(0, len(values)):
        if values[i] > 0 and indexes[i] != item_index:
            similar_indexes.append(indexes[i])

    return similar_indexes

sc = SparkContext(appName="CosineSimilarity")
spark = SparkSession(sc)
sentenceData = spark.createDataFrame([
    (1, "Delhi Mumbai Gandhinagar"),
    (2, "Delhi Mandi"),
    (3, "Hyderbad Jaipur")], ["id", "sentences"])

tokenizer = Tokenizer(inputCol="sentences", outputCol="words")
wordsData = tokenizer.transform(sentenceData)
print(wordsData.collect())

hashingTF = HashingTF(inputCol="words", outputCol="tf")
tf = hashingTF.transform(wordsData)

idf = IDF(inputCol="tf", outputCol="feature").fit(tf)
tfidf = idf.transform(tf)

normalizer = Normalizer(inputCol="feature", outputCol="norm")
data = normalizer.transform(tfidf)

mat = IndexedRowMatrix(
    data.select("id", "norm").rdd.map(lambda row: IndexedRow(row.id, row.norm.toArray()))).toBlockMatrix()
dot = mat.multiply(mat.transpose())
sim_matrix = dot.toLocalMatrix().toArray()
sparse_matrix = sparse.csr_matrix(sim_matrix)
print(sparse_matrix)
#similar_indexes = get_similar_indexes(sparse_matrix,1,1)
#print(similar_indexes)
