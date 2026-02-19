from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def apply_quality_rules(df: DataFrame, quality_rules: list) -> list:
    """
    Applies configurable data quality rules to a Spark DataFrame.

    Parameters:
        df (DataFrame): Input Spark DataFrame
        quality_rules (list): List of rule dictionaries defined in JSON config

    Returns:
        list: List of dictionaries with rule name and fail count
    """
    quality_results = []

    for rule in quality_rules:
        name = rule.get('name')
        col = rule.get('column')
        rtype = rule.get('type')

        # Skip rule if column does not exist
        if col not in df.columns:
            quality_results.append({
                "rule": name,
                "fail_count": -1,
                "status": "column_not_found"
            })
            continue

        if rtype == 'not_null':
            fail_count = df.filter(F.col(col).isNull()).count()

        elif rtype == 'unique':
            total = df.count()
            unique = df.select(col).distinct().count()
            fail_count = total - unique

        elif rtype == 'min':
            min_val = rule.get('value', 0)
            fail_count = df.filter(F.col(col) < min_val).count()

        elif rtype == 'date_range':
            start_date = rule.get('start_date')
            end_date = rule.get('end_date')
            fail_count = df.filter(
                (F.col(col) < start_date) | (F.col(col) > end_date)
            ).count()

        else:
            fail_count = 0

        quality_results.append({
            "rule": name,
            "fail_count": fail_count,
            "status": "failed" if fail_count > 0 else "passed"
        })

    return quality_results
