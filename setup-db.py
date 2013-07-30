#!/usr/bin/env python 

import os
from os.path import join, getsize
import psycopg2
import config

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Prior to running this script setup your database  #
#                                                   #
# See config.py for more information                #
# # # # # # # # # # # # # # # # # # # # # # # # # # #


# Open connection to new database 
conn = psycopg2.connect("dbname=%(dbname)s user=%(username)s password=%(password)s" \
	% config.database)
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("""
	CREATE TABLE IF NOT EXISTS files (
	id serial PRIMARY KEY,
	filename varchar(255),
	extension varchar(255),
	bytes bigint,
	root text,
	relativepath text,
	sha1 varchar(40),
	created varchar(19),
	modified varchar(19),
	accessed varchar(19)
	);
""")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

print "Database setup complete"