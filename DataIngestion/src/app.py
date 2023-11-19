import json
import asyncio
import pandas as pd
import logging
import traceback
import datetime
import boto3

from ReadStocks import stocks_list
from Job import download_job
from Constants import STOCKS_DATA_S3_BUCKET, STOCKS_DATA_S3_BUCKET_PREFIX


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Parse input data from event
        start_date = event.get('start_date', '2023-01-01')
        end_date = event.get('end_date', '2023-11-30')

        # Run the download job
        loop = asyncio.get_event_loop()
        final_nifty_data_df = loop.run_until_complete(download_job(stocks_list, start_date, end_date))

        # Define S3 path
        bucket_name = STOCKS_DATA_S3_BUCKET
        file_path = STOCKS_DATA_S3_BUCKET_PREFIX

        # Write DataFrame to S3 in parquet format

        today = datetime.date.today()
        output_file = f"{file_path}/{today.year}_{today.month}_{today.day}.csv"

        # output_file = f"data/{today.year}_{today.month}_{today.day}.csv"
        final_nifty_data_df.to_csv(index=False)

        s3_client.put_object(Body=final_nifty_data_df.to_csv(index=False), Bucket=bucket_name, Key=output_file)

        # final_nifty_data_df.to_csv('data/2023_stocks.csv', index=False)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':'success'
            })
        }
    except Exception as e:
        # Log the exception
        logger.error(f"Error in lambda_handler: {e}")
        # Extracts the stack trace as a string
        trace_string = traceback.format_exc()

        # Alternatively, you can get more detailed information
        exc_type, exc_value, exc_traceback = traceback.sys.exc_info()

        return {
            'statusCode': 500,
            'body': json.dumps({
                'status':'failed',
                'error':f"Error in lambda_handler: {e}",
                'traceback_details': {
                    'filename': exc_traceback.tb_frame.f_code.co_filename,
                    'lineno': exc_traceback.tb_lineno,
                    'name': exc_traceback.tb_frame.f_code.co_name,
                    'type': exc_type.__name__,
                    'message': str(exc_value),  # or simply use 'str(e)'
                }
            })
        }

# Uncomment for local testing
# if __name__ == "__main__":
#     event = {'start_date': '2023-01-01', 'end_date': '2023-11-30'}
#     response = asyncio.run(lambda_handler(event, None))
#     print(response)
