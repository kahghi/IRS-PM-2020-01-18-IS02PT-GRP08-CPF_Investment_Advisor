# import psycopg2
# from psycopg2 import Error
# from pydash import py_
# import numpy as np
# import pandas as pd
# import json as json
# import functools 
# import operator  
# import logging
# from util import *
# from decisiontree import *
# from ga_optimiser import *
# from flask import Flask, request, jsonify, Response, make_response
# try:
#     from flask_cors import CORS, cross_origin  # The typical way to import flask-cors
# except ImportError:
#     # Path hack allows examples to be run without installation.
#     import os
#     parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     os.sys.path.insert(0, parentdir)
#     from flask_cors import CORS, cross_origin
# # Response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
# # Response.headers['Access-Control-Allow-Methods'] = "GET, HEAD, OPTIONS, POST, PUT"
# # Response.headers['Access-Control-Allow-Headers'] = "Access-Control-Allow-Headers, Access-Control-Allow-Origin"
# #subclassing for response
# # class MyResponse(Response):
# #     pass
# # class MyFlask(Flask):
# #     response_class = MyResponse

# #Init App
# app = Flask(__name__, instance_relative_config=True)
# cors = CORS(app)
# # app.config['CORS_HEADERS'] = 'Content-Type'
# # cors = CORS(app, resources={r"/*/*": {"origins": "http://localhost:3000"}})
# # app.config['CORS_HEADERS'] = ['Content-Type']
# # app.config['CORS_METHODS'] = "GET,POST,OPTIONS"
# #  support_credentials=True, 
# # app.config['CORS_METHODS'] = "GET,POST,OPTIONS"
# logging.getLogger('flask_cors').level = logging.DEBUG

# #handlers ----------------------------------------------------------------------------------------

# def all_categories_handler():
#     categories = select_all_categories()
#     newArray = []
#     for x in categories:
#         if all(x):
#             string =  ''.join(x) 
#             newArray.append(string)
#     return newArray

# def selected_categories_handler(selected_cat):
#     print(selected_cat, 'in selected cat handler')
#     selected_categories = select_specific_categories(selected_cat)
#     # results = np.asarray(selected_categories)
#     results = selected_categories
#     print(results)
#     end_result = {'Data': {}}
#     for x in results:
#         records = x
#         key = records[7]

#         if key not in end_result['Data']:
#             end_result['Data'][key] = []
#             new_array = []
#             new_array.append(records[0])
#             new_array.append(records[1])
#             end_result['Data'][key].append(new_array)
#         else:
#             new_array = []
#             new_array.append(records[0])
#             new_array.append(records[1])
#             print(new_array,'added records')
#             end_result['Data'][key].append(new_array)
#     return end_result

# def decisiontree_handler(payload_to_sql):
#     #selected stock consists of pulling up of table, formatting to datatable and passing to engine
#     formatted_stock_results = transformation_for_decision_tree(payload_to_sql)
#     return formatted_stock_results

# def rulesEngine_handler(rules_payload):

#     print(rules_payload, 'in handleerrrrrr')
#     rtthpayload = rules_score_assign(rules_payload)
#     print(rtthpayload[0], 'rules payload')
#     print(rtthpayload[1], 'rules payload')
#     print('rulessss')
#     rules_time_score = rtthpayload[0]
#     rules_risk_score = rtthpayload[1]
#     print('initialising prof assign')
#     risk_profile = prof_assign(rules_time_score,rules_risk_score)
#     # if 'Error' in risk_profile["Data"]:
#     #     resp_payload = {"Error": risk_profile["Data"]["Error"]}
#     # resp_payload = {"Profile": risk_profile}
#     # print(resp_payload,'end handler')
#     return risk_profile

# def ga_handler(ga_payload, AmountCPFOA, risk_profile_string):
#     # rules_time_score = rules_score_assign(ga_payload)
#     # rules_risk_score = rules_score_assign(ga_payload)
#     # risk_profile = prof_assign(rules_time_score,rules_risk_score)
#     ga_returns = main_wrapper(ga_payload, AmountCPFOA, risk_profile_string)
#     return ga_returns

# #End of Handlers ----------------------------------------------------------------------------------------


# #Routes  ----------------------------------------------------------------------------------------
# @app.route('/decisiontree', methods =['POST'])
# def yieldselection():
#     req4 = request.get_json(silent=True, force=True)
#     selected_stocks = req4["Data"]["Selected_Stocks"]
#     payload_to_sql = []
#     for x in selected_stocks:
#         payload_to_sql.append(x["Code"])
#     print(payload_to_sql, 'sql payload')
#     compliant_payload_for_tree = decisiontree_handler(payload_to_sql)
#     yield_results = decisionTree(compliant_payload_for_tree)
#     print(yield_results)
#     final_response = {'Data': yield_results[0]}
#     Res = Response(json.dumps(final_response), status=200, content_type="application/json")
#     Res.headers.add('Access-Control-Allow-Origin', '*')
#     return Res

