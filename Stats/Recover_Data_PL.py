# Import des modules nécessaires
import requests
from bs4 import BeautifulSoup

# Fonction pour récupérer les noms des équipes
def get_TeamName():
    # URL de la page web
    url = 'https://www.premierleague.com/clubs'
    
    # Envoyer une requête GET à l'URL
    response = requests.get(url)

    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu de la page HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver la balise div avec la classe 'clubIndex col-12'
        results = soup.find('div', class_='clubIndex col-12')
        
        # Vérifier si la balise div est trouvée
        if results:
            data = []
            
            # Trouver toutes les balises h2 avec la classe 'club-card__name' à l'intérieur de results
            teamsName = results.find_all('h2', class_='club-card__name')
            
            # Vérifier si des balises h2 sont trouvées
            if teamsName:
                # Ajouter le texte de chaque balise h2 à la liste data
                for teams in teamsName:
                    data.append(teams.text)
                
                # Retourner la liste des noms des équipes
                return data
        else:
            print("Aucun élément correspondant trouvé.")
    else:
        print("La requête a échoué. Code de statut :", response.status_code)

# Fonction pour récupérer les informations sur les matchs de la Premier League
def Match_PL():
    # URL de la page web
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

# Fonction pour récupérer les statistiques de victoires/défaites des équipes
def Win_Lose():
    # URL de la page web
    url = "https://www.premierleague.com/tables"

    # Envoyer une requête GET à l'URL
    response = requests.get(url)

    # Appeler la fonction get_TeamName pour récupérer les noms des équipes
    PlTeams = get_TeamName()
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser Beautiful Soup pour analyser le contenu de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupérer les noms des équipes et les cotes des matchs
        home_team = Match_PL()['home_team']
        away_team = Match_PL()['away_team']
        
        # Initialiser les listes pour stocker les données 
        home_stat = []
        away_stat = []

        # Parcourir chaque paire d'équipes
        for homeTeam, awayTeam in zip (home_team, away_team):
            # Comparaison des noms des équipes pour les adapter à la page web
            for teams in PlTeams:
                if homeTeam == "Man. City":
                    homeTeam = "Manchester City"
                elif homeTeam == "Man. United":
                    homeTeam = "Manchester United"
                if awayTeam == "Man. City":
                    awayTeam = "Manchester City"
                elif awayTeam == "Man. United":
                    awayTeam = "Manchester United"
                if homeTeam[:5] == teams[:5]:
                    homeTeam = teams
                if awayTeam[:5] == teams[:5]:
                    awayTeam = teams
            
            # Trouver la balise tr des équipes domiciles et extérieur
            home = soup.find('tr', {'data-filtered-table-row-name': homeTeam})
            away = soup.find('tr', {'data-filtered-table-row-name': awayTeam})
            
            if home:
                # Filtrer la recherche pour trouver les statistiques des équipes
                homeStat = home.find('td', class_="league-table__form form hideMed")
                awayStat = away.find('td', class_="league-table__form form hideMed")
                
                # Trouver toutes les balises abbr pour les 5 derniers matchs joués 
                played_home = homeStat.find_all('abbr', class_="form-abbreviation")
                played_away = awayStat.find_all('abbr', class_="form-abbreviation")
                
                if played_home:
                    # Ajouter le contenu des balises abbr à la liste home_stat
                    for plays in played_home:
                        home_stat.append(plays.text.strip())
                            
                    # Ajouter le contenu des balises abbr à la liste away_stat
                    for plays in played_away:
                        away_stat.append(plays.text.strip())
                else:
                    print("Aucun élément correspondant trouvé pour les stats")
            else:
                print("Aucun élément correspondant trouvé pour l'équipe : ", homeTeam)
                
        # Découper la liste en tableaux de 5 en 5
        home_stat = [home_stat[i:i+5] for i in range(0, len(home_stat), 5)]
        away_stat = [away_stat[i:i+5] for i in range(0, len(away_stat), 5)]
        
        # Retourner un dictionnaire contenant les statistiques des équipes
        return {'home_stat': home_stat, 'away_stat': away_stat}
    else:
        print("La requête GET a échoué avec le code :", response.status_code)

# Fonction pour récupérer les logos des équipes
def get_TeamLogo():
    # URL de la page web
    url = "https://www.premierleague.com/tables"

    # Envoyer une requête GET à l'URL
    response = requests.get(url)

    # Appeler la fonction get_TeamName pour récupérer les noms des équipes
    PlTeams = get_TeamName()
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser Beautiful Soup pour analyser le contenu de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupérer les noms des équipes et les cotes des matchs
        home_team = Match_PL()['home_team']
        away_team = Match_PL()['away_team']
        
        # Initialiser les listes pour stocker les données 
        home_url = []
        away_url = []

        # Parcourir chaque paire d'équipes
        for homeTeam, awayTeam in zip (home_team, away_team):
            # Comparaison des noms des équipes pour les adapter à la page web
            for teams in PlTeams:
                if homeTeam == "Man. City":
                    homeTeam = "Manchester City"
                elif homeTeam == "Man. United":
                    homeTeam = "Manchester United"
                if awayTeam == "Man. City":
                    awayTeam = "Manchester City"
                elif awayTeam == "Man. United":
                    awayTeam = "Manchester United"
                if homeTeam[:5] == teams[:5]:
                    homeTeam = teams
                if awayTeam[:5] == teams[:5]:
                    awayTeam = teams
            
            # Trouver la balise tr des équipes domiciles et extérieur
            home = soup.find('tr', {'data-filtered-table-row-name': homeTeam})
            away = soup.find('tr', {'data-filtered-table-row-name': awayTeam})
            
            if home:
                # Trouver la balise img pour les logos des équipes
                home_tag = home.find('img')
                away_tag = away.find('img')
                
                # Récupérer l'URL des logos et les ajouter aux listes home_url et away_url
                home_src = home_tag.get('src')
                away_src = away_tag.get('src')
                home_url.append(home_src)
                away_url.append(away_src)
            else:
                print("Aucun élément correspondant trouvé")
    else:
        print("Aucun élément correspondant trouvé.")
    
    # Retourner un dictionnaire contenant les URL des logos des équipes
    return {'home_url': home_url, 'away_url': away_url}

# if __name__ == "__main__":
#     # Test unitaire pour obtenir le nom des équipes
#     print("Test unitaire pour obtenir le nom des équipes : ")
#     teams = get_TeamName()
#     print(teams)

#     # Test unitaire pour obtenir les cotes du match nul pour chaque match
#     print("Test unitaire pour obtenir les cotes du match nul pour chaque match : ")
#     draw_bet = Match_PL()['draw']
#     print(draw_bet)
