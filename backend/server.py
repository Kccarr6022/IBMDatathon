from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import tensorflow

# init app
basedir = os.path.abspath(os.path.dirname(__file__))  # base directory
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db and ma
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database class
class POST(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100))
    close = db.Column(db.Float)

    def __init__(self, id, time, close):
        self.id = id
        self.time = time
        self.close = close


# Database schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('close', 'time')


# Init schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    # import live stream data
    return render_template('test.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)