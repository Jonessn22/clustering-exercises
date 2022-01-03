##################################################################################| FILE USED TO WRANGLE ZILLOW



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


##################################################################################| ACQUIRE

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
def acquire_data(file_name, database, query):
    '''
THIS FUNCTION TAKES IN:
    (1) A CSV FILE NAME ***MAKE SURE YOU INCLUDE .CSV EXT*** 
    (2) DATABASE NAME AND 
    (3) SQL QUERY STRING 
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
        df = pd.read_csv(file_name)
        
    # or, if no local csv file
    else:

        # url database connection string 
        url = f'mysql+pymysql://{user}:{password}@{host}/{database}'

        # reading sql query into df using sql query and url string
        df = pd.read_sql(query, url)
        
        # write df to local csv file
        df.to_csv(file_name)
    
    return df 

##################################################################################| SUMMARIZE AND VISUALIZE

###############################################################| SUMMARIZE DATA FUNCTION
def summarize_data(df, num_unique_cols):
    '''
THIS FUNCTIONS TAKES IN A DATAFRAME AND THE MAX NUMBER OF UNIQUE COLUMN VALUES TO 
PRINT VALUE_COUNTS FOR AND PRINTS THE FOLLOWING SUMMARY INFORMATION:
    1) DF SHAPE, NUMBER OF ROWS AND COLUMNS
    2) DF INFO
    3) THE UNIQUE VALUES IN THE DF COLUMNS (NUMBER AND, IF <= 10, EACH UNIQUE VALUE)
    4) THE DESCRIPTIVE STATS FOR THE DF NUMERICAL COLUMNS
RETURNING A PREVIEW, THE FIRST FIVE ROWS, OF THE DATAFRAME
    '''
    
    preview = df.head()
    
    print('1) DataFrame Shape'.upper())
    print('-' * len('DataFrame Shape'))
    print(f'Rows: {df.shape[0]}\nColumns: {df.shape[1]}')
    print()
    print()
    
    print('2) DataFrame Info'.upper())
    print('-' * len('DataFrame Info'))
    print(df.info())
    print()
    print()
    
    print('3) Unique Values by Column'.upper())
    print('-' * len('Unique Values by Column'))
    
    unique_cols = []
    for col in df.columns:
        if df[col].nunique() <= num_unique_cols:
            print(col.upper())
            print('-' * len(col))
            print(f'Number of Unique Values for {col}: {df[col].nunique()}')
            print(df[col].value_counts(dropna = False))
            unique_cols.append(col)
            print()
            
        else:
            print(col.upper())
            print('-' * len(col))
            print(f'Number of Unique Values for {col}: {df[col].nunique()}')
            print(f'This column has > {num_unique_cols} values')
            print()
        print()
            
    print()
    print('4) Descriptive Stats'.upper())
    print('-' * len('Descriptive Stats'))
    print(df.describe())
    print()
            
    return preview

###############################################################| PLOT COLUMN HISTOGRAMS FUNCTIONS

def hist_data(df):
    '''
THIS FUNCTION TAKES IN A DF AND PLOTS A HISTOGRAM FOR EACH COLUMN.
    '''
    df.hist(figsize=((36), 32), bins=20)
    plt.tight_layout();
    
###############################################################| SEE NULLS FUNCTIONS
def nulls_by_col(df):
    '''
THIS FUNCTION TAKES IN A DATAFRAME AND RETURNS THE NUMBER OF ROWS MISSING FOR EACH COLUMN AND THE 
PERCENTAGE OF MISSING MISSING ROWS TO TOTAL ROWS. THE VALUES ARE SORTED IN DESCENDING ORDER BY THE PERCENTAGE MISSING.

LASTLY, THE NUMBER OF MISSING ROWS FOR EACH COLUMN IS PLOTTED IN A HISTOGRAM.
    '''

    num_missing_rows = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing_rows / rows
    
    nulls_by_col_df = pd.DataFrame({'num_missing_rows': num_missing_rows, 'pct_rows_missing': pct_missing})\
    .sort_values(by = 'pct_rows_missing', ascending = False)\
    .reset_index().rename(columns = {'index': 'attribute'})
    
    nulls_by_col_df.num_missing_rows.hist(figsize=(8, 4), bins = 100)
    plt.title('Distribution of Missing Rows for Each Column')
    
    return nulls_by_col_df


def nulls_by_row(df):
    '''
THIS FUNCTION TAKES IN A DATAFRAME AND RETURNS INFORMATION ABOUT THE NUMBER OF COLUMN VALUES
MISSING FROM EACH ROW. 
    1) COL 1 IS THE NUMBER OF COLUMN VALUES MISSING
    2) COL 2 IS THE NUMBER OF ROWS WITH THAT MANY (COL 1) COLUMN VALUES MISSING
    3) COL 3 IS THE PERCENTAGE OF COLUMN VALUES MISSING TO THE TOTAL NUMBER OF COLUMNS
    
THIS INFORMATION IS RETURNED IN THE FORM OF A DATAFRAME AND SORTED IN DESCENDING ORDER BY THE
PERCENTAGE OF COLUMN VALUES MISSING.
    '''
    
    df2 = pd.DataFrame(df.isnull().sum(axis = 1), columns = ['num_cols_missing']).reset_index()\
    .groupby('num_cols_missing').count().reset_index().rename(columns = {'index': 'num_rows'})
    
    df2['pct_cols_missing'] = df2.num_cols_missing / df.shape[1]
    
    df2 = df2.sort_values(by = 'pct_cols_missing', ascending = False)
    
    return df2


###############################################################| VISUALIZE OUTLIERS
def outlier_boxplots(df):
    '''
