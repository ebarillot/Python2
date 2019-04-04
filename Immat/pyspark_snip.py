# coding=utf-8

from __future__ import print_function, unicode_literals

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

# Configuratins related to Cassandra connector & Cluster
import os

# os.environ[b'PYSPARK_SUBMIT_ARGS'] = b"--packages com.datastax.spark:spark-cassandra-connector_2.11:2.3.0 --conf spark.cassandra.connection.host=192.168.60.38 pyspark-shell"
# sc = SparkContext(b'local', b'test')

conf = SparkConf().setAppName(b"Stand Alone Python Script")
sc = SparkContext(conf=conf)

sqlContext = SQLContext(sc)

sqlContext.read.format(b"org.apache.spark.sql.cassandra").options(table=b"immat_by_num_plaque_json", keyspace=b"ks_lab1_datalake").load().show()

# df = sqlContext.read('com.databricks.spark.csv').options(header='true', inferschema='true').load('cars.csv')
# df.select('year', 'model').write.format('com.databricks.spark.csv').save('newcars.csv')
