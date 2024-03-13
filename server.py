# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import sys


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()

    canada = data["Canada"]
    mexico = data["Mexico"]
    us = data["US"]

   
    total = sum(list(canada.values())) + sum(list(mexico.values())) + sum(list(us.values()))
    length = len(canada) + len(mexico) + len(us)

    years = sorted(list(data[list(data.keys())[0]].keys()))
    line_endpoints = {}

    for key in data:
        line_endpoints[key] = []
        for i in range(len(years) - 1):
            start_x = years[i]
            stop_x = years[i+1]
            line_endpoints[key].append([data[key][start_x],data[key][stop_x]])
    
    return render_template('index.html', avg = total / length, years = years, endpoints = line_endpoints)

@app.route('/year')
def year():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()

    year= request.args.get("year")

    requestedData = {}

    for key in data:
        requestedData[key] = [round(data[key][year], 2)]
    colors = {}
    for i in range(1,11):
        colors[55.017 + i *(82.04878049 - 55.017)/10] = 100 - 10 * i

    
    for value in requestedData:
        for color in colors:
            if requestedData[value][0] < color:
                requestedData[value].append(colors[color])
                break

    return render_template('year.html', year = year, requestedData = requestedData)

app.run(debug=True)
