#!/usr/bin/python
from flask import Flask, Response
import json
from config import *
try:
	import MySQLdb
except ImportError:
	import pymysql as MySQLdb

app = Flask(__name__)

@app.route("/quotes/<nick>/")
@app.route("/quotes/<nick>/<encoding>")
def lookupquote(nick=None, encoding=None):
	mimetype = "text/plain" if encoding == None else "application/json"
	if nick == None:
		resp = "Pass a nick" if encoding == None else """{"error": "No nick provided"}"""
		return Response(response=resp, mimetype=mimetype)
	db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_SCHEME)
	cursor = db.cursor()

	cursor.execute("SELECT quotation FROM quote WHERE name = %s", [nick])
	rows = cursor.fetchall()
	if len(rows) == 0:
		resp = "No quotes found" if encoding == None else """{"error": "No quotes found for this nick"}"""
		return Response(response=resp, mimetype=mimetype)

	decode = decode_py2 if check_py_version() == 2 else decode_py3

	if encoding == None:
		results = ""
		for row in rows:
			results += "<%s> %s\n" % (nick, decode(row[0]))

		resp = Response(response=results, mimetype=mimetype)
		return resp
	elif encoding == "json":
		results = {"nick": nick, "quotes": []}
		for row in rows:
			results["quotes"].append(decode(row[0]))
		return Response(response=json.dumps(results), mimetype=mimetype)

def check_py_version():
	""" Returns the major python version currently used """
	import sys
	return sys.version_info[0]

def decode_py3(data):
	""" Decode a latin-1 string and turn it into utf-8, the Python 3 way """
	return bytes(data, 'latin-1').decode('utf-8')

def decode_py2(data):
	""" Decode a latin-1 string and turn it into utf-8, the Python 3 way """
	return data.decode('utf-8')

if __name__ == "__main__":
	app.run(debug=True)
else:
	application = app
