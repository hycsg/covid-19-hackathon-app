from flask import Flask, render_template, session
from csvquery import *
import datetime

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/result/', methods=["POST"])
def result():
    input_data = {"state": request.form.get("state"), "county": request.form.get("county")}
    data_set = get_csv(f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date.strftime('%m-%d-%Y')}.csv")
    query_result = data_set.already_indexed("Admin2", Comparisons.strings).query_one({
        "Admin2": data_set["county"],
        "Province_State": data_set["state"]
    })
    return render_template("result.html", query_result.to_dictionary())
      

