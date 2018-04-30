from flask import Flask, render_template, json, jsonify, request
import flask
from database import Database
import os

app = Flask(__name__)
db = Database()

db.create_table()


@app.route('/api/movies', methods=['GET', 'POST'])
def get_movies():
	try:
		if flask.request.method == 'POST':
			db.insert_movie(request.json['name'], request.json['cover'])
			return jsonify(data=request.json), 201
		else:
			movies = db.fetch_movies()
			return jsonify(data=movies), 200
	except Exception as e:
		return jsonify(status='ERROR', message=str(e)), 500

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/shutdown', methods=['GET'])
def shutdown():
    stop_server()
    return 'Server shutting down...'

def start_server():
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def stop_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == "__main__":
	start_server()
