"""
Trouve les catégories qui ne contiennent pas beaucoup de livres
afin de renfoncer cette catégorie. L'exercice doit parcourir toutes
les catégories de livres et vérifier le nombre de livres qu'elles contiennent,
puis imprimer uniquement celles qui on moins de 20 livres.
"""

import requests
from bs4 import BeautifulSoup  

url = 'https://books.toscrape.com'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

aside = soup.find('div', class_='side_categories')
categories_div= aside.find('ul').find('li').find('ul')
categories_links= []

for child in categories_div.find_all('li'):
    a_tag= child.find('a')
    category_name = a_tag.text.strip()
    category_link = a_tag['href'].strip()
    full_link = url + '/' + category_link
    categories_links.append((category_name, full_link))

for category_name, category_link in categories_links:
    response = requests.get(category_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')
    num_books = len(books)

    if num_books < 20:
        print(f'{category_name} ont {num_books} livres.')