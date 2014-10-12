#!/usr/bin/python
from flask import Flask, Response
import MySQLdb
import json

app = Flask(__name__)

@app.route("/quotes/<nick>/")
@app.route("/quotes/<nick>/<encoding>")
def lookupquote(nick=None, encoding=None):
	mimetype = "text/plain" if encoding == None else "application/json"
	if nick == None:
		resp = "Pass a nick" if encoding == None else """{"error": "No nick provided"}"""
		return Response(response=resp, mimetype=mimetype)
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="bhottu")
	cursor = db.cursor()

	cursor.execute("SELECT quotation FROM quote WHERE name = %s", [nick])
	rows = cursor.fetchall()
	if len(rows) == 0:
		resp = "No quotes found" if encoding == None else """{"error": "No quotes found for this nick"}"""
		return Response(response=resp, mimetype=mimetype)
	if encoding == None:
		results = ""
		for row in rows:
			results += "<%s> %s\n" % (nick, row[0])
		resp = Response(response=results, mimetype=mimetype)
		return resp
	elif encoding == "json":
		results = {"nick": nick, "quotes": []}
		for row in rows:
			results["quotes"].append(row[0])
		return Response(response=json.dumps(results), mimetype=mimetype)

if __name__ == "__main__":
	app.run(debug=True)
