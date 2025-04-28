from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col, desc, sum, max, row_number
from pyspark.sql.window import Window
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def main():
    # Initialize Spark with Iceberg configurations
    spark = SparkSession.builder \
        .appName("Kaggle Dataset Analysis") \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
        .config("spark.sql.catalog.spark_catalog.type", "hive") \
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.local.type", "hadoop") \
        .config("spark.sql.catalog.local.warehouse", "/warehouse/iceberg") \
        .getOrCreate()
    
    print("PySpark Session initialized with Iceberg support")
    
    # Create the database if it doesn't exist
    spark.sql("CREATE DATABASE IF NOT EXISTS local.oil_analysis")
    
    print("Loading dataset...")
    df = spark.read.csv("/data/data.csv", header=True, inferSchema=True)
    
    print("Dataset Schema:")
    df.printSchema()
    
    print("Sample Data:")
    df.show(5)
    
    print("What are the top 5 destinations for oil produced in Albania?")
    albania_analysis_df = df.filter(df["originName"]=="Albania").groupBy("destinationName").count().orderBy(desc("count"))
    albania_analysis_df.show(5, False)
    
    # Write to Iceberg table
    print("Writing Albania analysis to Iceberg...")
    
    try:
        # Use Spark SQL to write to Iceberg
        albania_analysis_df.createOrReplaceTempView("albania_temp")
        
        # Create or replace the Iceberg table
        spark.sql("""
        CREATE OR REPLACE TABLE local.oil_analysis.albania_destinations
        USING iceberg
        AS SELECT * FROM albania_temp
        """)
        
        print("Successfully written to Iceberg table: local.oil_analysis.albania_destinations")
        
        # Verify the Iceberg table
        print("Verifying Iceberg table contents:")
        result = spark.sql("SELECT * FROM local.oil_analysis.albania_destinations ORDER BY count DESC LIMIT 5")
        result.show()
    except Exception as e:
        print(f"Error writing to Iceberg: {e}")
    
    # Also save as CSV for backward compatibility
    albania_analysis_df_pandas = albania_analysis_df.toPandas()
    albania_analysis_df_pandas.to_csv("/data/albania_analysis.csv")
    
    print("For UK, which destinations have a total quantity greater than 100,000?")
    uk_analysis_df1 = df.filter(df["originName"]=="United Kingdom").groupBy("destinationName").agg(sum("quantity").alias("sum_qty"))
    uk_analysis_df2 = uk_analysis_df1.filter(uk_analysis_df1["sum_qty"] > 100000)
    uk_analysis_df2.show(10, False)
    uk_analysis_df2_pandas = uk_analysis_df2.toPandas()
    uk_analysis_df2_pandas.to_csv("/data/uk_analysis.csv")
    
    print("What was the most exported grade for each year and origin?")
    max_grade_year_df_1 = df.groupBy("year", "gradeName", "originName").agg(sum("quantity").alias("sum_qty_per_year"))
    max_grade_year_df_1.show(5)
    max_grade_window = Window.partitionBy("year", "originName").orderBy(col("sum_qty_per_year").desc())
    max_grade_year_df2 = max_grade_year_df_1.withColumn("row", row_number().over(max_grade_window)).filter(col("row")==1).drop("row").withColumnRenamed("sum_qty_per_year", "max_quantity")
    max_grade_year_df2.show(10, False)
    
    max_grade_year_df_pandas = max_grade_year_df2.toPandas()
    max_grade_year_df_pandas.to_csv("/data/max_grade_by_year_origin.csv")
    
    print("Analysis complete. Results saved to Iceberg table and CSV files.")
    
    spark.stop()

if __name__ == "__main__":
    main()