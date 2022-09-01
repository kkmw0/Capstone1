from flask import Flask
from db_connect import db

def create_app():
    app = flask.Flask(__name__)
    db.init_app(app)

@app.route('/getfact', methods=['GET'])
def get_fact():
    return "Server"

@app.route('/getname/<name>', methods=['POST'])
def extract_name(name):
    print("Data received from a client : " + name)
    return name;

if  __name__ == '__main__':
    create_app().run(host = 'Your IP', port = 12345, debug = True)
