from flask import Flask, render_template, session

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/result/', methods=["POST"])
def result():
    input_data = {"state": request.form.get("state"), "county": request.form.get("county")}
      

