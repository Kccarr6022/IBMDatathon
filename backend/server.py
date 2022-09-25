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

# Database classes
class SYMPTOMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(100))
    symptom_value = db.Column(db.String(100))

    def __init__(self, id, symptom, value):
        self.id = id
        self.symptom = symptom
        self.symptom_value = value

class CLIENTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    symptoms_table = db.Column(db.Integer)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class CLIENTSYMPTOMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(100))

    def __init__(self, id, symptom):
        self.id = id
        self.symptom = symptom


# Database schemas
class SymptomSchema(ma.Schema):
    class Meta: # symptom number, symptom, symptom value
        fields = ('id', 'symptom', 'symptom_value')

class ClientSchema(ma.Schema):
    class Meta: # client id, name
        fields = ('id', 'name')

class ClientSymptomSchema(ma.Schema):
    class Meta: # client id, symptom
        fields = ('id', 'symptom')


# Init schema
symptom_schema = SymptomSchema()
symptoms_schema = SymptomSchema(many=True)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

client_symptom_schema = ClientSymptomSchema()
client_symptoms_schema = ClientSymptomSchema(many=True)

#importing data into SQL


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/test')
def test():
    # import live stream data
    cur = db.cursor()
    cur.execute("SELECT * FROM dataset")
    data = cur.fetchall()
    return render_template('test.html', data=data)

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)