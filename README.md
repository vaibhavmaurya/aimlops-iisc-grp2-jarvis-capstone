


# Stock Data Ingestion and Processing

This script is designed for stock data ingestion and processing, intended to be deployed as an AWS Lambda function. It utilizes several AWS services, including S3 for storage and SQS for messaging.

## Table of Contents
1. [Overview](#overview)
2. [Key Components](#key-components)
3. [Functionality](#functionality)
4. [Usage](#usage)

## Overview

The script performs the following key tasks:
1. **Data Download**: Uses an asynchronous download job to fetch stock data based on a predefined list of stocks.
2. **Data Storage**: Stores the fetched data in AWS S3 in CSV format.
3. **Queue Handling**: Interacts with an AWS SQS queue to manage messages related to the ingestion process.

## Key Components

- **AWS Services**: Utilizes Boto3 to interact with AWS services such as S3 and SQS.
- **Asynchronous Processing**: Employs asyncio for handling asynchronous operations.
- **Logging and Error Handling**: Implements logging for tracking the script's operations and includes detailed error handling and traceback logging.

## Functionality

- `lambda_handler(event, context)`: The main handler for the AWS Lambda function. It triggers the data download and storage process, handles exceptions, and logs errors. The function also manages the deletion of SQS messages upon successful data processing.

## Usage

To use this script:
1. Deploy it as an AWS Lambda function.
2. Ensure that the necessary AWS resources (S3 bucket, SQS queue) are correctly configured.


# Financial News Aggregation and Processing

This script is dedicated to aggregating and processing financial news for various companies, designed to operate as an AWS Lambda function. It integrates with various AWS services and web scraping techniques.

## Table of Contents
1. [Overview](#overview)
2. [Key Components](#key-components)
3. [Functionality](#functionality)
4. [Usage](#usage)

## Overview

The script carries out several important tasks:
1. **News Aggregation**: Fetches financial news from specified URLs using asynchronous web scraping.
2. **Data Processing**: Processes and cleans the scraped data for further analysis.
3. **Data Storage**: Stores the processed data in AWS S3 in CSV format.

## Key Components

- **AWS Boto3**: Manages interactions with AWS services like S3.
- **Asynchronous Web Scraping**: Utilizes `aiohttp` and `asyncio` for efficient and non-blocking web scraping.
- **Data Cleaning**: Implements various functions to clean and organize the scraped data.
- **Error Handling**: Includes comprehensive error handling and logging capabilities.

## Functionality

- `get_stock_df()`: Retrieves a list of stocks from S3 and returns a DataFrame.
- `fetch_financial_news_by_url(session, url)`: Asynchronously fetches news content from a given URL.
- `remove_whitespace(text)`, `find_article_body(data)`, `get_texts_soup_json(soup)`, `get_texts_soup_json_lrd(soup)`, `get_texts_soup_from_p(soup)`: Various functions to process and clean the scraped HTML and JSON data.
- `get_all_news_for_company()`: Main function to orchestrate the scraping of financial news for all listed companies.
- `save_to_s3(df)`: Saves the processed data to an S3 bucket in CSV format.
- `lambda_handler(event, context)`: The AWS Lambda handler function that initiates the scraping process and handles the storage of data.

## Usage

To deploy this script:
1. Set up as an AWS Lambda function.
2. Ensure AWS resources like S3 buckets are properly configured.
3. Trigger the Lambda function to start the news aggregation process.

*Note: Modify the environment variables and configurations as per your AWS setup.*


# Stock News Summary Generation

This script focuses on generating summaries of financial news articles related to various companies, intended to be deployed as an AWS Lambda function. It leverages AWS services and a summarization model for processing.

## Table of Contents
1. [Overview](#overview)
2. [Key Components](#key-components)
3. [Functionality](#functionality)
4. [Usage](#usage)

## Overview

The script executes several critical tasks:
1. **Data Retrieval**: Fetches stock news data from an S3 bucket.
2. **Summary Generation**: Uses a natural language processing model to generate summaries of financial news.
3. **Data Storage**: Saves the generated summaries to AWS S3 in CSV format.

## Key Components

- **AWS Boto3 and Bedrock**: Interacts with AWS services, including S3 for storage and Bedrock for accessing the summarization model.
- **Data Cleaning and Processing**: Includes functions for cleaning and preparing text data for summarization.
- **Error Handling**: Implements comprehensive error handling and logging mechanisms.

## Functionality

- `get_stock_news_df(Bucket, Key)`: Retrieves stock news data from an S3 bucket and returns a DataFrame.
- `save_to_s3(df)`: Saves the DataFrame to an S3 bucket in CSV format.
- `build_prompt(text, company_code, company_name)`: Constructs a prompt for the summarization model based on the news text.
- `call_bedrock(prompt)`: Invokes the Bedrock model to generate a summary of the provided text.
- `clean_summary(summary)`: Cleans the generated summary by removing excessive whitespace and formatting issues.
- `build_summary(df)`: Processes each news article in the DataFrame to generate summaries.
- `lambda_handler(event, context)`: The AWS Lambda handler function that orchestrates the summary generation and storage process.

## Usage

To deploy this script:
1. Set it up as an AWS Lambda function.
2. Configure AWS resources, such as S3 buckets and Bedrock model access.
3. Trigger the Lambda function, which will process the stock news data and generate summaries.

*Note: Adjust the environment variables and AWS configurations according to your specific setup.*

3. Trigger the Lambda function through AWS services or by sending events in the expected format.

*Note: For local testing, uncomment the code block at the end of the script.*

