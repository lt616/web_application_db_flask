# Change data type 
# People 
ALTER TABLE people MODIFY playerID VARCHAR(64) NOT NULL; 
ALTER TABLE people MODIFY birthCountry VARCHAR(64) NULL; 
ALTER TABLE people MODIFY birthState VARCHAR(64) NULL; 
ALTER TABLE people MODIFY birthCity VARCHAR(64) NULL; 
ALTER TABLE people MODIFY deathCountry VARCHAR(64) NULL; 
ALTER TABLE people MODIFY deathState VARCHAR(64) NULL; 
ALTER TABLE people MODIFY deathcity VARCHAR(64) NULL; 
ALTER TABLE people MODIFY nameFirst VARCHAR(64) NULL; 
ALTER TABLE people MODIFY nameLast VARCHAR(64) NULL;
ALTER TABLE people MODIFY nameGiven VARCHAR(64) NULL;
ALTER TABLE people MODIFY birthYear INT NULL; 
ALTER TABLE people MODIFY birthMonth INT NULL; 
ALTER TABLE people MODIFY birthDay INT NULL; 
ALTER TABLE people MODIFY deathYear INT NULL; 
ALTER TABLE people MODIFY deathMonth INT NULL; 
ALTER TABLE people MODIFY deathDay INT NULL; 
ALTER TABLE people MODIFY weight INT NULL; 
ALTER TABLE people MODIFY height INT NULL; 
ALTER TABLE people MODIFY debut VARCHAR(64) NULL; 
ALTER TABLE people MODIFY finalGame VARCHAR(64) NULL; 
ALTER TABLE people MODIFY throws ENUM('L', 'R', 'S') NULL DEFAULT NULL; 
ALTER TABLE people MODIFY bats ENUM('L', 'R', 'S') NULL DEFAULT NULL; 

# Batting 
ALTER TABLE batting MODIFY playerID VARCHAR(64) NOT NULL; 
ALTER TABLE batting MODIFY teamID VARCHAR(64) NOT NULL; 
ALTER TABLE batting MODIFY lgID VARCHAR(64) NULL; 
ALTER TABLE batting MODIFY yearID INT NOT NULL; 
ALTER TABLE batting MODIFY stint INT NOT NULL; 
ALTER TABLE batting MODIFY G INT NULL; 
ALTER TABLE batting MODIFY AB INT NULL; 
ALTER TABLE batting MODIFY R INT NULL; 
ALTER TABLE batting MODIFY H INT NULL; 
ALTER TABLE batting MODIFY 2B INT NULL; 
ALTER TABLE batting MODIFY 3B INT NULL; 
ALTER TABLE batting MODIFY HR INT NULL; 
ALTER TABLE batting MODIFY RBI INT NULL; 
ALTER TABLE batting MODIFY SB INT NULL; 
ALTER TABLE batting MODIFY CS INT NULL; 
ALTER TABLE batting MODIFY BB INT NULL; 
ALTER TABLE batting MODIFY SO INT NULL; 
ALTER TABLE batting MODIFY IBB INT NULL; 
ALTER TABLE batting MODIFY HBP INT NULL; 
ALTER TABLE batting MODIFY SH INT NULL; 
ALTER TABLE batting MODIFY SF INT NULL; 
ALTER TABLE batting MODIFY GIDP INT NULL; 

# Appearance 
ALTER TABLE appearances MODIFY teamID VARCHAR(64) NOT NULL; 
ALTER TABLE appearances MODIFY lgID VARCHAR(64) NOT NULL; 
ALTER TABLE appearances MODIFY playerID VARCHAR(64) NOT NULL; 
ALTER TABLE appearances MODIFY yearID INT NULL; 
ALTER TABLE appearances MODIFY G_all INT NULL; 
ALTER TABLE appearances MODIFY GS INT NULL; 
ALTER TABLE appearances MODIFY G_batting INT NULL; 
ALTER TABLE appearances MODIFY G_defense INT NULL; 
ALTER TABLE appearances MODIFY G_p INT NULL; 
ALTER TABLE appearances MODIFY G_c INT NULL; 
ALTER TABLE appearances MODIFY G_1b INT NULL; 
ALTER TABLE appearances MODIFY G_2b INT NULL; 
ALTER TABLE appearances MODIFY G_3b INT NULL; 
ALTER TABLE appearances MODIFY G_ss INT NULL; 
ALTER TABLE appearances MODIFY G_lf INT NULL; 
ALTER TABLE appearances MODIFY G_cf INT NULL; 
ALTER TABLE appearances MODIFY G_rf INT NULL; 
ALTER TABLE appearances MODIFY G_of INT NULL; 
ALTER TABLE appearances MODIFY G_dh INT NULL; 
ALTER TABLE appearances MODIFY G_ph INT NULL; 
ALTER TABLE appearances MODIFY G_pr INT NULL; 

