import requests
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='c7cbeeb8111b4f97b052fd9441183f1f')

# /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           sources='bbc-news,the-verge',
#                                           category='business',
#                                           language='en',
#                                           country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='covid AND oil',
                                      from_param='2020-05-10',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

# /v2/sources
sources = newsapi.get_sources()
print((sources['sources']))