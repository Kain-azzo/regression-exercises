import pandas as pd
import numpy as np
import env
from sklearn.model_selection import train_test_split
import os




def check_file_exists(file, query, url):
    '''checks for file, then creates if it does not exist'''
    if os.path.exists(file):
        print('this file exists, reading csv')
        frame = pd.read_csv(file, index_col=0)
    else:
        print('this file doesnt exist, read from sql, and export to csv')
        frame = pd.read_sql(query, url)
        frame.to_csv(file)
        
    return frame



def get_zillow():
    '''aquires data'''
    query = '''select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from propertylandusetype
        join properties_2017
            using (propertylandusetypeid)
    WHERE propertylandusedesc = ("Single Family Residential")'''
    url = env.get_db_url("zillow")
    file = 'zillow.csv'
    frame = check_file_exists(file, query, url)
   
    return frame


def prep_zillow(zillow):
    '''Takes the data frame and gets rid of unnecessary data converts isp charges data into a usable format for modeling''' 
    zillow = get_zillow()
    zillow = zillow.dropna()
    zillow = zillow.rename(columns = {'bedroomcnt':'bedrooms',
                     'bathroomcnt':'bathrooms',
                     'calculatedfinishedsquarefeet':'area',
                     'taxvaluedollarcnt':'taxvalue',
                     'fips':'county'})
    
    zillow.yearbuilt = zillow.yearbuilt.astype(int)
    zillow.area = zillow.area.astype(int)
    zillow.bedrooms = zillow.bedrooms.astype(int)
    zillow.taxvalue = zillow.taxvalue.astype(int)
    zillow.area = zillow.area.astype(int)
    zillow.county = zillow.county.map({6037:'LA',6059:'Orange',6111:'Ventura'})
    
    return zillow


def wrangle_zillow(zillow):
    '''Gets prepped data'''
    zillow = prep_zillow(get_zillow())

    return zillow


def split_data(df):
    '''Takes the data frame and breaks it into train, test, and split information, with two splits'''
    train, validate_test = train_test_split(df,
                     train_size=0.6,
                     random_state=123)
                  
    validate, test = train_test_split(validate_test,
                                     train_size=0.5,
                                     random_state=123)
                                    
    return train,validate,test

def X_y_split(df, target):
    '''
    This function takes in a dataframe and a target variable
    Then it returns the X_train, y_train, X_validate, y_validate, X_test, y_test
    and a print statement with the shape of the new dataframes
    '''  
    train, validate, test = split_data(df)

    X_train = train.drop(columns= target)
    y_train = train[target]

    X_validate = validate.drop(columns= target)
    y_validate = validate[target]

    X_test = test.drop(columns= target)
    y_test = test[target]
        
    # Have function print datasets shape
    print(f'X_train -> {X_train.shape}')
    print(f'X_validate -> {X_validate.shape}')
    print(f'X_test -> {X_test.shape}')  
    
    return X_train, y_train, X_validate, y_validate, X_test, y_test

def disc_cols(df):
    '''determine if column is continous or discrete(categorical'''
    cat_cols= df.select_dtypes(include=['object']).columns.tolist()
    return cat_cols

def cont_cols(df):
    num_cols= df.select_dtypes(exclude=['object']).columns.tolist()
    return num_cols





