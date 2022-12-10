import json, csv
import pandas as pd
import config
from datetime import datetime, timedelta



dfArr = pd.DataFrame (columns = ['day', 'month', 'year', 'dow','hour', 'min', 'depICAO', 'craftType', 'airline'])
dfDep = pd.DataFrame (columns = ['day', 'month', 'year', 'dow','hour', 'min', 'arrICAO', 'craftType', 'airline'])

dfArr.to_csv('arrData.csv', sep=',')
dfDep.to_csv('depData.csv', sep=',')


print(dfArr.head())
print(dfDep.head())

