import requests
from fastapi import FastAPI
from bs4 import BeautifulSoup

app = FastAPI()

@app.get('/news')
def get_news():
    url =  'https://indianexpress.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = []
    for item in soup.findAll('a', class_='topblockNews__sidebarLink'):
        title.append(item.text)
    
    return {
        'news_headlines': title[:5]
    }

