import os
import pandas as pd
from env import host, user, password


def acquire_data(file_name, index_col, database, query):
    '''
THIS FUNCTION TAKES IN:
    (1) A CSV FILE NAME ***MAKE SURE YOU INCLUDE .CSV EXT*** 
    (2) COLUMN FROM TABLE TO BE USED AS DATAFRAME INDEX
    (3) DATABASE NAME AND 
    (4) SQL QUERY STRING 
AND RETURNS A PANDAS DF BY:
        (i.) CHECKING TO SEE IF LOCAL CSV FILE WITH DATA EXISTS
        (ii.) WRITING THE LOCAL CSV FILE OT PANDAS DF 
OR, IF LOCAL CSV DOES NOT EXIST:
        (i.) IMPORTING DATABASE CONNECTION CREDENTIALS
        (ii.) USING CREDENTIALS TO CREATE DATABASE CONNECTION STRING
        (iii.) READING THE SQL QUERY INTO A DF
        (iv.) CACHING DF AND SAVING DATA AS LOCAL CSV FILE
    '''
    # checking for local csv file
    if os.path.isfile(file_name):
        
        # reading csv file to pandas df
        df = pd.read_csv(file_name, index_col = index_col)
        
    # if no local csv file
    else:

        # url database connection string
        url = f'mysql+pymysql://{user}:{password}@{host}/{database}'

        # reading sql query into df using query, url string, and index_col parameter
        df = pd.read_sql(query, url, index_col)
        
        # write df to local csv file
        df.to_csv(file_name)
    
    return df   