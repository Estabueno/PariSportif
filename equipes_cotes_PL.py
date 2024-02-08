import requests
from bs4 import BeautifulSoup

url = "https://www.enligne.parionssport.fdj.fr/paris-football/angleterre/premier-league"

# Envoyer une requête GET à l'URL
response = requests.get(url)

# Vérifier si la requête a réussi (code 200)
if response.status_code == 200:
    # Utiliser Beautiful Soup pour analyser le contenu de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver la balise div avec la classe "psel-webapp-wrapper"
    psel_webapp_wrapper = soup.find('div', class_='psel-webapp-wrapper')

    # Trouver toutes les balises div avec la classe "psel-market--3-columns" à l'intérieur de psel-webapp-wrapper
    opponent_info = psel_webapp_wrapper.find_all('div', class_='psel-market--3-columns')

    # Afficher le contenu de chaque balise div class="psel-market psel-market--3-columns psel-market__row"
    for info in opponent_info:
        # Extraire le texte des balises span avec la classe "psel-opponent__name"
        teams = info.find_all('p', class_='psel-market__label')
        
        # Extraire le texte des balises span avec la classe "psel-opponent__quote"
        quotes = info.find_all('span', class_='psel-outcome__data')
        
        # Afficher le résultat formaté
        for team, quote in zip(teams, quotes):
            print(f"{team.text.strip()}: {quote.text.strip()}", end=" ")
        print()  # Passer à la ligne suivante
else:
    print("La requête GET a échoué avec le code :", response.status_code)
