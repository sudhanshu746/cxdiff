import pandas as pd
import sys


file=sys.argv[1]
pd.read_csv(file,  encoding='utf8').to_excel(f"{file.split('.')[0]}.xlsx", index=False, sheet_name='Sheet1', engine='openpyxl')