"""
Exercices qui recherche les livres sur un site web en fonction du nombre d'etoiles
"""

import re

import requests 
from bs4 import BeautifulSoup 


# Crée la fonction
def main() -> list[int]: 

    book_ids = []
    # Tente de récupérer la page web et gère les exceptions
    try:
        response = requests.get('https://books.toscrape.com')
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
        raise requests.exceptions.RequestException from err
    
    # Parse le texte de la réponse avec BeautifulSoup
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

    # Trouve tous les livres avec une étoile unique et affiche leurs titres
    one_star_books = soup.select('p.star-rating.One')
    # Trouve les titres
    for book in one_star_books:
        try:
            book_link = (book.find_next('h3').find('a')['href'])
            
        except AttributeError as err:
            print('Impossible de trouver la balise <h3>')
            raise AttributeError from err
        except TypeError as err:
            print('Impossible de trouver la balise <a>')
            raise TypeError from err
        except KeyError as err:
            print('Impossible de trouver le [href]')
            raise KeyError from err
        
        try:
            # Récupère le ID du livre avec expressions regulieres
            book_id = re.findall(r"_\d+", book_link)[0][1:]
        except IndexError as err:
            print('Impossible de trouver l\'ID du livre')
            raise IndexError from err
        else:
            book_ids.append(int(book_id))

    return book_ids
        
if __name__ == '__main__':
    print(main())