#!/usr/bin/python3
from flask import Flask, Response
import json
from config import *
import pymysql as MySQLdb 

app = Flask(__name__)

@app.route("/search/<keyword>/")
@app.route("/search/<keyword>/<encoding>")
def search(keyword=None, encoding=None):
	if keyword == None:
		return "Pass a keyword"

	db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_SCHEME)
	cursor = db.cursor()
	cursor.execute("SELECT name, quotation FROM quote WHERE quotation LIKE %s", ("%"+keyword+"%"))
	rows = cursor.fetchall()

	return format(rows, encoding)

@app.route("/quotes/<nick>/")
@app.route("/quotes/<nick>/<encoding>")
def lookupquote(nick=None, encoding=None):
	if nick == None:
		return "Pass a nick"
	db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_SCHEME)
	cursor = db.cursor()

	cursor.execute("SELECT name, quotation FROM quote WHERE name = %s", [nick])
	rows = cursor.fetchall()

	return format(rows, encoding)

def format(rows, encoding):
	mimetype = "text/plain" if encoding == None else "application/json"
	if len(rows) == 0:
		resp = "No quotes found\n" if encoding == None else """{"error": "No quotes found"}"""
		return Response(response=resp, mimetype=mimetype)

	if encoding == None:
		#Return it as plaintext
		results = "\n".join(["<%s> %s" % (x[0], decode(x[1])) for x in rows]) + "\n"
		return Response(response=results, mimetype=mimetype)

	elif encoding == "json":
		#Return it as json
		results = [{"nick": x[0], "quote": decode(x[1])} for x in rows]
		return Response(response=json.dumps(results), mimetype=mimetype)

def decode(data):
	""" Decode a latin-1 string and turn it into utf-8 """
	return data.encode("latin-1").decode("utf-8", errors="replace")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
else:
	application = app
