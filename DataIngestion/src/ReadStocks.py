__all__ = ["stocks_list"]

import pandas as pd
from Constants import STOCKS_COMPANY_LIST_PATH


stocks_data_path = "data/stocklist.csv"
stocks_list = pd.read_csv(STOCKS_COMPANY_LIST_PATH)
print(stocks_list.info())
