import requests

def generateURL(keyword,fromDate,toDate):
    url = 'https://newsapi.org/v2/everything?qInTitle=covid AND {}&apiKey=c7cbeeb8111b4f97b052fd9441183f1f&language=en&pageSize=100&from={}&to={}'.format(keyword,fromDate,toDate)
    return url

response = requests.get(generateURL('oil','2020-05-16','2020-05-16'))
print(response.json())
