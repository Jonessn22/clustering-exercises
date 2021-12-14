from env import user, host, password

import pandas as pd

import os
def get_connection(db, user = user, host = host, password = password):
    '''
THIS FUNCTION TAKES IN A DATABASE AND SQL SERVER CREDENTIALS, RETURNING THE STRING THAT WILL BE
USED TO ACCESS AND CONNECT TO THAT SERVER.
    '''
    
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def acquire_data(file_name, db):
    '''

    '''
    
    # if csv data file already exists in local directory...
    if os.path.isfile(file_name):
        
        # write the data to dataframe
        df = pd.read_csv(file_name)
    
    # if csv data file does not exist in local direction ...
    else:
        
        # read the sql query used to dataframe
        sql_query = '''SELECT *
                        FROM properties_2017
                        LEFT JOIN airconditioningtype ON airconditioningtypeid
                        LEFT JOIN architecturalstyletype ON architecturalstyletypeid
                        LEFT JOIM buildingclasstype ON buildingclasstype
                        LEFT JOIN heatingorsystemtype ON heatingorsystemtypeid
                        LEFT JOIN predictions_2017 ON parcelid
                        LEFT JOIN propertylandusetype ON propertylandusetypeid
                        LEFT JOIN storytype ON storytypeid
                        LEFT JOIN typeconstructiontype ON typeconstructiontypeid

                    '''
        df = pd.read_sql(sql_query, get_connection(db))
        
        # cache csv file with data
        # df.to_csv('zillow.csv')
        
    return df

