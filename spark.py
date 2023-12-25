import pandas as pd
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import input_file_name
from pyspark.sql.functions import monotonically_increasing_id, col,regexp_extract,concat_ws,split
custom_schema = StructType([
    StructField("Day",IntegerType(), True),
    StructField("T",DoubleType(), True),
    StructField("TM2",DoubleType(), True),
    StructField("Tm3",DoubleType(), True),
    StructField("SLP",DoubleType(), True),
    StructField("H",  DoubleType(), True),
    StructField("PP",  DoubleType(), True),
    StructField("VV",  DoubleType(), True),
    StructField("V",  DoubleType(), True),
    StructField("VM",  DoubleType(), True),
    StructField("Country",StringType(),True),
    StructField("Month",StringType(),True),
    StructField("Year",IntegerType(),True)
])


# Tạo đối tượng SparkSession
spark = SparkSession.builder.appName("example").getOrCreate()

# Đường dẫn đến file CSV
input_path = "hdfs://localhost:9000/Users/vuanhduc/climate_data_expand/*.csv"
# Đọc dữ liệu từ file CSV vào DataFrame
df = spark.read.csv(input_path, header=False)
df_with_id = df.withColumn("row_id", monotonically_increasing_id())
df = df_with_id.filter(col("row_id") > 0).drop("row_id")
columns_to_keep = df.columns[:10] + df.columns[15:]
df = df.select(*columns_to_keep)
for column in columns_to_keep:
    if column != "_c15" and column != "_c16":
        df = df.withColumn(column,col(column).cast("double"))
df = df.withColumn(columns_to_keep[-1],col(columns_to_keep[-1]).cast("int"))
df = df.withColumn("_c0",col("_c0").cast("int"))
#print(input_file_name())


df = spark.createDataFrame(df.rdd, schema=custom_schema)
df=df.fillna({'country':'Unknown'})
df.show()
df.dropna()






# Thay đổi thông tin kết nối tại đây
uri = "mongodb+srv://ducva:1MpD1kPwNnl6TMpS@climatebd.5yhppdx.mongodb.net/"
client = MongoClient(uri)

# Chọn hoặc tạo một database và collection
db = client["example3"]
collection = db["final"]
# Giả sử df là DataFrame của bạn

# Chuyển DataFrame thành dạng dữ liệu hỗ trợ
data = [row.asDict() for row in df.collect()]
# Chèn dữ liệu vào collection
collection.insert_many(data)

# Đóng kết nối
client.close()
