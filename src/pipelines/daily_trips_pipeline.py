config = load_config_from_s3(CONFIG_S3_PATH)

df = read_dataset(
    spark,
    config['source']['bucket'],
    config['source']['prefix'],
    config['source']['format']
)

quality_results = apply_quality_rules(df, config['quality_rules'])

write_parquet(df, raw_path, partitions)

df_gold = build_gold_layer(df, config['gold_layer'])

write_parquet(df_gold, gold_path, gold_partitions)