import warnings
warnings.filterwarnings("ignore")

import wrangle

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

np.random.seed(4)



def kmeans_model(train, feat_cols, scaler, min_k, max_k):
    '''
THIS FUNCTION TAKES IN A DF OF MODEL TRAINING DATA, A LIST OF THE FEATURES THAT WILL BE USED FOR MODELING, A SCALING
OBJECT (StandardScaler OR MinMaxScaler), minimum and (maximum - 1) for range of k_clusters predictions, AND THE ORIGINAL
DF. IT RETURNS THE ORIGINAL DF WITH A PREDICTION COLUMNS FOR EACH OF THE (max_k - 1) CLUSTERS. 
    '''

    #selecting features for features df - X
    X = train[feat_cols]
    
    #scale features prior to modeling
    scaler_object = scaler.fit(X)
    X_scaled = pd.DataFrame(scaler_object.transform(X), columns = X.columns)
    
    #for loop to create a df with n - 1 columns for each cluster prediction from range(min_k, (max - 1)_k)
    for n in range(min_k, max_k):
    
        #creating kmeans model object
        kmeans = KMeans(n_clusters = n)

        #fitting data to model
        kmeans.fit(X_scaled)
        
        #adding predictions column to original df
        pred_df = X_scaled
        pred_df[f'{n}_clusters'] = kmeans.predict(pred_df)
        
    #making sure X_scaled is only feature columns, does not include predictions columns
    X_scaled = X_scaled[feat_cols]
        
    return X, X_scaled, pred_df


def visualize_clusters(pred_df, x, y):
    '''
 THIS FUNCTION TAKES IN A DATAFRAME OF ORIGINAL DATA ALONG WITH EACH N_CLUSTERS MODEL PREDICTION COLUMN AND PLOTS
 A SCATTERPLOT FOR EACH N_CLUSTERS COLUMN, WITH EACH CLUSTER IN A DIFFERENT COLOR. 
    '''
    
    for col in pred_df.columns:
        
        if col not in [x, y]:
            
            pred_df[col] = 'cluster_' + pred_df[col].astype(str)

            sns.relplot(data = pred_df, x = x, y = y, hue = col)

            plt.title(f'{col}')

            plt.show()

            print()
            
            
def plot_inertia(X_scaled, min_k_range, max_k_range):
    '''
THIS FUNCTION TAKES IN X (A DF OF MODEL FEATURES), A MIN VALUE FOR THE K RANGE AND A MAX VALUE - 1 FOR THE
K RANGE AND CREATES A LINE PLOT WITH THE INERTIA (ON THE Y AXIS) PLOTTED AGAINST EACH K VALUE (ON THE X AXIS).
    '''
    
    with plt.style.context('seaborn-whitegrid'):
        
        pd.Series({k: KMeans(k).fit(X_scaled).inertia_ for k in range(min_k_range, max_k_range)}).plot(marker = 'x')
        
        plt.xticks(range(min_k_range, max_k_range))
        
        plt.title('Change in Inertia as k Increases')
        
        plt.show()
        
        
    
    

