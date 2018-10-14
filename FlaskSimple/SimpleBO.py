import pymysql
import json 
import sys 

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='COMS4111_assignment02',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor) 

# key -> value: table -> primary key 
primary_key_pairs = {}  

# key -> value: tuple(table, foreign key) -> referenced key 
foreign_key_pairs = {} 


def run_q(q, fetch=False):
    cursor = cnx.cursor() 
    cursor.execute(q) 
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result 

def run_q_without_res(q): 
    cursor = cnx.cursor() 
    try:
      affected_num = cursor.execute(q) 
      if affected_num == 0: 

    except: 


# def run_q(q, args, fetch=False):
#     cursor = cnx.cursor()
#     cursor.execute(q, args)
#     if fetch:
#         result = cursor.fetchall()
#     else:
#         result = None
#     cnx.commit()
#     return result


def process_result(result, limit): 
  res_len = len(result) 

  if res_len > (limit - 1): 
    return result[:-1], True 
  else: 
    return result, False  


def find_related_materials(resource, related_resource): 
    for foreign_key in foreign_key_pairs: 
      if foreign_key[0] == resource and foreign_key_pairs[foreign_key][0] == related_resource: 
        return foreign_key[1], foreign_key_pairs[foreign_key][1] 

      if foreign_key_pairs[foreign_key][0] == resource and foreign_key[0] == related_resource: 
        return foreign_key_pairs[foreign_key][1], foreign_key[1] 


def find_base_resource(resource, query, fields, offset, limit): 
    query_str = "" 

    for key, value in query.items(): 
      if not key == "fields" and not key == "offset" and not key == "limit": 
        query_str = " AND " + str(key) + " = '" + str(value) + "'" 

    if not query_str == "": 
        query_str = query_str[5:] 
        query_str = " WHERE " + query_str 

    limit += 1 
    q = "SELECT " + str(fields) + " FROM " + str(resource) + query_str + " LIMIT " + str(limit) + " OFFSET " + str(offset) 
    result = run_q(q, True) 

    return process_result(result, limit)


def find_spec_resource(resource, primary_key, fields): 
    query_str = "" 

    # construct primary keys 
    primary_key_columns = primary_key_pairs[resource] 
    primary_keys = primary_key.split("_") 
    print(primary_key_columns) 

    if len(primary_key_columns) == 0 or not len(primary_key_columns) == len(primary_keys): 
      return [], True 

    query_str = "" 
    for i in range(0, len(primary_key_columns)): 
      query_str += " AND " + str(primary_key_columns[i]) + " = '" + str(primary_keys[i]) + "'" 

    if not query_str == "": 
        query_str = query_str[5:] 
        query_str = " WHERE " + query_str   

    q = "SELECT " + str(fields) + " FROM " + str(resource) + query_str 
    print(q) 
    result = run_q(q, True) 

    if not result: 
      return None 
    else: 
      return result[0]  


def find_related_resource(resource, primary_key, related_resource, query, fields, offset, limit): 
    primary_resource = find_spec_resource(resource, primary_key, "*") 
    if not primary_resource: 
      return [] 

    resource_key, related_resource_key = find_related_materials(resource, related_resource) 

    query_str = " INNER JOIN " + str(resource) + " ON " + resource + "." + resource_key + " = " + related_resource + "." + related_resource_key 

    condition_str = " WHERE " + str(resource) + "." + resource_key + " = '" + primary_resource[resource_key] + "'" 

    limit += 1 
    q = "SELECT " + str(fields) + " FROM " + str(related_resource) + query_str + condition_str + " LIMIT " + str(limit) + " OFFSET " + str(offset) 

    result = run_q(q, True) 

    return process_result(result, limit) 


# def find_people_by_primary_key(primary_key, query, fields): 

#     query_str = "" 

#     for key, value in query.items(): 
#         if not key == "fields":  
#             query_str += " AND " + str(key) + " = '" + str(value) + "'" 

#     # if not query_str == "": 
#         # query_str = " WHERE" + query_str 


#     q = "SELECT " + str(fields) + " FROM people WHERE playerid = %s" + query_str 
#     print(q) 
#     result = run_q(q, True)
#     return result 

query = "select constraint_schema as s_schema, constraint_name as c_name, table_name as s_table, column_name as s_col_name, ordinal_position as o_position, position_in_unique_constraint as u_position, referenced_table_schema as r_schema, referenced_table_name as r_table, referenced_column_name as r_column from information_schema.KEY_COLUMN_USAGE WHERE CONSTRAINT_SCHEMA = 'COMS4111_assignment02'"
keys = run_q(query, True) 

for key_pair in keys: 
  if key_pair["c_name"] == "PRIMARY": 
    # store primary keys 
    if not key_pair["s_table"] in primary_key_pairs: 
      primary_key_pairs[key_pair["s_table"]] = [] 
    primary_key_pairs[key_pair["s_table"]].append(key_pair["s_col_name"]) 
  else: 
    # store foreign keys 
    foreign_key_pairs[tuple([key_pair["s_table"], key_pair["s_col_name"]])] = tuple([key_pair["r_table"], key_pair["r_column"]]) 






