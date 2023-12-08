import os

OUTPUT_BUCKET    = os.environ.get('OUTPUT_BUCKET', 'vm-aimlops-2023')
OUTPUT_PREFIX    = os.environ.get('OUTPUT_PREFIX', 'capstone/stocks/stocks_summary/')
LLAMA_MODEL_ID   = os.environ.get('LLAMA_MODEL_ID', 'meta.llama2-13b-chat-v1')
AMAZON_MODEL_ID  = os.environ.get('AMAZON_MODEL_ID', 'amazon.titan-text-express-v1')
TEXT_TOKEN_SIZE  = int(os.environ.get('TEXT_TOKEN_SIZE', '300'))
RES_WORD_SIZE    = int(os.environ.get('RES_WORD_SIZE', '400'))
RES_BULLT_POINTS = int(os.environ.get('RES_BULLT_POINTS', '6'))
MAX_TOKEN_SIZE   = int(os.environ.get('MAX_TOKEN_SIZE', '2000'))

