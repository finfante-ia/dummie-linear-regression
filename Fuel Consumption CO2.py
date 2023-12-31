# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 02:14:22 2023

@author: finfa
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split


class LR_hue:
    def __init__(self):
        self.fitted=False
        
    def fit(self, X, y, hue):
        self.hue=hue
        self.hue_features=[]
        self.hue_features=X[hue].unique()
        self.dict_lr={}
        yre=[]
        yhatre=[]
        for hue_feature in self.hue_features:
            xh=X[X[hue]==hue_feature].drop(hue, axis=1).to_numpy()
            yh=y[X[hue]==hue_feature].to_numpy()
            yre=np.concatenate((yre, yh))
            self.dict_lr[hue_feature]=LinearRegression()
            self.dict_lr[hue_feature].fit(xh, yh)
            yhat=self.dict_lr[hue_feature].predict(xh)
            yhatre=np.concatenate((yhatre, yhat))
            
        print('training accuracy score:', metrics.mean_squared_error(yre,yhatre))
        print('training r2_score:', metrics.r2_score(yre,yhatre))
        print('training mean_absolute_error:', metrics.mean_absolute_error(yre,yhatre))   
        
        self.fitted=True    
        #return self.dict_lr
        
    def check_fitted(self):
        if not self.fitted:
            raise ValueError("NotFittedError")
            
    def predict(self, X):
        self.check_fitted()
        hue=self.hue
        y=X.copy()[[]]       #create empty y to store predictions keeping the indexes from X
        y['yhat']=np.nan
        for hue_feature in self.hue_features:
            xh=X[X[hue]==hue_feature].drop(hue, axis=1)
            pr=self.dict_lr[hue_feature].predict(xh.to_numpy())
            pr=pd.DataFrame(pr, columns=['yhat'], index=xh.index) # store predictions with original x.index used
            y.update(pr) #only update the values in y where indexes from pr matches
        return y['yhat']
    
    def get_params(self):
        self.check_fitted()
        df_params=pd.DataFrame(columns=['Variable','params'])
        for hue_feature in self.hue_features:
            df_params.loc[len(df_params.index)]=[hue_feature, self.dict_lr[hue_feature].get_params()]
        return df_params
    
    def coef_(self):
        self.check_fitted()
        df_params=pd.DataFrame(columns=['Variable','coef_'])
        for hue_feature in self.hue_features:
            df_params.loc[len(df_params.index)]=[hue_feature, self.dict_lr[hue_feature].coef_]
        return df_params        
    
    def intercept_(self):
        self.check_fitted()
        df_params=pd.DataFrame(columns=['Variable','coef_'])
        for hue_feature in self.hue_features:
            df_params.loc[len(df_params.index)]=[hue_feature, self.dict_lr[hue_feature].intercept_]
        return df_params     

    def scores(self,X,y):
        self.check_fitted()
        y=y.to_frame()
        hue=self.hue
        yhat=self.predict(X).to_frame()
        df_params=pd.DataFrame(columns=[hue,'Accuracy', 'R2', 'MSE', 'MAE'])
        for hue_feature in self.hue_features:
            yhath=yhat[X[hue]==hue_feature]
            yh=y[X[hue]==hue_feature]
            df_params.loc[len(df_params.index)]=[hue_feature, metrics.mean_squared_error(yh,yhath), metrics.r2_score(yh,yhath), metrics.mean_squared_error(yh,yhath) ,metrics.mean_absolute_error(yh,yhath)]
        df_params.loc[len(df_params.index)]=['Total', metrics.mean_squared_error(y,yhat), metrics.r2_score(y,yhat), metrics.mean_squared_error(y,yhat) ,metrics.mean_absolute_error(y,yhat)]
        return df_params        


df=pd.read_csv('FuelConsumptionCo2.csv')        

X=df[['ENGINESIZE', 'CYLINDERS' ,'FUELTYPE', 'FUELCONSUMPTION_CITY','FUELCONSUMPTION_HWY', 'FUELCONSUMPTION_COMB' ,'FUELCONSUMPTION_COMB_MPG']]
y=df['CO2EMISSIONS']

X_train, X_test, Y_train, Y_test = train_test_split(X,y, test_size=0.2, random_state=2)

lr=LR_hue()

lr.fit(X_train,Y_train,'FUELTYPE')

y_hat=lr.predict(X_test)

print('Test accuracy score:', metrics.mean_squared_error(Y_test,y_hat))
print('Test r2_score:', metrics.r2_score(Y_test,y_hat))
print('Test mean_absolute_error:', metrics.mean_absolute_error(Y_test,y_hat))
