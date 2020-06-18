import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Analyzer():

    def __init__(self,filepath):
        self.df = pd.read_csv(filepath, header=None,names=['Title','Description','Date'])
        self.analyzer = SentimentIntensityAnalyzer()
    
    def datewiseBlob(self):
        groupedDF = self.df.applymap(str).groupby(['Date'],as_index=False).agg({'Title' : ' '.join, 'Description' : ' '.join})
        groupedDF['Corpus'] = groupedDF['Title'] + groupedDF['Description']
        self.groupedDF = groupedDF
    
    def calculateSentiment(self):
        self.datewiseBlob()
        sentimentDF = self.groupedDF
        sentimentDF['Title'] = sentimentDF['Title'].apply(lambda x: self.analyzer.polarity_scores(x)['compound'])
        sentimentDF['Description'] = sentimentDF['Description'].apply(lambda x: self.analyzer.polarity_scores(x)['compound'])
        sentimentDF['Corpus'] = sentimentDF['Corpus'].apply(lambda x: self.analyzer.polarity_scores(x)['compound'])
        return sentimentDF
        
if __name__ == '__main__':

    datapath = './../data/news/'
    for filename in os.listdir(datapath):
        filepath = datapath+filename
        analyzer = Analyzer(filepath)
        sentimentDF = analyzer.calculateSentiment()
        sentimentDF.to_csv('./../data/news/sentiment/{}'.format(filename), index = False, header=True)
        print('Sentiment Values Saved for: ', filename)
