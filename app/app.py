from flask import Flask, render_template, session, request
from csvquery import get_csv, open_csv, Comparisons
from datetime import date, timedelta

app = Flask(__name__)
title = "COVID in my County"
static_dir = "static/"

# loading data
# county_population = open_csv(f"{static_dir}population.csv")
# county_population.already_indexed("full", Comparisons.strings)

yesterday = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
data = get_csv(f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{yesterday}.csv")
data = data.select_as({"Admin2":"county", "Province_State":"state", "Confirmed":"confirmed cases", "Deaths":"deaths", "Recovered":"recovered", "Last_Update":"last update"})
data.already_indexed("county", Comparisons.strings)
data.replace(data.fields, lambda s: s.lower())
data.add_field("full", lambda row: f"{row['county']}, {row['state']}")
data.index("full", Comparisons.strings)

counties_states = data.select(["county", "state"]).query({"state":{"neq":""},"county":{"neq":""}})
counties_states.add_field("full", lambda row: f"{row['county']}, {row['state']}")
states = counties_states.select_unique("state").to_list()

# responses
@app.route('/')
def main():
    return render_template('index.html', title=title)

@app.route('/result', methods=["POST"])
def result():
    input_data = {"state": request.form.get("state").lower(), "county": request.form.get("county").lower()}
    info_dict = data.query_one(input_data).select(["confirmed cases", "recovered", "deaths", "last update", "full"]).to_dictionary()
    location = "Invalid Request"
    last_update = ""
    if info_dict != {}:
        location = ", ".join([" ".join([word.capitalize() for word in section.split(" ")]) for section in info_dict.pop("full").split(", ")])
        last_update = info_dict.pop("last update")
    return render_template("result.html", location=location, last_update=last_update, result=info_dict, title=title)

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
    
    selected_state = counties_states.query({"state":state}).index("county", Comparisons.strings)
    counties = selected_state.select_unique("county").to_list()
    
    results = []
    for county in counties:
        if partial_county == county[0:len(partial_county)]:
            results.append(county)
            if len(results) == 5:
                break
    return ";".join(results)