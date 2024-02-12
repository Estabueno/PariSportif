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
    
    # Initialiser les listes pour stocker les données 
    home_team = []
    draw = []
    away_team = []
    match_quotes = []

    # Afficher le contenu de chaque balise div class="psel-market psel-market--3-columns psel-market__row"
    for info in opponent_info:
        # Extraire le texte des balises span avec la classe "psel-opponent__name"
        teams = info.find_all('p', class_='psel-market__label')
        
        # Extraire le texte des balises span avec la classe "psel-opponent__quote"
        quotes = info.find_all('span', class_='psel-outcome__data')
        
        # Stocker les données dans les listes correppondantes
        home_team.append(teams[0].text.strip())
        draw.append(teams[1].text.strip())
        away_team.append(teams[2].text.strip())
        
        # Récupérer les côtes des matchs
        for quote in quotes:
            match_quotes.append(quote.text.strip())
        
    print(home_team)
    print(away_team)
    print(match_quotes)
else:
    print("La requête GET a échoué avec le code :", response.status_code)