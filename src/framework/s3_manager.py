from pyspark.sql import DataFrame


def read_dataset(spark, bucket: str, prefix: str, file_format: str) -> DataFrame:
    """
    Reads a dataset from S3.

    Parameters:
        spark: SparkSession
        bucket (str): S3 bucket name
        prefix (str): S3 prefix/path inside the bucket
        file_format (str): File format (e.g., 'parquet', 'csv', 'json')

    Returns:
        DataFrame: Spark DataFrame loaded from S3
    """
    path = f"s3://{bucket}/{prefix}"
    return spark.read.format(file_format).load(path)


def write_parquet(df: DataFrame, path: str, partitions: list = None, mode: str = "overwrite") -> None:
    """
    Writes a DataFrame to S3 in Parquet format.

    Parameters:
        df (DataFrame): Spark DataFrame to write
        path (str): Full S3 path (e.g., s3://bucket/raw/table/)
        partitions (list, optional): Columns to partition by
        mode (str): Write mode ('overwrite', 'append')
    """
    if partitions:
        df.write.mode(mode).partitionBy(partitions).parquet(path)
    else:
        df.write.mode(mode).parquet(path)
