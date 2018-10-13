# web_application_db_flask
An interactive, web application using a relational database based on MySQL and Flask. 
The inferface and front-end was built by prof. Donald Ferguson. 

# Overview 
There are two parts to the application:

* Modify a database schema to improve data integrity when users enter new data or update existing data.
* Implement common REST API calls supporting user stories by defining simple application code and database queries that support the user stories. 

# Back-end API
The endpoint will support the following paths and HTTP operations
* ```/<resource>```

            POST (INSERT) 
            
            GET with query parameters and fields
       
* ```/<resource>/<primary_key>```

            GET with fields selection

            DELETE
       
* ```/<resource1>/<primary_key>/<resource1>```

            GET with fields
            
            POST (INSERT)
            
* ```/roster``` Gets info about a team and year.

            GET with query parameters teamID, yearID
            
            Returns [{playerID, nameLast, nameFirst, G_all, H, AB}]
            
* ```/career_stats``` Gets career totals for selected players.

            GET with query parameters to choose player based on fields in People.
            
            Returns [{playerID, nameLast, nameFirst, total_h, total_ab, career_avg, total_g}]
            
* ```/career_stats/<playerID>```

            Same as above.
       
            For a specific playerID




