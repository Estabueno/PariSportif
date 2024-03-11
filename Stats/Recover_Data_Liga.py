# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup

# URL de la page web
url = "https://www.enligne.parionssport.fdj.fr/paris-football/espagne/laliga"

# Envoyer une requête GET à l'URL
response = requests.get(url)

# Fonction pour récupérer les informations sur les matchs de la Liga
def Match_Liga():
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu de la page HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver la balise div avec la classe "psel-webapp-wrapper"
        psel_webapp_wrapper = soup.find('div', class_='psel-webapp-wrapper')

        # Trouver toutes les balises div avec la classe "psel-market--3-columns" à l'intérieur de psel-webapp-wrapper
        opponent_info = psel_webapp_wrapper.find_all('div', class_='psel-market--3-columns')
        
        # Initialiser les listes pour stocker les données 
        home_team = []
        away_team = []
        draw = []
        home_bet = []
        away_bet = []

        # Parcourir chaque balise div avec la classe "psel-market--3-columns"
        for info in opponent_info:
            # Extraire le texte des balises p avec la classe "psel-market__label"
            teams = info.find_all('p', class_='psel-market__label')
            
            # Extraire le texte des balises span avec la classe "psel-outcome__data"
            bets = info.find_all('span', class_='psel-outcome__data')
            
            # Stocker les données dans les listes correspondantes
            home_team.append(teams[0].text.strip())
            away_team.append(teams[2].text.strip())
            
            i = 0
            
            # Récupérer les cotes des matchs
            for bet in bets:
                if(i == 0):
                    home_bet.append(bet.text.strip())
                elif(i == 1):
                    draw.append(bet.text.strip())
                else:
                    away_bet.append(bet.text.strip())
                i+=1
        
        # Retourner un dictionnaire contenant les informations sur les matchs
        return {'home_team': home_team, 'away_team': away_team, 'draw' : draw, 'home_bet' : home_bet, 'away_bet' : away_bet}
    else:
        print("La requête GET a échoué avec le code :", response.status_code)