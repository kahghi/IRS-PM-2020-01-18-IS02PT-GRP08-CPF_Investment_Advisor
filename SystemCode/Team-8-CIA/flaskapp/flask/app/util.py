from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error
from pydash import py_
import pandas as pd
from collections import defaultdict
import array as arr
import json as json
import numpy as np


#Init App
# app = Flask(__name__)


# def get_all_

def establish_conection(sql_query):
    try:
        #database connection string
        connection = psycopg2.connect(host = "localhost", 
                            database = "TEAM", 
                            port = "5432",
                            user="NUS", 
                            password="NUSMTECH")
        cursor = connection.cursor()
        postgreSQL_select_Query =  sql_query
        cursor.execute(postgreSQL_select_Query)
        record = cursor.fetchall()
        return record


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
        
def rules_score_assign(array_of_scores):
        print('rules scores assign in util')
        print(array_of_scores[0], array_of_scores[1], 'values')
        string_array = map(str, array_of_scores)
        sql_query = f"select array_to_json(array_agg(row_to_json(d)))from (select \"Schwab\".\"Score\", \"Schwab\".\"RiskType\"from \"public\".\"Schwab\" WHERE  \"UniqueID\" IN ('{array_of_scores[0]}','{array_of_scores[1]}','{array_of_scores[2]}','{array_of_scores[3]}','{array_of_scores[4]}','{array_of_scores[5]}','{array_of_scores[6]}')) d"
        record = establish_conection(sql_query)
        object_list_of_results = record[0][0]
        print(object_list_of_results)
        object_list_of_results = record[0][0]
        print(object_list_of_results)
        #separate it into individual riskTypes
        group_results = py_.group_by(object_list_of_results, 'RiskType')
        #Assign to new objects
        th_object = group_results['TH']
        rt_object = group_results['RT']
        print(th_object, 'th_object')
        print(rt_object)
        #intialise variables for sum #TH risktypes only consists of 2 questions
        th_score = 0
        rt_score = 0

        for i in range(len(th_object)):
            th_score += th_object[i]['Score']
        
        for i in range(len(rt_object)):
            rt_score += rt_object[i]['Score']
        
        
        print(th_score, rt_score, 'scores in data access layer')
        return th_score, rt_score

def select_all_categories():
#method to get all of the categories from db
    sql_query = f"Select \"public\".\"SGX Data\".\"Sector\" from \"public\".\"SGX Data\" GROUP BY \"public\".\"SGX Data\".\"Sector\""
    results = establish_conection(sql_query)
    return results


def select_specific_categories(selected_sectors):
    print(selected_sectors, 'in select specific methods, print payload')
    print(selected_sectors[0], 'first result')
    result_0 = selected_sectors[0] 
    result_1 = selected_sectors[1] 
    result_2 = selected_sectors[2]  
    result_3 = selected_sectors[3] 
    sql_query = f"SELECT * FROM \"public\".\"SGX Data\" WHERE \"public\".\"SGX Data\".\"Sector\" = '{result_0}' OR \"public\".\"SGX Data\".\"Sector\" = '{result_1}' OR \"public\".\"SGX Data\".\"Sector\" = '{result_2}' OR \"public\".\"SGX Data\".\"Sector\" = '{result_3}'"
    results = establish_conection(sql_query)
    # json_results = json.dumps(results)
    # print(json_results, 'jsonified')
    
    return results


def prof_assign(time,risk):
    print('in prof assign')
    df = pd.read_csv("app/Profile Assignment.csv", index_col=0)
    input_dict_time = {'3 - 4':[3,4], '7 - 9':[7,8,9], '10 - 12':[10,11,12],'14 - 18':list(range(14,19))}
    input_dict_risk = {'0 - 10':list(range(0,11)),'40':list(range(40,45))}

    # Exception Handling for time risk score
    if time in (1,2):
        return {
            "Error": "Your investment time horizon is shorter than our expected timeline for calculations. \nIf you would like to invest, we would like to reccomend the CPF Special Account"
            }
    else:
        for key,values in input_dict_time.items():
            if time in values:
                time = key
        else:
            time = str(time)
                    
        for key,values in input_dict_risk.items():
            if risk in values:
                risk = key
        else:
            risk = str(risk)
    
        
    
    return df.loc[time,risk]

