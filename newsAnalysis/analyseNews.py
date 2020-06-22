import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient

class Analyzer():

    def __init__(self,filepath):
        self.df = pd.read_csv(filepath, header=None,names=['Title','Description','Date'],engine='python')
        self.analyzer = SentimentIntensityAnalyzer()
    
    def datewiseBlobDF(self):
        groupedDF = self.df.applymap(str).groupby(['Date'],as_index=False).agg({'Title' : ' '.join, 'Description' : ' '.join})
        groupedDF['Corpus'] = groupedDF['Title'] + groupedDF['Description']
        return groupedDF
    
    def calculateSentiment(self,groupedDF):
        sentimentDF = pd.DataFrame()
        sentimentDF['Date'] = groupedDF['Date']
        sentimentDF['Title'] = groupedDF['Title'].apply(lambda x: self.analyzer.polarity_scores(x)['compound'])
        sentimentDF['Description'] = groupedDF['Description'].apply(lambda x: self.analyzer.polarity_scores(x)['compound'])
        sentimentDF['Corpus'] = groupedDF['Corpus'].apply(lambda x: self.analyzer.polarity_scores(x)['compound'])
        return sentimentDF
        
if __name__ == '__main__':

    datapath = './../data/news/'
    # datapath = 'G:/TCS/Consumerism-Covid19/data/news/'
    db = MongoClient("mongodb+srv://dbuser:TCS-Consumerism@cluster0-tchxh.mongodb.net/<dbname>?retryWrites=true&w=majority").ConsumerismInsights
    news = db.news
    news.delete_many({})

    for filename in os.listdir(datapath):
        filepath = datapath+filename
        analyzer = Analyzer(filepath)
        groupedDF = analyzer.datewiseBlobDF()
        sentimentDF = analyzer.calculateSentiment(groupedDF)

        ##Push sentiment values to MongoDB
        data = {'documentID' : filename.split('.')[0]}
        for (columnName, columnData) in sentimentDF.iteritems():
            data[columnName] = list(columnData)
        news.insert_one(data)
    


