from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_gold_layer(df: DataFrame, gold_config: dict) -> DataFrame:
    """
    Builds the Gold layer DataFrame based on configuration.

    Parameters:
        df (DataFrame): Input Spark DataFrame (Raw layer)
        gold_config (dict): Gold layer configuration from JSON

    Returns:
        DataFrame: Aggregated Gold DataFrame
    """

    group_cols = gold_config.get("group_by", [])
    metrics = gold_config.get("metrics", [])

    agg_expressions = []

    for metric in metrics:
        column_name = metric.get("column")
        agg = metric.get("agg")
        alias = metric.get("alias")

        if agg == "count":
            agg_expressions.append(F.count("*").alias(alias))

        elif agg == "sum":
            agg_expressions.append(F.sum(column_name).alias(alias))

        elif agg == "avg":
            agg_expressions.append(F.avg(column_name).alias(alias))

    # If no grouping columns provided, return original df
    if not group_cols:
        return df

    return df.groupBy(group_cols).agg(*agg_expressions)