def transformation_for_decision_tree(selected_stocks):
    sql_query = f"SELECT * FROM \"public\".\"SGX Data\" WHERE \"public\".\"SGX Data\".\"RIC\" IN ('{selected_stocks[0]}','{selected_stocks[1]}','{selected_stocks[2]}','{selected_stocks[3]}')"
    print(sql_query, 'query string')
    results = establish_conection(sql_query)
    array_results = np.asarray(results)
    print(array_results, 'array results')
       

    stockchoices = {
        'Trade Name':[],
        'Trade Code':[],
        'RIC':[],
        'Sector':[],
        'Size':[],
        'P/E':[],
        'Yield':[],
        'GTI':[],
        'Net Profit':[],
        'ROE':[],
        'Debt/Equity':[],
        'Price/Book':[],
        '52W Pr':[]
    }
    for x in array_results:
        stockchoices['Trade Name'].append(x[0])
        stockchoices['Trade Code'].append(x[1])
        stockchoices['RIC'].append(x[1])
        stockchoices['Sector'].append(x[7])
        stockchoices['Size'].append(x[2])
        stockchoices['P/E'].append(float(x[3]))
        stockchoices['Yield'].append(float(x[4]))
        stockchoices['GTI'].append(float(x[5]))
        stockchoices['Net Profit'].append(float(x[6]))
        stockchoices['ROE'].append(float(x[8]))
        stockchoices['Debt/Equity'].append(float(x[9]))
        stockchoices['Price/Book'].append(float(x[10]))
        stockchoices['52W Pr'].append(float(x[11]))
         
    print(stockchoices, 'STOCK CHOPICESSSASDAD')
    return stockchoices


     #test prediction based on AEM, CosmoSteel, Mapletree, SGX and Jason Marine (low,low,high = 0,0,1,0,1)
        # stockchoices={'Trade Name':['CosmoSteel','SGX','Mapletree Com Tr','AEM','Jason Marine'],
        #         'Trade Code':['DEF','OOO','MMMM','ABC','GHI'],
        #         'RIC':['BCDE.SI','SGXL.SI','MACT.SI','ABCD.SI','CDEF.SI'],
        #         'Sector':['Mineral Resources','Banking & Investment Services','Real Estate','Technology Equipment','Technology Equipment'],
        #         'Size':['SmallCap','LargeCap','LargeCap','MidCap','LargeCap'],
        #         'P/E':[8.28,25.01,5.45,10.25, 2.86],
        #         'Yield':[3.13,3.09,4.63,2.56,4.17],
        #         'GTI':[78.0,121,82,79, 68.0],
        #         'Net Profit':[3.07,43.63,192.16,16.33,13.76],
        #         'ROE':[3.75,41.01,17.82,47.14,19.33],
        #         'Debt/Equity':[39.63,0.00,54.9,0.29,0.00],
        #         'Price/Book':[0.31,8,1.11,2.48,0.60],
        #         '52W Pr':[63.27,31.44,-12.16,80.91,50.00]}
# results = rules_score_assign(['helo','hello'])
# print(results)
# input_time = 18
# input_risk = 40
# print(input_risk, 'input risk')
# print(type(input_risk))
# risk_category = prof_assign(input_time, input_risk)
# print(risk_category)





# @app.route('/score', methods =['POST'])
# def get_score():
    # RulesTable = rulesTable.query.all()
    # return jsonify({'RulesTable':RulesTable})

#Run Server
# if __name__ == '__main__':
#     app.run(debug=True)



#Ditching ORM as it is becoming a hassle instead of increasing productivity, using Raw SQL instead below are all the alchemy codes
# --------------------------------------------------------------------------------------------------------------------------------------------

# from flask_sqlalchemy import SQLAlchemy, get_debug_queries
# from flask_marshmallow import Marshmallow

# basedir  = os.path.abspath(os.path.dirname(__file__))
# underlying sqlachemy it utilises psycopg2 so scrapping away all of sql alchemy
#sqlalchem connection string
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jaxvndnjtymzmo:92828596218ce31380246e8f65af40aff0e96bed5d6a4884441982535c634ba8@ec2-54-88-130-244.compute-1.amazonaws.com/daokjnadb02aqo'
# app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# ma = Marshmallow(app)

# db model
# class rulesTable(db.Model):
#     UniqueID = db.Column(db.Integer, primary_key = True)
#     Answers = db.Column(db.String)
#     Score = db.Column(db.Integer)
#     RiskType = db.Column(db.String)
#     QuestionNo = db.Column(db.String)

# def __init__(self, UniqueID, Answers, Score, RiskType, QuestionNo):
#     self.UniqueID = UniqueID
#     self.Answers = Answers
#     self.Score = Score
#     self.RiskType = RiskType
#     self.QuestionNo = QuestionNo

#sql debugging
# def sql_debug(response):
#     queries = list(get_debug_queries())
#     query_str = ''
#     total_duration = 0.0
#     for q in queries:
#         total_duration += q.duration
#         stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
#         query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))
#     print ('=' * 80)
#     print ('SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
#     print ('=' * 80)
#     print ((query_str).rstrip('\n'))
#     print ('=' * 80 + '\n')
#     return response
# app.after_request(sql_debug)