THIS FUNCTION TAKES IN A DATAFRAME AND, FOR ALL NUMERIC COLUMNS, DISPLAYS HORIZONTAL
BOXPLOTS ALLOWING OUTLIERS TO BE VISUALIZED. IF A COLUMN IS NON-NUMERIC THEN THE COLUMN
NAME ALONG WITH A PRINT STATEMENT WILL BE EXECUTED.
    '''
    
    for col in df.columns:
        if df[col].dtypes != 'O':
            print(col.upper())
            sns.boxplot(x = col, data = df)
            plt.show()
            print()
            print()
        else:
            print(f'{col.upper()} is a nonnumeric dtype')
            print()
            print()


##################################################################################| PREPARE
###############################################################| REMOVE SELECT COLUMNS
def remove_cols(df, cols_to_remove):
    '''
THIS FUNCTION TAKES IN A DF AND A LIST OF COLUMNS TO BE REMOVED AND 
RETURNS A DF WITHOUT THOSE COLUMNS.
    '''
    
    df = df.drop(columns = cols_to_remove)
    
    return df


###############################################################| FILTER ONE UNIT PROPERTIES
def one_unit_filters(df):
    '''
    
    '''
    
    #filtering rows with > 1 unit count
    df2 = df[df.unitcnt == 1]
    
    #filtering rows with bedroomcnt > 5
    df2 = df2[df2.bedroomcnt <= 5]
    
    #filtering propertylandtypeuseid
    df2 = df2[df2.propertylandusetypeid.isin([260, 261, 263, 265, 266])]
    
    return df2


###############################################################| HANDLE NULLS (MISSING VALUES)
def handle_missing_values(df, prop_req_cols, prop_req_rows):
    '''
THIS FUNCTION TAKES IN A DATAFRAME AND REMOVES NULL VALUES FROM COLUMNS 
AND THEN ROWS USING THE RESPECTIVE PROPORTIONS FED INTO IT USING THE 
DROPNA() FUNCTION.
    '''
    
    # to get the minimum non-null value threshold for keeping for keeping a column
    # a column must have at least this many non null values to be kept in the final df
    threshold = round(prop_req_cols * len(df.index))
    
    # takes in the above threshold and completes permanent drop of columns with less than
    # that many non null values
    df.dropna(axis =1, thresh = threshold, inplace = True)
    
    # to get the minimum non-null value threshold for keeping for keeping a row
    # a row must have at least this many non null values to be kept in the final df
    threshold = round(prop_req_rows * len(df.columns))
    
    # takes in the above threshold and completes permanent drop of columns with less than
    # that many non null values
    df.dropna(axis = 0, thresh = threshold, inplace = True)
    
    return df    


##################################################################################| MALL WRANGLE FUNCTIONS
def outlier_function(df, cols, k):
    '''
THIS FUNCTION TAKES IN A DATAFRAME, A LIST OF COLUMNS TO HAVE OUTLIERS REMOVED FROM
    '''
    for col in df[cols]:
        q1 = df.annual_income.quantile(0.25)
        q3 = df.annual_income.quantile(0.75)
        iqr = q3 - q1
        upper_bound =  q3 + k * iqr
        lower_bound =  q1 - k * iqr     
        df = df[(df[col] < upper_bound) & (df[col] > lower_bound)]
    return df


def wrangle_mall_df():
    '''
THIS FUNCTION ACQUIRES AND WRANGLES THE MALL DATA. FIRST REMOVING OUTLIERS, THEN
CREATING NUMERICAL DUMMY COL FOR CATEGORICAL GENDER COL, AND THEN SPLITTING THE DATA.
    '''
    
    # acquire data
    sql = 'select * from customers'
    mall_df = acquire_data('mall_data.csv', 'mall_customers', sql)
    
    # handle outliers
    mall_df = outlier_function(mall_df, ['age', 'spending_score', 'annual_income'], 1.5)
    
    # get dummy for gender column
    dummy_df = pd.get_dummies(mall_df.gender, drop_first=True)
    mall_df = pd.concat([mall_df, dummy_df], axis=1).drop(columns = ['gender'])
    mall_df.rename(columns= {'Male': 'is_male'}, inplace = True)

    # split the data in train, validate and test
    train, test = train_test_split(mall_df, train_size = 0.8, random_state = 123)
    train, validate = train_test_split(train, train_size = 0.75, random_state = 123)
    
    return mall_df, train, validate, test

def min_max_scaler(train, valid, test):
    '''
    Uses the train & test datasets created by the split_my_data function
    Returns 3 items: mm_scaler, train_scaled_mm, test_scaled_mm
    This is a linear transformation. Values will lie between 0 and 1
    '''
    num_vars = list(train.select_dtypes('number').columns)
    
    scaler = MinMaxScaler(copy=True, feature_range=(0,1))
    
    train[num_vars] = scaler.fit_transform(train[num_vars])
    
    valid[num_vars] = scaler.transform(valid[num_vars])
    
    test[num_vars] = scaler.transform(test[num_vars])
    
    return scaler, train, valid, test