#!/usr/bin/env python 

import os, time, psycopg2, hashlib
from os.path import join, getsize
import config

conn = psycopg2.connect("dbname=%(dbname)s user=%(username)s password=%(password)s" \
	% config.database)
cur = conn.cursor()

# top level directory to search (have to escape backslashes, f-u Windows)
# WAS: root = 'C:\\jamesbatch\\sdrive\\ConsoleLogBackup'
root = config.directoryToAnalyze
print "Performing analysis on ", root

for fullpath, dirs, files in os.walk(root):
	for name in files:
		
		filepath = join(fullpath, name)
	
		# get the file extension
		# use os.path.splitext() to split the filename on the last period
		# returns an array of two items; take the second by doing [1]
		# returned string will have the period on the front; strip it with [1:]
		# make it all lowercase
		ext = os.path.splitext(name)[1][1:].lower()
		
		size = getsize( filepath ) # size of this file
		
		# path to files with top level removed
		# this will make it easier to translate between S-drive files being
		# analyzed on a computer other than JSC-MOD-FS3
		relativepath = fullpath[len(root):]
		
		stats = os.stat( filepath )
		
		sha1 = hashlib.sha1()
		sha1.update( file( filepath , 'rb').read() )
		sha1 = sha1.hexdigest()		
		
		created = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stats.st_ctime))
		modified = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stats.st_mtime))
		accessed = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stats.st_atime))
		
		query = """
			INSERT INTO files 
			(filename,extension,bytes,root,relativepath,sha1,created,modified,accessed) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
			"""
		
		cur.execute(query, 
			(name,ext,size,root,relativepath,sha1,created,modified,accessed))
	
	print "Complete with directory", fullpath
			
# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()		

print "complete"