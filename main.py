from flask import Flask, render_template

app = Flask(__name__)

@app.route('/s3', methods=['GET'])
def manipulate_s3():
    return render_template('s3.html')

@app.route('/', methods=['GET', 'POST'])
def route_homepage():
    return render_template('index.html', title="AWS Frontend")

app.run(debug=True)