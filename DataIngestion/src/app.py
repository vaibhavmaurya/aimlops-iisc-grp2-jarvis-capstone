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
sqs = boto3.client('sqs')

YOUR_SQS_QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/135671745449/aimlops-grp2-jarvis-casptone-stockingestion-schedule'


def delete_queue_message(reciept_handle):
    # Delete the message from the queue
    response = sqs.delete_message(
        QueueUrl=YOUR_SQS_QUEUE_URL,
        ReceiptHandle=reciept_handle
    )

    print("QUEUE Deleted Successfully")

    return response


def lambda_handler(event, context):
    try:
        # Parse input data from event

        # Run the download job
        loop = asyncio.get_event_loop()
        final_nifty_data_df = loop.run_until_complete(download_job(stocks_list))

        # Define S3 path
        bucket_name = STOCKS_DATA_S3_BUCKET
        file_path = STOCKS_DATA_S3_BUCKET_PREFIX

        # Write DataFrame to S3 in parquet format

        todays_date = datetime.datetime.now().strftime('%d-%m-%Y')
        output_file = f"{file_path}/stock-prices-{todays_date}.csv"

        # output_file = f"data/{today.year}_{today.month}_{today.day}.csv"
        final_nifty_data_df.to_csv(index=False)

        s3_client.put_object(Body=final_nifty_data_df.to_csv(index=False), Bucket=bucket_name, Key=output_file)

        # final_nifty_data_df.to_csv('data/2023_stocks.csv', index=False)
        if (event.get('Records', '@') != '@') and (event['Records'][0].get('receiptHandle', '@') != '@'):
            delete_queue_message(event['Records'][0]['receiptHandle'])

        print("DOWNLOAD Job is completed")

        return {
            'statusCode': 200,
            'body': {
                'stock_data_load_status':'SUCCESS',
                'stock_data_load_location':f's3://{bucket_name}/{output_file}',
                'stock_data_load_failed_reason':""
            }
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
            'body': {
                'stock_data_load_status':'FAILED',
                'stock_data_load_location':f'',
                'stock_data_load_failed_reason':f"Error: {e}"
                }
            
        }

# Uncomment for local testing
# if __name__ == "__main__":
#     event = {'start_date': '2023-01-01', 'end_date': '2023-11-30'}
#     response = asyncio.run(lambda_handler(event, None))
#     print(response)
