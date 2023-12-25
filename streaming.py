from pymongo import MongoClient
from pyspark.sql import SparkSession
import os
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import input_file_name
from pyspark.sql.functions import monotonically_increasing_id, col,regexp_extract
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 pyspark-shell'
spark = SparkSession.builder.appName("KafkaSparkStreaming").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "streaming") \
    .load()
df_stream = df_stream.selectExpr("CAST(value AS STRING)")
uri = "mongodb+srv://ducva:1MpD1kPwNnl6TMpS@climatebd.5yhppdx.mongodb.net/"
client = MongoClient(uri)

# Chọn hoặc tạo một database và collection
db = client["example2"]
collection = db["example_collection2"]
# Giả sử df là DataFrame của bạn

query = df_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch_id: df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("uri", uri).option("database", "example2").option("collection", "streaming_data").save()) \
    .start()

# Đóng kết nối
client.close()
