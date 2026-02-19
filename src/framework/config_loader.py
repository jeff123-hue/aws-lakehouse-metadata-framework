import boto3
import json

def load_config_from_s3(config_s3_path: str) -> dict:
    """
    Loads a JSON configuration file from S3.

    Parameters:
        config_s3_path (str): Full S3 path to config file (e.g. s3://bucket/path/config.json)

    Returns:
        dict: Parsed JSON configuration
    """
    s3 = boto3.client('s3')

    bucket_name = config_s3_path.split('/')[2]
    key_name = '/'.join(config_s3_path.split('/')[3:])

    obj = s3.get_object(Bucket=bucket_name, Key=key_name)

    return json.loads(obj['Body'].read())
