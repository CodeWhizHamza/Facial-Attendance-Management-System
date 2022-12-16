import pandas as pd
from config import *

cols = ['DateTime', *list(courses)]
table = pd.DataFrame(columns=cols)
# print(cols)
record = pd.Series(['15-12-2022-900', 'A', 'P', 'A',
                   'P', 'P', 'P', 'A', 'A'], index=cols)


table = table.append(record, ignore_index=True)
table = table.append(record, ignore_index=True)
table = table.append(record, ignore_index=True)
table = table.append(record, ignore_index=True)

table.to_csv('test.csv', sep=',')
