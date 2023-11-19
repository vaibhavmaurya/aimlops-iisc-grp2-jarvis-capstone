__all__ = ["download_job"]

import asyncio
import aiohttp
import pandas as pd
import io
from typing import List, Dict, Any


def get_timestamp_today():

    # Get today's date
    today = pd.Timestamp.today()

    # Get the timestamp of today's beginning
    start_ts = int(today.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

    # Get the timestamp of today's end
    end_ts = int(today.replace(hour=23, minute=59, second=59, microsecond=999).timestamp())

    print("Start timestamp:", start_ts)
    print("End timestamp:", end_ts)
    return start_ts, end_ts


# Define URL template
URL = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history"

async def download_stock_data(session: aiohttp.ClientSession, company_code: str, company_name: str, start_date: int, end_date: int) -> pd.DataFrame:
    """
    Asynchronously downloads stock data for a given company_code between start and end dates.

    :param session: aiohttp.ClientSession object for making HTTP requests.
    :param company_code: Stock company_code.
    :param start_date: Start date as a timestamp.
    :param end_date: End date as a timestamp.
    :return: DataFrame with stock data.
    """
    url = URL.format(company_code, start_date, end_date)
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                df = pd.read_csv(io.StringIO(data))
                df['company_name'] = company_name
                df['company_code'] = company_code.split('.NS')[0]
                return df
            else:
                print(f"Failed to download data for {company_code}. HTTP status: {response.status}")
                return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while downloading data for {company_code}: {e}")
        return pd.DataFrame()

async def download_job(stocks_list: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Main function to download stock data for multiple company_codes.

    :param stocks_list: DataFrame containing stock company_codes.
    :param start_date: Start date in 'YYYY-MM-DD' format.
    :param end_date: End date in 'YYYY-MM-DD' format.
    :return: DataFrame with combined stock data.
    """
    start_ts = int(pd.to_datetime(start_date).timestamp())
    end_ts = int(pd.to_datetime(end_date).timestamp())

    start_ts, end_ts = get_timestamp_today()

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(download_stock_data(session, row['company_code'], row['company_name'], start_ts, end_ts)) for _, row in stocks_list.iterrows()]
        nifty_data_list = await asyncio.gather(*tasks)

        nifty_data_df = pd.concat(nifty_data_list, ignore_index=True)
        nifty_data_df['Date'] = pd.to_datetime(nifty_data_df['Date'])
        nifty_data_df['year'] = nifty_data_df['Date'].dt.year
        nifty_data_df['month'] = nifty_data_df['Date'].dt.month
        nifty_data_df['day'] = nifty_data_df['Date'].dt.day

        return nifty_data_df

# Example usage
# stocks_list = pd.DataFrame({
#     'company_code': ['ADANIPORTS.NS', 'BAJAJ-AUTO.NS'],
#     'Company Name': ['Adani Ports', 'Bajaj Auto Ltd.']
# })
# start_date = '2023-01-01'
# end_date = '2023-11-30'
# loop = asyncio.get_event_loop()
# nifty_data_df = loop.run_until_complete(main(stocks_list, start_date, end_date))
