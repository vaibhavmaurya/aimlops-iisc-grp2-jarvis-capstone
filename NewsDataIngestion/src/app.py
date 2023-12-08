import json
import asyncio
import re
from bs4 import BeautifulSoup
from datetime import datetime
import aiohttp
import os
import boto3
import io
import pandas as pd
import traceback
from Constants import OUTPUT_BUCKET, OUTPUT_PREFIX, STOCK_BUCKET, STOCK_PREFIX


# OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
# OUTPUT_PREFIX = os.environ['OUTPUT_PREFIX']

# STOCK_BUCKET = os.environ['STOCK_BUCKET']
# STOCK_PREFIX = os.environ['STOCK_PREFIX']


s3_client = boto3.client('s3')


def get_stock_df():
    obj = s3_client.get_object(Bucket=STOCK_BUCKET, Key=STOCK_PREFIX)
    
    data = obj['Body'].read().decode('utf-8')
    stocks_list = pd.read_csv(io.StringIO(data))
    return stocks_list



async def fetch_financial_news_by_url(session, url):
    async with session.get(url) as response:
        if response.status is 200:
            return BeautifulSoup(await response.text(), 'html.parser')
        else:
            print(f"Error fetching financial news for {url}: {response.status}")
            return None


def remove_whitespace(text):
    # Adjusted regular expression pattern to remove additional whitespace characters like \t, \n, etc., but keep spaces
    pattern_additional_whitespace = r'[\t\n\r\f\v]'
    text = text.replace("\'", r"").replace('@','')
    
    # Performing the replacement with the updated pattern
    return re.sub(pattern_additional_whitespace, '', text)



def find_article_body(data):
    # Check if the data is a dictionary   
    if isinstance(data, dict):
        # If the key 'articleBody' is in the dictionary, return its value
        if 'articleBody' in data:
            return data['articleBody']
        # Otherwise, recursively search in the values of the dictionary
        for key, value in data.items():
            result = find_article_body(value)
            if result is not None:
                return result
    # Check if the data is a list
    elif isinstance(data, list):
        # Recursively search in each item of the list
        for item in data:
            result = find_article_body(item)
            if result is not None:
                return result
    # Return None if 'articleBody' is not found
    return None


def get_texts_soup_json(soup):
    json_texts = []
    script_tags = soup.find_all('script', {'type': 'application/json'})
    if script_tags:
        for script_tag in script_tags:
            json_texts.append(script_tag.text)
    return json_texts
    

def get_texts_soup_json_lrd(soup):
    json_texts = []
    for item in soup.find_all('script', {'type': 'application/ld+json'}):
        # print(item)
        try:
            m = json.loads(remove_whitespace(item.text))
            text = find_article_body(m)
            json_texts.append(text)
        except:
            pass
    json_texts = [x for x in json_texts if x is not None]
    if len(json_texts) == 0:
        return None
    else:
        return " ".join([x for x in json_texts if x is not None])


def get_texts_soup_from_p(soup):
    p_texts = []
    p_tags = soup.find_all('p')
    if p_tags:
        for p_tag in p_tags:
            p_texts.append(p_tag.text.strip())
        return " ".join(list(set(p_texts)))
    else:
        return None