# @app.route('/categories/curated', methods =['POST'])
# # @cross_origin(headers=['Content-Type'], origin='localhost')
# def selected_categories():
#     print(request, 'request body')
#     req2 = request.get_json(silent=False, force = True)
#     print(req2, 'request')
#     transformed = req2["Data"]
#     selected_cat = transformed
#     selected_categories = selected_categories_handler(selected_cat)
#     Res = Response(json.dumps(selected_categories), status=200, content_type="application/json")
#     Res.headers.add('Access-Control-Allow-Origin', '*')
#     return Res
    
#     # return Response(json.dumps(selected_categories), status=200, content_type="application/json" headers=["Access-Control-Allow-Origin"])

# @app.route('/categories', methods = ['GET'])
# def all_categories():
#     categories = all_categories_handler()
#     resp = {
#         "Data": categories
#     }
#     print(categories, 'new array')
#     return Response(json.dumps(resp), status=200, content_type="application/json")

# @app.route('/rules', methods = ['POST'])
# def check_rules(): 
#     req = request.get_json(silent=True, force=True)
#     print(req["Data"]["Rules"], 'rules payload')
#     rules_payload = req["Data"]["Rules"]
#     print(rules_payload, 'rules payload')
#     risk_profile_string = rulesEngine_handler(rules_payload)
#     print(risk_profile_string, 'rules end')
#     resp = {"Data": risk_profile_string }
#     Res = Response(json.dumps(resp), status=200, content_type="application/json")
#     print(type(Res))
#     Res.headers.add('Access-Control-Allow-Origin', '*')
#     return Res

# @app.route('/ga', methods =['POST'])
# @cross_origin(headers=['Content-Type'], origin='localhost')
# def ga_master():
#     print('in ga master')
#     req = request.get_json(silent=True, force=True)
#     selected_stocks = req["Data"]["Selected_Stocks"]
#     rules_payload = req["Data"]["Rules"]
#     AmountCPFOA = req["Data"]["CPFOA"]
#     payload_to_sql = []
#     for x in selected_stocks:
#         payload_to_sql.append(x["Code"])
#     print(payload_to_sql, 'sql payload')
#     compliant_payload_for_tree = decisiontree_handler(payload_to_sql)
#     yield_results = decisionTree(compliant_payload_for_tree)
#     risk_profile_string = rulesEngine_handler(rules_payload)
#     final_page_returns = ga_handler(yield_results[1], AmountCPFOA, risk_profile_string)
#     resp = {
#         "Data": {
#             "best_return":final_page_returns[0],
#             "optimal_risk":final_page_returns[1],
#             "risk_profile":risk_profile_string,
#             "stock_allocation":final_page_returns[2],
#             "CPFOA":final_page_returns[3],
#             "rules_risk": final_page_returns[4]
#         }
#     }
#     print(resp, 'final payload')
#     print('rules end')
#     Res = Response(json.dumps(resp),status=200, content_type="application/json")
#     print(type(Res))
#     return Res
    
#     # return Response(json.dumps(resp), status=200, content_type="application/json")
        
# # @app.route('/categories/0)

# # def get_score():
#     # RulesTable = rulesTable.query.all()
#     # return jsonify({'RulesTable':RulesTable})

# # Run Server
# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)



# #Ditching ORM as it is becoming a hassle instead of increasing productivity, using Raw SQL instead below are all the alchemy codes
# # --------------------------------------------------------------------------------------------------------------------------------------------

# # from flask_sqlalchemy import SQLAlchemy, get_debug_queries
# # from flask_marshmallow import Marshmallow

# # basedir  = os.path.abspath(os.path.dirname(__file__))
# # underlying sqlachemy it utilises psycopg2 so scrapping away all of sql alchemy
# #sqlalchem connection string
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jaxvndnjtymzmo:92828596218ce31380246e8f65af40aff0e96bed5d6a4884441982535c634ba8@ec2-54-88-130-244.compute-1.amazonaws.com/daokjnadb02aqo'
# # app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

# # db = SQLAlchemy(app)
# # ma = Marshmallow(app)

# # db model
# # class rulesTable(db.Model):
# #     UniqueID = db.Column(db.Integer, primary_key = True)
# #     Answers = db.Column(db.String)
# #     Score = db.Column(db.Integer)
# #     RiskType = db.Column(db.String)
# #     QuestionNo = db.Column(db.String)

# # def __init__(self, UniqueID, Answers, Score, RiskType, QuestionNo):
# #     self.UniqueID = UniqueID
# #     self.Answers = Answers
# #     self.Score = Score
# #     self.RiskType = RiskType
# #     self.QuestionNo = QuestionNo

# #sql debugging
# # def sql_debug(response):
# #     queries = list(get_debug_queries())
# #     query_str = ''
# #     total_duration = 0.0
# #     for q in queries:
# #         total_duration += q.duration
# #         stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
# #         query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))
# #     print ('=' * 80)
# #     print ('SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
# #     print ('=' * 80)
# #     print ((query_str).rstrip('\n'))
# #     print ('=' * 80 + '\n')
# #     return response
# # app.after_request(sql_debug)