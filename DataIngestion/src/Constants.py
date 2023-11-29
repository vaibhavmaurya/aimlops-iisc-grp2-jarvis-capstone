import os

STOCKS_DATA_S3_BUCKET        = os.environ.get('STOCKS_DATA_S3_BUCKET', 'vm-aimlops-2023')
STOCKS_DATA_S3_BUCKET_PREFIX = os.environ.get('STOCKS_DATA_S3_BUCKET_PREFIX', 'capstone/stocks/stocks_data')
STOCKS_COMPANY_LIST_PATH     = os.environ.get('STOCKS_COMPANY_LIST_PATH', 'capstone/stocks/stocks_companies/stocklist.csv')