async def get_all_news_for_company():
    all_texts = []
    all_companies_urls = []
    today_date = datetime.now().strftime("%Y-%m-%d")

    news_url = "https://www.google.com/finance/quote/{}:NSE"
    
    df_all_companies = get_stock_df()

    async with aiohttp.ClientSession() as session:

        all_companies = [row['company_code'].split('.NS')[0] for _, row in df_all_companies.iterrows()]
        all_search    = [row['search_term'] for _, row in df_all_companies.iterrows()]
        
        tasks = [asyncio.create_task(fetch_financial_news_by_url(session, news_url.format(x))) for x in all_companies]
        company_news_soup_list = await asyncio.gather(*tasks)

        
        for company, soup, search_term in zip(all_companies, company_news_soup_list, all_search):
            if soup is None:
                all_texts.append({
                    'date':today_date,
                    'company_code': company,
                    'url': '',
                    'complete_text': '',
                    'char_length': 0,
                    'token_by_space': 0,
                    'error':'Soup failed'
                })
            else:
                all_companies_urls.append({
                    'company':company,
                    'urls':list(set([div.find('a').get('href') for div in soup.find_all('div', class_='z4rs2b')])),
                    'search_term':search_term
                })

        # print(all_companies_urls)
                
        # company_news_soup = await fetch_financial_news_by_url(session, news_url)
        # all_urls = [div.find('a').get('href') for div in company_news_soup.find_all('div', class_='z4rs2b')]

        for company_url in all_companies_urls:

            all_urls = company_url['urls']
            company_code = company_url['company']
            search_term = company_url['search_term']
            # tasks = [fetch_financial_news_by_url(session, url) for url in all_urls]
            tasks = [asyncio.create_task(fetch_financial_news_by_url(session, url)) for url in all_urls]
            url_soups = await asyncio.gather(*tasks)
    
            for url_soup, url in zip(url_soups, all_urls):
                print(f"Reading the URL: {url}")
                complete_text = ""
                if url_soup is not None:
                    p_texts = get_texts_soup_from_p(url_soup)
                    json_lrd_texts = get_texts_soup_json_lrd(url_soup)
                    complete_text = p_texts if p_texts is not None and search_term in p_texts.lower() else complete_text
                    complete_text = complete_text + " " + json_lrd_texts if json_lrd_texts is not None and search_term in json_lrd_texts.lower() else complete_text
                    all_texts.append({
                        'date':today_date,
                        'company_code': company_code,
                        'url': url,
                        'complete_text': complete_text,
                        'char_length': len(complete_text),
                        'token_by_space': len(complete_text.split(" ")),
                        'error':''
                    })
                else:
                    all_texts.append({
                        'date':today_date,
                        'company_code': company_code,
                        'url': url,
                        'complete_text': "",
                        'char_length': 0,
                        'token_by_space': 0,
                        'error':'soup has failed'
                    })
    return all_texts


def save_to_s3(df):
    # Write DataFrame to S3 in parquet format

    # today = datetime.now()
    todays_date = datetime.now().strftime('%d-%m-%Y')
    output_file = f"{OUTPUT_PREFIX}stock-news-{todays_date}.csv"

    # output_file = f"data/{today.year}_{today.month}_{today.day}.csv"
    # final_nifty_data_df.to_csv(index=False)

    s3_client.put_object(Body=df.to_csv(index=False), Bucket=OUTPUT_BUCKET, Key=output_file)
    return f"s3://{OUTPUT_BUCKET}/{output_file}"



def lambda_handler(event, context):
    try:
        # Parse input data from event

        # Run the download job
        loop = asyncio.get_event_loop()
        complete_data = loop.run_until_complete(get_all_news_for_company())
        df_complete = pd.DataFrame(complete_data)

        # Define S3 path
        s3_file_path = save_to_s3(df_complete)

        print("DOWNLOAD Job is completed")
        
        # 'stock_news_load_status': {'S': 'PENDING'},
        # 'stock_news_load_location': {'S': 'EMPTY'},
        # 'stock_news_load_failed_reason': {'S': 'EMPTY'},

        return {
            'statusCode': 200,
            'body': {
                'stock_news_load_status':'SUCCESS',
                'stock_news_load_location':s3_file_path,
                'stock_news_load_failed_reason':""
            }
        }
    except Exception as e:
        # Log the exception
        # logger.error(f"Error in lambda_handler: {e}")
        # # Extracts the stack trace as a string
        trace_string = traceback.format_exc()
        print(trace_string)

        # # Alternatively, you can get more detailed information
        # exc_type, exc_value, exc_traceback = traceback.sys.exc_info()

        return {
            'statusCode': 500,
            'body': {
                'stock_news_load_status':'FAILED',
                'stock_news_load_location':f'',
                'stock_news_load_failed_reason':f"Error: {e}"
                }
            
        }
