import requests
from bs4 import BeautifulSoup as BS
from django.apps import apps

# Article = apps.get_model('news', 'Article')
r = requests.get(r'https://mig.kz')
html = BS(r.content, 'html.parser')

for i in html.select('.external-rates'):
    date = i.select('.date')
    for j in i.select('li'):
        value = j.select('h4')
        currency = j.select('p')
        print(value[0].text)
        print(currency[0].text)
        print(date[0].text)