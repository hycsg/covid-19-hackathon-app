from flask import Flask, render_template, session, request
from csvquery import *
from datetime import date, timedelta

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result():
    input_data = {"state": request.form.get("state"), "county": request.form.get("county")}
    yesterday = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
    data_set = get_csv(f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{yesterday}.csv")
    query_result = data_set.already_indexed("Admin2", Comparisons.strings).query_one({
        "Admin2": input_data["county"],
        "Province_State": input_data["state"]
    })
    return render_template("result.html", result=query_result.to_dictionary())
      

