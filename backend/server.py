from flask import Flask, render_template
import tensorflow
from model import infer


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inference', method=['POST'])
def model_inference():
    res = infer(request.form.get("symptoms")) # request looks like { "symptoms":[] }
    return res

@app.route('/live')
def live_parse():
    # import live stream data
    return render_template('live_parse.html')

@app.route('/archieves')
def archieves():
    return render_template('archieves.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)