import requests
from bs4 import BeautifulSoup  
from pprint import pprint


url = 'https://books.toscrape.com'
response = requests.get(url)

with open('index.html', 'w') as f:
    f.write(response.text)

with open('index.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(response.text, 'html.parser')
aside = soup.find('div', class_='side_categories')
categories_div= aside.find('ul').find('li').find('ul')
categories = [child.text.strip() for child in categories_div.children if child.name]

images = soup.find('section').find_all('img')
images_urls = [image['src'].strip() for image in images if image.get('src')]

""" articles = soup.find_all('article', class_='product_pod')

for article in articles:
    links = article.find_all('a')
    if len(links) >= 2:
        link = links[1]
        pprint(link.get('title'))
        

 """

titles_tags = soup.find_all('a', title=True)
titles = [a['title'] for a in titles_tags]
pprint(titles)