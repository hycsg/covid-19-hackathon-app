from flask import Flask, render_template, session

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/result/', methods=["POST"])
def result():
    data = {"name": request.form.get("city")}
     

