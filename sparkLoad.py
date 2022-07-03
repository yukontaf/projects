#%%
import findspark as initiate_pyspark
initiate_pyspark.init('/usr/local/spark')
from pyspark.context import SparkContext
pyspark_context = SparkContext('local', 'sparkL')

#%%
from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("sparkLoad") \
    .getOrCreate()


#%%
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/yukontaf") \
    .option("dbtable", "dinosaurs") \
    .option("user", "glebsokolov") \
    .option("password", "") \
    .option("driver", "org.postgresql.Driver") \
    .load()

#%%
df.show()

#%%
df.write.csv('dinosaurs.csv')
#%%
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/yukontaf") \
    .option("dbtable", "dinosaurs2") \
    .option("user", "glebsokolov") \
    .option("password", "") \
    .save()

#%%
from pyspark import SparkConf
pyspark_configuration = SparkConf().setAppName("gradient_boosting_method").setMaster("local")
from pyspark.sql import SparkSession 
pyspark_session = SparkSession(pyspark_context)
# pyspark_df = pyspark_session.createDataFrame(df)





