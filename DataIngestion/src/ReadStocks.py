__all__ = ["stocks_list"]

import pandas as pd
import boto3
import io
from Constants import STOCKS_COMPANY_LIST_PATH, STOCKS_DATA_S3_BUCKET


s3_client = boto3.client('s3')
# stocks_data_path = "data/stocklist.csv"

obj = s3_client.get_object(Bucket=STOCKS_DATA_S3_BUCKET, Key=STOCKS_COMPANY_LIST_PATH)

data = obj['Body'].read().decode('utf-8')
stocks_list = pd.read_csv(io.StringIO(data))

# stocks_list = pd.read_csv(STOCKS_COMPANY_LIST_PATH)
print(stocks_list.info())
