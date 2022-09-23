from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import threading
import time
import os


# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))  # base directory
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# db class
class POST(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100))
    close = db.Column(db.Float)

    def __init__(self, id, time, close):
        self.id = id
        self.time = time
        self.close = close


# Schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('close', 'time')


# Init schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


#background
def collect_closes():
    """Threaded function
    """

    while True:
        pass

@app.route('/post', methods=['POST'])
def myfun():
    return "Hi there" 

@app.route('/hello', methods=['GET'])
def yello():
    return "lol"

@app.route('/', methods=['GET'])
def mainroute():
    candle = db.session.query(POST).order_by(POST.id.desc()).first() # sample query 
    return post_schema.jsonify(candle)


@app.route('/route1', methods=['GET'])
def fourhourclose():
    data = db.session.query(POST).all() # sample query
    return posts_schema.jsonify(data)


def main():
    threading.Thread(target=collect_closes).start() # background task
    threading.Thread(target=app.run(host='0.0.0.0', port=8080,
                     debug=True, threaded=True)).start()


# run api endpoint
if __name__ == '__main__':
    main()