# Teams 
ALTER TABLE teams MODIFY yearID int NOT NULL; 
ALTER TABLE teams MODIFY teamID VARCHAR(64) NOT NULL; 

# Managers 
ALTER TABLE managers MODIFY playerID VARCHAR(64) NOT NULL; 
ALTER TABLE managers MODIFY yearID INT NOT NULL; 
ALTER TABLE managers MODIFY teamID varchar(64) NOT NULL; 
ALTER TABLE managers MODIFY inseason INT NOT NULL; 

# Fielding 
ALTER TABLE fielding MODIFY playerID VARCHAR(64) NOT NULL; 
ALTER TABLE fielding MODIFY teamID VARCHAR(64) NULL; 
ALTER TABLE fielding MODIFY lgID VARCHAR(64) NULL; 
ALTER TABLE fielding MODIFY POS VARCHAR(64) NULL; 
ALTER TABLE fielding MODIFY yearID int NULL; 
ALTER TABLE fielding MODIFY stint int NULL; 
ALTER TABLE fielding MODIFY G int NULL; 
ALTER TABLE fielding MODIFY GS int NULL; 
ALTER TABLE fielding MODIFY InnOuts int NULL; 
ALTER TABLE fielding MODIFY PO int NULL; 
ALTER TABLE fielding MODIFY A int NULL; 
ALTER TABLE fielding MODIFY E int NULL; 
ALTER TABLE fielding MODIFY DP int NULL; 
ALTER TABLE fielding MODIFY PB int NULL; 
ALTER TABLE fielding MODIFY WP int NULL; 
ALTER TABLE fielding MODIFY SB int NULL; 
ALTER TABLE fielding MODIFY CS int NULL; 
ALTER TABLE fielding MODIFY ZR int NULL; 



# clean up null values 
# People 
UPDATE people SET birthCountry=NULL WHERE birthCountry="";  
UPDATE people SET birthState=NULL WHERE birthState="";  
UPDATE people SET birthCity=NULL WHERE birthCity=""; 
UPDATE people SET deathCountry=NULL WHERE deathCountry="";  
UPDATE people SET deathState=NULL WHERE deathState="";  
UPDATE people SET deathcity=NULL WHERE deathcity="";  
UPDATE people SET nameFirst=NULL WHERE nameFirst="";  
UPDATE people SET nameLast=NULL WHERE nameLast="";  
UPDATE people SET nameGiven=NULL WHERE nameGiven="";  
UPDATE people SET bats=NULL WHERE bats="";  
UPDATE people SET throws=NULL WHERE throws="";  

# Batting
UPDATE batting SET lgID=NULL WHERE lgID="";  

# Appearance 
UPDATE appearances SET lgID=NULL WHERE lgID="";  

# Fielding 
UPDATE fielding SET playerID=NULL WHERE playerID=""; 
UPDATE fielding SET teamID=NULL WHERE teamID=""; 
UPDATE fielding SET lgID=NULL WHERE lgID=""; 
UPDATE fielding SET POS=NULL WHERE POS=""; 


# Add constraints - Primary keys 
# People 
ALTER TABLE people ADD PRIMARY KEY (playerID); 

# Batting
ALTER TABLE batting ADD PRIMARY KEY (playerID, teamID, yearID, stint); 

# Appearance 
ALTER TABLE appearances ADD PRIMARY KEY (playerID, teamID, yearID); 

# Teams 
ALTER TABLE teams ADD PRIMARY KEY (yearID, teamId); 

# Managers
ALTER TABLE managers ADD PRIMARY KEY (playerID, teamID, yearID, inseason); 



# Add constraints - Foreign keys 
ALTER TABLE appearances ADD CONSTRAINT apptopeople FOREIGN KEY (playerID) REFERENCES people(playerID); 
ALTER TABLE batting ADD CONSTRAINT battingtopeople FOREIGN KEY (playerID) REFERENCES people(playerID); 
ALTER TABLE fielding ADD CONSTRAINT fieldtopeople FOREIGN KEY (playerID) REFERENCES people(playerID); 
ALTER TABLE managers ADD CONSTRAINT managertopeople FOREIGN KEY (playerID) REFERENCES people(playerID); 





















