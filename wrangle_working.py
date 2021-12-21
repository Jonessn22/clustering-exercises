######################################################################## FILE USED TO ACQUIRE AND WRANGLE ZILLOW

###############################################################| IMPORTS
import os

#stored db credentials (use ignore file to hide)
import env

#python libraries
import numpy as np
import pandas as pd

#visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

#sklearn library
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


###############################################################| CONNECTION FUNCTION
def get_connection(db):
    '''
THIS FUNCTION TAKES IN A DB FROM SQL SERVER AND USES THE SERVER CREDENTIALS FROM ENV
FILE TO RETURN A STRING THAT WILL BE USED TO CONNECT TO THE SQL SERVER. 
    '''
    #server access credentials
#    from env import host, user, password
    
    #url connection string
    return f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{db}'


###############################################################| SQL QUERY
qry_zillow = '''
SELECT prop.*, 
       pred.logerror, 
       pred.transactiondate, 
       air.airconditioningdesc, 
       arch.architecturalstyledesc, 
       build.buildingclassdesc, 
       heat.heatingorsystemdesc, 
       landuse.propertylandusedesc, 
       story.storydesc, 
       construct.typeconstructiondesc 

FROM   properties_2017 prop  
       INNER JOIN (SELECT parcelid,
       					  logerror,
                          Max(transactiondate) transactiondate 
                   FROM   predictions_2017 
                   GROUP  BY parcelid, logerror) pred
               USING (parcelid) 
       LEFT JOIN airconditioningtype air USING (airconditioningtypeid) 
       LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid) 
       LEFT JOIN buildingclasstype build USING (buildingclasstypeid) 
       LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid) 
       LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid) 
       LEFT JOIN storytype story USING (storytypeid) 
       LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid) 
WHERE  prop.latitude IS NOT NULL 
       AND prop.longitude IS NOT NULL AND transactiondate <= '2017-12-31'; 
            '''


###############################################################| ACQUIRE DATA FUNCTION
def acquire_data(file_name, db, qry):
    '''
THIS FUNCTION TAKES IN A CSV FILE NAME, A DB FROM THE SQL SERVER, AND A SQL QUERY. IF THE 
FILE EXISTS IN THE LOCAL DIRECTORY IT WILL WRITE IT TO A DF. IF IT DOES NOT IT WILL USE THE 
DB AND CONNECTION FUNCTION TO WRITE THE SQL QUERY TO A DB AND THEN WRITE THE QUERY TO A CSV 
TO BE SAVED LOCALLY.
    '''
    
    # if csv data file already exists in local directory...
    if os.path.isfile(file_name):
        
        # write the data to dataframe
        df = pd.read_csv(file_name)
    
    # if csv data file does not exist in local direction ...
    else:
        
        #url string from preceding function, uses to establish server connection
        url = get_connection(db)

        #writing sql query to df
        df = pd.read_sql(qry, url)
        
        #saving data as a csv file locally
        df.to_csv(file_name)
    
    return df


###############################################################| 