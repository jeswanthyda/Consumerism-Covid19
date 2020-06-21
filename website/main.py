from flask import Flask, render_template, request
import requests
from pymongo import MongoClient
import pycountry
from collections import defaultdict
 




app = Flask(__name__)

class MDB():

    def __init__(self):
        self.db = MongoClient("mongodb+srv://dbuser:TCS-Consumerism@cluster0-tchxh.mongodb.net/<dbname>?retryWrites=true&w=majority").ConsumerismInsights
        self.plots = self.db.plots
        self.news = self.db.news   

    def getGroupedBarData(self,documentIDs):
        params = []
        for docID in documentIDs:
            colours = ['rgba(255,166,0,0.2)','rgba(188,80,144,0.2)']
            borderColours = ['rgb(255,166,0,0.2)','rgb(188,80,144,0.2)']
            data = self.plots.find_one({'documentID':docID},{'_id': False})
            datasets = [
                {
                    'label': "A",
                    'data': data['A'],
                    'backgroundColor': colours[0],
                    'borderColor': borderColours[0],
                    'borderWidth': 2,
                },
                {
                    'label': "B",
                    'data': data['B'],
                    'backgroundColor': colours[1],
                    'borderColor': borderColours[1],
                    'borderWidth': 2,
                },
                
            ]
            params.append({
                'documentID':docID,
                'datasets':datasets,
                'labels':data['labels'],
                'text': data['text'],
                'title': data['title']
            })
        return params

    # def getIndustryBarData(self,documentIDs):
    #     params = []
    #     for docID in documentIDs:
    #         data = self.plots.find_one({'documentID':docID},{'_id': False})
    #         datasets = [
    #             {
    #                 'data': data['scores'],
    #                 'backgroundColor': 'orange'
    #             },
    #         ]
    #         params.append({
    #             'documentID':docID,
    #             'datasets':datasets,
    #             'labels':data['labels']
    #         })
    #     return params

    def getNewsSentiment(self):
        datasets = []
        # colours = ['rgb(255,255,0)','rgb(0,234,255)','rgb(170,0,255)',
        #             'rgb(255,127,0)', 'rgb(191,255,0)', 'rgb(237,185,185)', 'rgb(185,215,237)',
        #             'rgb(231,233,185)', 'rgb(220,185,237)', 'rgb(35,98,143)', 'rgb(143,106,35)'
        #             ]
        industries = self.news.find({})
        for industry in industries:
            data = {
                'label':industry['documentID'],
                'fill': False,
                'lineTension': 0.1,
                'borderColor':'rgb(255,127,0)',
                'data': list(industry['Title'])  #TODO: TRY TITLE and DESCRIPTION
                }
            datasets.append(data)
        plot_params = {'documentID':'newsSentiment','labels':list(industry['Date']), 'datasets':datasets}
        return plot_params


database = MDB()

@app.route("/")
def coverPage():
    return render_template('cover.html')

@app.route("/acknowledgement")
def acknowledgement():
    return render_template('acknowledgement.html')

@app.route("/insights")
def insights():
    documentIDsBig = ['persoanl_interpretation']
    paramsBig = database.getGroupedBarData(documentIDs=documentIDsBig)

    documentIDsSmall = ['consumerism','gender','country','education','profession','residence','family_size','household_income_pa']
    paramsSmall = database.getGroupedBarData(documentIDs=documentIDsSmall)
    
    documentIDsStaticSmall = ['growth_anticon','remote_everything']
    paramsStaticSmall = database.getGroupedBarData(documentIDs=documentIDsStaticSmall)

    paramsNews = database.getNewsSentiment()

    documentIDsScores = ['industry_scores','postcov_scores','postcov_scores_2']
    paramsScores = database.getGroupedBarData(documentIDs=documentIDsScores)

    return render_template('insights.html',paramsStaticSmall=paramsStaticSmall,paramsSmall=paramsSmall,paramsBig=paramsBig[0],paramsNews=paramsNews,paramsScores=paramsScores)


@app.route("/Introduction")
def consumerism():
    return render_template('Introduction.html')

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

