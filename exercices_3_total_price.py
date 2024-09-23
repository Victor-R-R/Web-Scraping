"""
Exercice qui récupére le prix total et le stock de la bibliothèque.

"""
import sys
from typing import List
import re
from urllib.parse import urljoin

from selectolax.parser import HTMLParser
from loguru import logger
import requests


# Initialisation du logger
logger.remove()
logger.add(f'books.log', rotation="5000kb", level="INFO")
logger.add(sys.stderr, level="INFO")

BASE_URL = "https://books.toscrape.com/index.html"

def get_all_urls_books(url: str)-> List[str]:
    # Récupere toutes les URLs des livres sur toutes les pages à partir d'une URL

    urls = []

    with requests.Session() as session:

        while True:
            logger.info(f"Récupération des livres de la page {url}")
            try:
                response = session.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                logger.error(f"Erreur lors de la requête HTTP {url}: {err}")
                continue
            
            tree = HTMLParser(response.text)
            books_urls = get_all_books_urls_on_page(url, tree)
            urls.extend(books_urls)

            url = get_next_page_url(url, tree)
            if not url:
                break


    return urls

def get_next_page_url(url: str, tree: HTMLParser)-> str | None:
    # Récupère l'URL de la page suivante à partir du HTML d'une page donnée.

    next_page_node = tree.css_first('li.next > a')
    if next_page_node and 'href' in next_page_node.attributes:
        return urljoin(url, next_page_node.attributes['href'])
    
    logger.info("Aucune page suivante disponible.")
    return None 


def get_all_books_urls_on_page(url: str, tree: HTMLParser)-> List[str]:
    # Récupère tous les URLs des livres sur une page spécifique.
    try:
        books_links_nodes = tree.css("h3 > a")
        return [urljoin(url, link.attributes['href']) for link in books_links_nodes if 'href' in link.attributes]
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des URLs des livres: {e}")
        return []
def get_book_price(url: str, session: requests.Session = None)-> float:
    # Récupère le prix d'un livre à partir de l'URL
    try:
        if session:
            response = session.get(url)
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        tree = HTMLParser(response.text)
        price = extract_price_from_page(tree = tree)
        stock = extract_stock_quantity_from_page(tree = tree)
        price_stock = price * stock
        logger.info(f"Get book price at {url}: found {price_stock}")
    
        return price_stock

    except requests.exceptions.RequestException as err:
        logger.error(f"Erreur lors de la requête HTTP: {err}")
        return 0.0
    
def extract_price_from_page(tree: HTMLParser)-> float:
    # Récupère le prix total d'un livre à partir du HTML
    
    price_node = tree.css_first('p.price_color')
    if price_node:
        price_string = price_node.text()
    else:
        logger.error("Aucun noeud contenant le prix n'a été trouvé.")
        return 0.0
    
    try:
        price = re.findall(r"[0-9.]+", price_string)[0]
    except IndexError as e:
        logger.error(f"Aucun nombre n'a été trouvé: {e}")
        return 0.0
    else:
        return float(price)
def extract_stock_quantity_from_page(tree: HTMLParser)-> int:
    # Récupère la quantité disponible d'un livre à partir du HTML
    try:
        stock_node = tree.css_first('p.instock.availability')
        return int(re.findall(f"\d+", stock_node.text())[0])
    except AttributeError as e:
        logger.error(f"Aucun noeud 'p.instock.availability' n'a été trouvé sur la page: {e}.")
        return 0
    except IndexError as e:
        logger.error(f"Aucune nombre n'a été trouvée dans le noeud: {e}.")
        return 0
    
def main():
    base_url = "https://books.toscrape.com/index.html"
    all_books_urls = get_all_urls_books(url=base_url)
    total_price = []
    with requests.Session() as session:
        for book_url in all_books_urls:
            price = get_book_price(url=book_url, session=session)
            total_price.append(price)
            
    return sum(total_price)
if __name__ == "__main__":
    print(main())