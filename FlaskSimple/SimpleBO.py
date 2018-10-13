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


def find_spec_resource(resource, primary_key, query, fields, offset, limit): 
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
    primary_key_pairs[key_pair["s_table"]] = key_pair["s_col_name"] 
  else: 
    # store foreign keys 
    foreign_key_pairs[tuple([key_pair["s_table"], key_pair["s_col_name"]])] = tuple([key_pair["r_table"], key_pair["r_column"]]) 






