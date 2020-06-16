from flask import Flask, render_template, request
import requests
from pymongo import MongoClient
import pycountry

app = Flask(__name__)

@app.route("/")
def coverPage():
    return render_template('cover.html')

@app.route("/insights")
def insights():
    return render_template('insights.html')


@app.route("/consumerism")
def consumerism():
    return render_template('consumerism.html')

@app.route("/approach")
def approach():
    return render_template('approach.html')


@app.route("/team")
def team():
    return render_template('team.html')

@app.route("/world")
def world():
    db = MongoClient("mongodb+srv://dbuser:TCS-Consumerism@cluster0-tchxh.mongodb.net/<dbname>?retryWrites=true&w=majority").ConsumerismInsights
    world_count = db.twitter.find_one({})
    worldData = []
    for key,value in world_count.items():
        if len(key) == 2: #Only Country code is of length 2 in database
            try:
                worldData.append([pycountry.countries.get(alpha_2=key).name,value])
            except:
                worldData.append([key,value])
    worldData = sorted(worldData,key=lambda x: x[1],reverse=True)
    return render_template('world.html',worldData=[['Country', 'Engagement']]+worldData)



if __name__ == "__main__":
    app.run(debug=True)