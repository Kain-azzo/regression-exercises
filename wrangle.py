import pandas as pd
import numpy as np
import env
from sklearn.model_selection import train_test_split
import os




# def check_file_exists(file, query, url):
  
#     if os.path.exists(file):
#         print('this file exists, reading csv')
#         frame = pd.read_csv(file, index_col=0)
#     else:
#         print('this file doesnt exist, read from sql, and export to csv')
#         frame = pd.read_sql(query, url)
#         frame.to_csv(file)
        
#     return frame


def wrangle_zillow_stuff():
    file = 'zillow.csv'
    query = '''select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from propertylandusetype
        join properties_2017
            using (propertylandusetypeid)
    WHERE propertylandusedesc = ("Single Family Residential")'''
    url = env.get_db_url("zillow")
#     frame = check_file_exists(file, query, url)
    zillow = pd.read_sql(query,url)
    zillow = zillow.dropna()
    zillow.yearbuilt = zillow.yearbuilt.astype(int)
    zillow.fips = zillow.fips.astype(int)
    zillow.bedroomcnt = zillow.bedroomcnt.astype(int)
    zillow.taxvaluedollarcnt = zillow.taxvaluedollarcnt.astype(int)
    zillow.rename(columns={"calculatedfinishedsquarefeet": "calfinsqft"}, inplace=True)
    zillow.calfinsqft = zillow.calfinsqft.astype(int)
    
    return frame



# def wrangle_zillow(fin=wrangle_zillow_stuff(), target_column=wrangle_zillow_stuff()"taxamount"):
#     '''Takes the data frame and breaks it into train, test, and split information, with two splits'''

#     # Use the specified target column for stratification
#     target = fin[target_column]

#     train, validate_test = train_test_split(fin,
#                      train_size=0.6,
#                      random_state=123,
#                      stratify=target
#                     )

#     validate, test = train_test_split(validate_test,
#                                      train_size=0.5,
#                                      random_state=123,
#                                      stratify=validate_test[target]
#                                     )

#     return train, validate, test





