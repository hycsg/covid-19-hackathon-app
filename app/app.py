from flask import Flask, render_template, session, request
from csvquery import get_csv, open_csv, Comparisons
from datetime import date, timedelta

app = Flask(__name__)

# loading data
yesterday = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
data = get_csv(f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{yesterday}.csv")
data = data.select_as({"Admin2":"county", "Province_State":"state", "Confirmed":"confirmed", "Deaths":"deaths", "Recovered":"recovered", "Last_Update":"last update"})
data.already_indexed("county", Comparisons.strings)
data.replace(data.fields, lambda s: s.lower())

counties_states = data.select(["county", "state"]).query({"state":{"neq":""},"county":{"neq":""}})
counties_states.add_field("full", lambda row: f"{row['county']}, {row['state']}")
states = counties_states.select_unique("state").to_list()

# responses
@app.route('/')
def main():
    return render_template('index.html', title="COVID in my County")

@app.route('/result', methods=["POST"])
def result():
    input_data = {"state": request.form.get("state").toLowerCase(), "county": request.form.get("county").toLowerCase()}
    query_result = data.query_one(input_data)
    return render_template("result.html", result=query_result.to_dictionary())

@app.route('/get_state')
def get_state():
    partial_state = request.args.get("s")
    if partial_state == "":
        return ""
    results = []
    for state in states:
        if partial_state == state[0:len(partial_state)]:
            results.append(state)
    return ";".join(results)

@app.route('/get_county')
def get_county():
    state = request.args.get("s")
    partial_county = request.args.get("c")
    if partial_county == "":
        return ""
    
    selected_state = counties_states.query({"state":state})
    counties = selected_state.select_unique("county").to_list()
    results = []
    for county in counties:
        if partial_county == county[0:len(partial_county)]:
            some_results = selected_state.query({"county":county}).select("full").to_list()
            for r in some_results:
                results.append(r)
                if len(results) == 3:
                    break
        if len(results) == 3:
            break
    return ";".join(results)