import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pickle 
import asyncio
#defining global variable as this loop keeps throwing error..
stocks = None
def stock_allocation_choice(stockchoices_array):
   for i in stockchoices_array['Pred_Binary']:
        if i == 1:
           stocks = stockchoices_array[stockchoices_array['Pred_Binary'] == 1].index.values     
   return stocks

def stock_symbols_and_names(stocks, stockchoices_array):
        stock_names = []

        for num in stocks:
                stock_names.append(stockchoices_array.iloc[num,0])
                stock_names.sort()
        print(stock_names)

        stock_symbols = []

        for num in stocks:
                stock_symbols.append(stockchoices_array.iloc[num,1])
                stock_symbols.sort()
        print(stock_symbols)

        return stock_names, stock_symbols

def decisionTree(stock_choices):

        # load the trained model from disk
        model_filename = 'CIA_Pred_XGBoost.sav'
        clf_XGB_trained = pickle.load(open(model_filename, 'rb'))

        stockchoices=stock_choices
        print(stock_choices,'in array')

        #compliant payload
        # stockchoices={'Trade Name':['CosmoSteel','SGX','Mapletree Com Tr','AEM','Jason Marine'],
        #       'Trade Code':['DEF','OOO','MMMM','ABC','GHI'],
        #       'RIC':['BCDE.SI','SGXL.SI','MACT.SI','ABCD.SI','CDEF.SI'],
        #       'Sector':['Mineral Resources','Banking & Investment Services','Real Estate','Technology Equipment','Technology Equipment'],
        #       'Size':['SmallCap','LargeCap','LargeCap','MidCap','LargeCap'],
        #       'P/E':[8.28,25.01,5.45,10.25, 2.86],
        #       'Yield':[3.13,3.09,4.63,2.56,4.17],
        #       'GTI':[78.0,121,82,79, 68.0],
        #       'Net Profit':[3.07,43.63,192.16,16.33,13.76],
        #       'ROE':[3.75,41.01,17.82,47.14,19.33],
        #       'Debt/Equity':[39.63,0.00,54.9,0.29,0.00],
        #       'Price/Book':[0.31,8,1.11,2.48,0.60],
        #       '52W Pr':[63.27,31.44,-12.16,80.91,50.00]}
        # input features into an 
        
        stockchoices_array = pd.DataFrame(stockchoices)
        #print(stockchoices_array)

        #slice the array containing feature data
        input_feat = stockchoices_array.iloc[:,[5,7,8,9,10,11,12]]
        #print(input_feat)

        # output the predicted performance & append to last column of dataset?
        #pred_YieldPerf=clf.predict(input_feat)
        pred_YieldPerf=clf_XGB_trained.predict(input_feat)
        #print(pred_YieldPerf)

        # assign predicted values into dataframe
        stockchoices_array['Pred_Binary'] = pred_YieldPerf

        Pred_Label=[]
        for i in stockchoices_array['Pred_Binary']:
                if i == 1:
                        Pred_Label.append('High Yield')
                else:
                        Pred_Label.append('Low Yield')
                
        stockchoices_array['Pred_Label']=Pred_Label
        #print(Pred_Label)
        #print(stockchoices_array)

        PredLabel_dict = dict(zip(stockchoices_array['Trade Name'], stockchoices_array['Pred_Label']))
   
        print(stockchoices_array['Pred_Binary'], 'stockchoices for stock assignment')
        #Placed a function in here, I think the variable stock is being referenced before the for loop with the if check is completed. Dont know how to do a async await here in python..
        stocks = stock_allocation_choice(stockchoices_array)
        while stocks is None:
                pass
        ga_load = stock_symbols_and_names(stocks, stockchoices_array)
        stock_names = ga_load[0]
        stock_symbols = ga_load[1]
        # for i in stockchoices_array['Pred_Binary']:
        #         if i == 1:
        #          stocks = stockchoices_array[stockchoices_array['Pred_Binary'] == 1].index.values
        return PredLabel_dict, stock_names, stock_symbols
        
        # output trade name     
        

     