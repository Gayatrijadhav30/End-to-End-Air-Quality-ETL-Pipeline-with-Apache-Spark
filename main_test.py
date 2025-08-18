from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when, avg
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# --- ENV SETUP ---
os.environ["AWS_ACCESS_KEY_ID"] = " " #Put your AWS S3 bucket key
os.environ["AWS_SECRET_ACCESS_KEY"] = " "
os.environ["JAVA_HOME"] = r"C:/Program Files/Eclipse Adoptium/jdk-11.0.27.6-hotspot"
os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ["PATH"]

# JDBC connection info
jdbc_url = "jdbc:postgresql://localhost:5432/epa_air_test"
jdbc_jar = r"C:/spark_jars/postgresql-42.6.2.jar"  # or latest version
db_properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

# --- STEP 1: CREATE DATABASE IF NEEDED ---
def create_postgres_database(db_name):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE {db_name}')
            print(f"📦 Created database: {db_name}")
        else:
            print(f"📦 Database {db_name} already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error checking/creating database:", e)

create_postgres_database("epa_air_test")


# --- STEP 2: SET ALL REQUIRED JARS (S3 + JDBC) ---
aws_jar = "C:/spark_jars/hadoop-aws-3.3.5.jar,C:/spark_jars/aws-java-sdk-bundle-1.11.1026.jar"
jdbc_jar = r"C:\spark_jars\postgresql-42.6.2.jar"

# --- STEP 3: CREATE SPARK SESSION ---
spark = SparkSession.builder \
    .appName("EPA Air Pipeline") \
    .config("spark.jars", jdbc_jar) \
    .config("spark.driver.extraClassPath", jdbc_jar) \
    .config("spark.executor.extraClassPath", jdbc_jar) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"]) \
    .config("spark.hadoop.fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"]) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.eu-north-1.amazonaws.com") \
    .getOrCreate()


# ------------------ STEP 4: PIPELINE FUNCTION ------------------ #
def process_gas(folder, table_name, fill_aqi=False):
    print(f"\n▶ Processing {table_name} data...")
    df = spark.read.csv(f"s3a://blobstorageair/{folder}/*.csv", header=True, inferSchema=True)
    df = df.drop("Event Type")
    
    df = df.select(
        to_date(col("Date Local"), "yyyy-MM-dd").alias("date"),
        col("State Name").cast("string").alias("state"),
        col("City Name").cast("string").alias("city"),
        col("Site Num").cast("int").alias("site_id"),
        col("Latitude").cast("double").alias("lat"),
        col("Longitude").cast("double").alias("lon"),
        col("Arithmetic Mean").cast("double").alias("mean_value"),
        col("1st Max Value").cast("double").alias("max_value"),
        col("AQI").cast("double").alias("aqi"),
        col("Parameter Name").cast("string").alias("pollutant"),
        col("Local Site Name").cast("string").alias("local_site"),
        col("CBSA Name").cast("string").alias("cbsa")
    )
    
    df = df.dropna(subset=["date", "state", "city", "site_id", "mean_value"])
    
    if fill_aqi:
        factor_df = df.filter((col("aqi").isNotNull()) & (col("mean_value").isNotNull())) \
                      .withColumn("ratio", col("aqi") / col("mean_value"))
        factor = factor_df.agg(avg("ratio")).first()[0]
        print(f"🧮 Estimated AQI = mean_value × {factor:.2f}")
        df = df.withColumn("aqi", when(col("aqi").isNull(), col("mean_value") * factor).otherwise(col("aqi")))
    
    df = df.fillna({"local_site": "Unknown", "cbsa": "Unknown"})
    
    df.write.mode("append").jdbc(url=jdbc_url, table=table_name, properties=db_properties)
    print(f"✅ {table_name} data appended to PostgreSQL.")


# ------------------ STEP 5: RUN THE PIPELINE ------------------ #
process_gas("Co", "Co")
process_gas("No2", "No2")
process_gas("Ozone", "Ozone")
process_gas("So2", "So2", fill_aqi=True)

print("\n🚀 All datasets processed and loaded to PostgreSQL successfully!")
