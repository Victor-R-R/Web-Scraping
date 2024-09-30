"""Nous importons la méthode `sync` de la bibliothèque Playwright.
"""
from playwright.sync_api import sync_playwright



# Nous utilisons un `with` pour créer une instance et la stocker dans une variable.
with sync_playwright() as playwright:
    # Nous créons une variable où nous stockons le navigateur dans Chrome avec un en-tête.
    browser = playwright.webkit.launch(headless=False)
    # Nous ouvrons la nouvelle page.
    page = browser.new_page()
    # Nous accédons au site web que nous voulons.
    page.goto("https://www.docstring.fr/scraping/")
    # pour que le navigateur ne se ferme pas immédiatement, nous ajoutons 1 seg.
    page.wait_for_timeout(1000)

    # Nous récupérons le premier bouton qui contient le texte "Récupérer les livres secrets".
    button = page.get_by_role("button", name="Récupérer les livres secrets")

    if button:
        # Si le bouton est présent, nous cliquons dessus.
        button.click()

    # pour que le navigateur ne se ferme pas immédiatement, nous ajoutons 5 seg.
    page.wait_for_timeout(5000)

    # Ferme le navigateur
    browser.close()