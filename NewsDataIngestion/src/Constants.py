import os

OUTPUT_BUCKET    = os.environ.get('OUTPUT_BUCKET', 'vm-aimlops-2023')
OUTPUT_PREFIX    = os.environ.get('OUTPUT_PREFIX', 'capstone/stocks/stocks_news/')
STOCK_BUCKET     = os.environ.get('STOCK_BUCKET', 'vm-aimlops-2023')
STOCK_PREFIX     = os.environ.get('STOCK_BUCKET', 'capstone/stocks/stocks_companies/stocklist_truncated.csv')
