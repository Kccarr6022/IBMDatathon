from flask import Flask, render_template
import tensorflow

app = Flask(__name__)



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