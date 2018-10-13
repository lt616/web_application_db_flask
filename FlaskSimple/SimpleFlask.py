# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request

import SimpleBO 

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)


# @app.route('/api/people/<primary_key>', methods=['GET']) 
# def get_resource(primary_key):

#     result = SimpleBO.find_people_by_primary_key(primary_key)

#     if result:
#         return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
#     else:
#         return "NOT FOUND", 404 


def preprocess_query(query): 
	fields = "*" 
	if "fields" in query: 
		fields = query["fields"] 

	offset = 0 
	if "offset" in query: 
		offset = int(query["offset"]) 

	limit = 10 
	if "limit" in query: 
		limit = int(query["limit"]) 

	return fields, offset, limit 


def process_pagination(data_result, has_next_page, request_url, offset, limit): 

	request_prefix = request_url.split("&offset")[0] 

	link = [] 
	if not offset == 0: 
		previous = {} 
		previous["previous"] = request_prefix + "&offset=" + str(offset - limit) + "&limit=" + str(limit) 
		link.append(previous) 

	current = {} 
	current["current"] = request_prefix + "&offset=" + str(offset) + "&limit=" + str(limit) 
	link.append(current) 

	if has_next_page: 
		nextL = {} 
		nextL["next"] = request_prefix + "&offset=" + str(offset + limit) + "&limit=" + str(limit) 
		link.append(nextL) 

	result = {} 
	result["link"] = link 
	result["data"] = data_result 

	return result 





@app.route('/api/<resource>', methods=['GET']) 
def get_base_resource(resource): 
	query = request.args 

	fields, offset, limit = preprocess_query(query) 

	data_result, has_next_page = SimpleBO.find_base_resource(resource, query, fields, offset, limit) 

	if data_result: 
		result = process_pagination(data_result, has_next_page, request.url, offset, limit) 
		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
	else: 
		return "NOT FOUND", 400 


@app.route('/api/<resource>/<primary_key>', methods=['GET']) 
def get_spec_resource(resource, primary_key): 
	query = request.args 

	fields, offset, limit = preprocess_query(query) 

	data_result, has_next_page = SimpleBO.find_spec_resource(resource, primary_key, query, fields, offset, limit) 

	if data_result: 
		result = process_pagination(data_result, has_next_page, request.url, offset, limit) 
		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
	else: 
		return "NOT FOUND", 400 




# @app.route('/api/people/<primary_key>?<query_expression>&fields=<fields>', methods=['GET']) 
# @app.route('/api/people/<primary_key>', methods=['GET']) 
# @app.route('/api/people/<primary_key>', defaults={'fields': '*', 'query_expression': '*'}, methods=['GET']) 
# def get_resource_with_query(primary_key): 
# 	query = request.args 
	
# 	fields = "*" 
# 	if "fields" in query: 
# 		fields = query["fields"] 

# 	result = SimpleBO.find_people_by_primary_key(primary_key, query, fields) 

# 	if result: 
# 		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
# 	else: 
# 		return "NOT FOUND", 400 



if __name__ == '__main__':
    app.run()




