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
	print(request_url) 
	request_prefix = request_url.split("offset")[0] 
	print(request_prefix) 
	if not "?" in request_prefix: 
   		request_prefix += "?" 
	else: 
		if not request_prefix.endswith('&'): 
			request_prefix += "&"

	link = [] 
	if not offset == 0: 
		previous = {} 
		previous["previous"] = request_prefix + "offset=" + str(offset - limit) + "&limit=" + str(limit) 
		link.append(previous) 

	current = {} 
	current["current"] = request_prefix + "offset=" + str(offset) + "&limit=" + str(limit) 
	link.append(current) 

	if has_next_page: 
		nextL = {} 
		nextL["next"] = request_prefix + "offset=" + str(offset + limit) + "&limit=" + str(limit) 
		link.append(nextL) 

	result = {} 
	result["link"] = link 
	result["data"] = data_result 

	return result 





@app.route('/api/<resource>', methods=['GET']) 
def get_base_resource(resource): 
	query = request.args 
	print(resource) 

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

	result = SimpleBO.find_spec_resource(resource, primary_key, fields) 

	if result: 
		# result = process_pagination(data_result, has_next_page, request.url, offset, limit) 
		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
	else: 
		return "Error: NOT FOUND", 400 


@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['GET']) 
def get_related_resource(resource, primary_key, related_resource): 
	query = request.args 

	fields, offset, limit = preprocess_query(query) 
	print("match") 
	data_result, has_next_page = SimpleBO.find_related_resource(resource, primary_key, related_resource, query, fields, offset, limit) 

	if data_result: 
		result = process_pagination(data_result, has_next_page, request.url, offset, limit) 
		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
	else: 
		return "Error: NOT FOUND", 400 


@app.route('/api/<resource>', methods=['POST']) 
def post_base_resource(resource): 
	data = request.form 

	result, err = SimpleBO.save_base_resource(resource, data) 
	if result: 
		return "Update Successfully", 200 
	else: 
		return "Error: " + err, 400 


@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['POST']) 
def post_related_resource(resource, primary_key, related_resource): 
	data = request.form  

	result, err = SimpleBO.save_related_resource(resource, primary_key, related_resource, data) 
	if result: 
		return "Insert Successfully", 201 
	else: 
		return "Error: " + err, 400 


@app.route('/api/<resource>/<primary_key>', methods=['PUT']) 
def put_spec_resource(resource, primary_key): 
	data = request.form 
	print(data) 

	result, err = SimpleBO.update_spec_resource(resource, primary_key, data) 
	if result: 
		return "Update Successfully", 200 
	else: 
		return "Error: " + err, 400 


@app.route('/api/<resource>/<primary_key>', methods=['DELETE']) 
def delete_spec_resource(resource, primary_key): 

	result, err = SimpleBO.del_spec_resource(resource, primary_key) 
	if result: 
		return "Delete Successfully", 200 
	else: 
		return "Error: " + err, 400 


# Custom queries 
@app.route('/api/teammates/<player_id>', methods=['GET']) 
def custom_teammates(player_id): 
	query = request.args 

	fields, offset, limit = preprocess_query(query) 

	data_result, has_next_page = SimpleBO.get_teammates(player_id, offset, limit) 

	if data_result: 
		result = process_pagination(data_result, has_next_page, request.url, offset, limit) 
		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
	else: 
		return "NOT FOUND", 400 


@app.route('/api/roster', methods=['GET']) 
def custom_roster(): 
	query = request.args 

	fields, offset, limit = preprocess_query(query) 

	data_result, has_next_page = SimpleBO.get_roster(query["teamid"], query["yearid"], offset, limit) 

	if data_result: 
		result = process_pagination(data_result, has_next_page, request.url, offset, limit) 
		return json.dumps(result), 200, {'Content-Type': 'application/json; charset=utr-8'} 
	else: 
		return "NOT FOUND", 400 


@app.route('/api/people/<primary_key>/career_stats', methods=['GET']) 
def custom_career_stats(primary_key): 
	query = request.args 

	fields, offset, limit = preprocess_query(query) 

	data_result, has_next_page = SimpleBO.get_career_stats(primary_key, offset, limit) 

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




