import json
import boto3
from datetime import datetime
import io
import re
from Constants import OUTPUT_BUCKET, OUTPUT_PREFIX, AMAZON_MODEL_ID, \
                      TEXT_TOKEN_SIZE, RES_WORD_SIZE, RES_BULLT_POINTS, MAX_TOKEN_SIZE
import pandas as pd
from botocore.config import Config
import traceback


s3_client = boto3.client('s3')

my_config = Config(
    region_name = 'us-east-1',
)
boto3_bedrock = boto3.client('bedrock-runtime', config=my_config)


def get_stock_news_df(Bucket, Key):
    try:
        obj = s3_client.get_object(Bucket=Bucket, Key=Key)
    except Exception as e:
        raise Exception(f'''
            Bucket and prefix does not exists, reason: {e}
            Bucket: {Bucket}
            Key   : {Key}
        ''')
    
    data = obj['Body'].read().decode('utf-8')
    return pd.read_csv(io.StringIO(data))


def save_to_s3(df):
    # Write DataFrame to S3 in parquet format

    todays_date = datetime.now().strftime('%d-%m-%Y')
    output_file = f"{OUTPUT_PREFIX}summary-{todays_date}.csv"

    # output_file = f"data/{today.year}_{today.month}_{today.day}.csv"
    # final_nifty_data_df.to_csv(index=False)

    s3_client.put_object(Body=df.to_csv(index=False), Bucket=OUTPUT_BUCKET, Key=output_file)
    return f"s3://{OUTPUT_BUCKET}/{output_file}"



def build_prompt(text, company_code, company_name):
    return f'''Following is the financial news about the company {company_name}, which is in short called as {company_code}.:
               {text}                  
            Provide the summary of the above financial news in {RES_WORD_SIZE} words with maximum {RES_BULLT_POINTS} bullet points. Exclude any which is not related to the
            company {company_name} and the company name in short form {company_code}
            '''


def call_bedrock(prompt):
    params = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4000,
                "stopSequences": [],
                "temperature":0,
                "topP":1
                }
            } 
    body = json.dumps(params)
    modelId = AMAZON_MODEL_ID   
    accept = 'application/json'
    contentType = 'application/json'
    response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    # response_content = response.get('body').read().decode('utf-8')
    response_content = response.get('body').read().decode('utf-8')
    # response_body = json.loads(response_content)
    # Convert JSON string to a Python dictionary
    parsed_data = json.loads(response_content)
    
    # Extract the outputText from the first item in the results list
    return parsed_data['results'][0]['outputText']


def clean_summary(summary):
    # Modify the text: remove all whitespace except for spaces
    summary = re.sub(r'[\t\n\r]+', '', summary)
    
    # Replace multiple spaces with a single space
    return re.sub(r'\s+', ' ', summary)



def build_summary(df):
    summary_response = []
    for i, row in df.iterrows():
        summary = ''
        error = ''
        try:
            if row['token_by_space'] <= TEXT_TOKEN_SIZE:
                summary = row['complete_text']
            else:
                prompt = build_prompt(row['complete_text'][:MAX_TOKEN_SIZE], row['company_code'], row['company_name'])
                summary = call_bedrock(prompt)
                summary = summary if summary is not None else summary
                summary = clean_summary(summary)
        except Exception as e:
            print(f'''
                    Error Occurred while building summary, Reason: {e}
                    company : {row['company_code']}
                    url     : {row['url']}
                   ''')
            error = f"Error Occurred while building summary, Reason: {e}"
        summary_response.append({
            'date'         :row['date'],
            'company_code' :row['company_code'],
            'url'          :row['url'],
            'summary'      :summary,
            'error'        :error
        })
    
    return pd.DataFrame(summary_response)



def lambda_handler(event, context):
    try:
        # Parse input data from event
        # s3_news_path = "s3://vm-aimlops-2023/capstone/stocks/stocks_news/2023_12_3.csv"

                # 'stock_news_load_status':'FAILED',
                # 'stock_news_load_location':f'',
                # 'stock_news_load_failed_reason':f"Error: {e}"

        news_ingest_response = event['event_data']
        print('News Ingest data came here')
        print(news_ingest_response)

        if news_ingest_response['stock_news_load_status'] == 'FAILED':
             raise Exception(f'''
                The previous step the News Ingest FAILED
            ''') 
        s3_news_path = news_ingest_response['stock_news_load_location'] 
        # 
        # Regular expression pattern to match the S3 bucket and the file prefix
        pattern = r"s3://([^/]+)/(.+\.csv)"

        # Extracting the S3 bucket and the file prefix
        match = re.search(pattern, s3_news_path)
        if match:
            s3_bucket = match.group(1)
            file_prefix = match.group(2)
            print(f'''
                    INPUT
                      s3_bucket  : {s3_bucket}
                      file_prefix: {file_prefix}
            ''')
        else:
            raise Exception(f'''
                The S3 file Path is not valid: {s3_file_path}
            ''')         

        # Run the download job
        df_news = get_stock_news_df(Bucket=s3_bucket, Key=file_prefix)
        df_summary = build_summary(df_news)
        s3_file_path = save_to_s3(df_summary)
        # print(df_summary)

        # event['event_data']
        return {
            'statusCode': 200,
            'body': {
                'stock_summary_load_status':'SUCCESS',
                'stock_summary_load_location':s3_file_path,
                'stock_summary_load_failed_reason':""
            }
        }
    except Exception as e:
        # Log the exception
        # logger.error(f"Error in lambda_handler: {e}")
        # # Extracts the stack trace as a string
        traceback.print_exc()

        # # Alternatively, you can get more detailed information
        # exc_type, exc_value, exc_traceback = traceback.sys.exc_info()

        return {
            'statusCode': 500,
            'body': {
                'stock_summary_load_status':'FAILED',
                'stock_summary_load_location':f'',
                'stock_summary_load_failed_reason':f"Error: {e}"
                }
            
        }
