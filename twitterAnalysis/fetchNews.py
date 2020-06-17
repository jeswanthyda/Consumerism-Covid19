import requests
import pandas as pd
from collections import defaultdict
import datetime

class News():

    def __init__(self,sectors,key):
        self.key = key
        self.sectors = sectors
        

    def generateURL(self,keyword,fromDate=None,toDate=None):
        if fromDate and toDate:
            url = 'https://newsapi.org/v2/everything?q=(covid OR corona) AND {} AND sector&apiKey={}&language=en&sortBy=publishedAt&pageSize=100&from={}&to={}'.format(keyword,self.key,fromDate,toDate)
        elif fromDate:
            url = 'https://newsapi.org/v2/everything?q=(covid OR corona) AND {} AND sector&apiKey={}&language=en&sortBy=publishedAt&pageSize=100&from={}'.format(keyword,self.key,fromDate)
        elif toDate:
            url = 'https://newsapi.org/v2/everything?q=(covid OR corona) AND {} AND sector&apiKey={}&language=en&sortBy=publishedAt&pageSize=100&to={}'.format(keyword,self.key,toDate)
        else:
            url = 'https://newsapi.org/v2/everything?q=(covid OR corona) AND {} AND sector&apiKey={}&language=en&sortBy=publishedAt&pageSize=100'.format(keyword,self.key)
        return url

    def cleanAndSave(self,articles,sector):
        filtered = defaultdict(list)
        for article in articles:
            filtered['title'].append(article['title'])
            filtered['description'].append(article['description'])
            filtered['publishedAt'].append(article['publishedAt'])
        cleanDF = pd.DataFrame.from_dict(filtered)
        cleanDF.to_csv('./../data/news/{}.csv'.format(sector), mode='a', index = False, header=False)

    def fetchNews(self):
        for backdays in range(30,32):
            fetchDate = (datetime.datetime.today().date()-datetime.timedelta(days=backdays)).isoformat()
            for sector in self.sectors:
                response = requests.get(self.generateURL(' AND '.join(sector.split()),fetchDate,fetchDate)).json()
                try:
                    self.cleanAndSave(response['articles'],''.join(sector.split()))
                    print('Saved {}.csv of {}'.format(sector,fetchDate))
                except KeyError as e:
                    print(e)


if __name__ == "__main__":
    
    # key = 'c7cbeeb8111b4f97b052fd9441183f1f'
    # key = '7d241a0335de4d7394d95d1acf471aad'
    # key = '35b15026724f41eaaf44d114dc30edf1'
    key = '8b28ac7492c94e6e886081d42968d6f6'
    sectors = ['Communication Services','Consumer Discretionary','Consumer Staples','Energy','Financials',
                'Health Care','Industrials','Information Technology','Materials','Real Estate','Utilities',]
    
    data = News(sectors=sectors,key=key)
    data.fetchNews()
                
    



