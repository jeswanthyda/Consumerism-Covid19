from flask import Flask, render_template, request
import requests

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
    worldData = [
        ['Country', 'Popularity'],
        ['Germany', 200],
        ['United States', 300],
        ['Brazil', 700],
        ['Canada', 500],
        ['France', 600],
        ['RU', 700],
      ]
    return render_template('world.html',worldData=worldData)



if __name__ == "__main__":
    app.run(debug=True)