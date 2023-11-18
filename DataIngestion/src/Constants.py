import os

STOCKS_DATA_S3_BUCKET        = os.environ.get('STOCKS_DATA_S3_BUCKET', 'your-bucket-name')
STOCKS_DATA_S3_BUCKET_PREFIX = os.environ.get('STOCKS_DATA_S3_BUCKET_PREFIX', 'parquet prefix')
STOCKS_COMPANY_LIST_PATH     = os.environ.get('STOCKS_DATA_S3_BUCKET_PREFIX', 'data/stocklist.csv')
