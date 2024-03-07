import requests
from bs4 import BeautifulSoup

# Fonction pour récupérer les noms des équipes
def get_TeamName():
    url = 'https://www.premierleague.com/clubs'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find('div', class_='clubIndex col-12')
        
        if results:
            data = []
            teamsName = results.find_all('h2', class_='club-card__name')
            
            if teamsName:
                for teams in teamsName:
                    data.append(teams.text)
                return data
        else:
            print("Aucun élément correspondant trouvé.")
    else:
        print("La requête a échoué. Code de statut : ", response.status_code)

def Match_PL():
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

        # Afficher le contenu de chaque balise div class="psel-market psel-market--3-columns psel-market__row"
        for info in opponent_info:
            # Extraire le texte des balises span avec la classe "psel-opponent__name"
            teams = info.find_all('p', class_='psel-market__label')
            
            # Extraire le texte des balises span avec la classe "psel-opponent__quote"
            bets = info.find_all('span', class_='psel-outcome__data')
            
            # Stocker les données dans les listes correppondantes
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
        
        return  {'home_team': home_team, 'away_team': away_team, 'draw' : draw, 'home_bet' : home_bet, 'away_bet' : away_bet}
    else:
        print("La requête GET a échoué avec le code :", response.status_code)
        
def Win_Lose():
    url = "https://www.premierleague.com/tables"

    # Envoyer une requête GET à l'URL
    response = requests.get(url)

    PlTeams = get_TeamName()
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser Beautiful Soup pour analyser le contenu de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupérer les stats des équipes
        home_team = Match_PL()['home_team']
        away_team = Match_PL()['away_team']
        
        # Initialiser les listes pour stocker les données 
        home_stat = []
        away_stat = []

        for homeTeam, awayTeam in zip (home_team, away_team):
            # Comparaison des équipes
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
                # Filtrer la recherche
                homeStat = home.find('td', class_="league-table__form form hideMed")
                awayStat = away.find('td', class_="league-table__form form hideMed")
                
                # Trouver toutes les balises pour les 5 derniers matchs joués 
                played_home = homeStat.find_all('abbr', class_="form-abbreviation")
                played_away = awayStat.find_all('abbr', class_="form-abbreviation")
                
                if played_home:
                    # Afficher le contenu et le récupérer 
                    for plays in played_home:
                        home_stat.append(plays.text.strip())
                            
                    # Afficher le contenu et le récupérer 
                    for plays in played_away:
                        away_stat.append(plays.text.strip())
                else:
                    print("Aucun élément correspondant trouvé pour les stats")
            else:
                print("Aucun élément correspondant trouvé pour l'équipe : ", homeTeam)
                
        # Découper la liste en tableaux de 5 en 5
        home_stat = [home_stat[i:i+5] for i in range(0, len(home_stat), 5)]
        away_stat = [away_stat[i:i+5] for i in range(0, len(away_stat), 5)]
        return {'home_stat': home_stat, 'away_stat': away_stat}
    else:
        print("La requête GET a échoué avec le code :", response.status_code)
            
def get_TeamLogo():
    url = "https://www.premierleague.com/tables"

    # Envoyer une requête GET à l'URL
    response = requests.get(url)

    PlTeams = get_TeamName()
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser Beautiful Soup pour analyser le contenu de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupérer les stats des équipes
        home_team = Match_PL()['home_team']
        away_team = Match_PL()['away_team']
        
        # Initialiser les listes pour stocker les données 
        home_url = []
        away_url = []

        for homeTeam, awayTeam in zip (home_team, away_team):
            # Comparaison des équipes
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
                home_tag = home.find('img')
                away_tag = away.find('img')
                home_src = home_tag.get('src')
                away_src = away_tag.get('src')
                home_url.append(home_src)
                away_url.append(away_src)
            else:
                    print("Aucun élément correspondant trouvé")
        else:
                print("Aucun élément correspondant trouvé.")
                
        return {'home_url': home_url, 'away_url': away_url}
    else:
            print("La requête a échoué. Code de statut : ", response.status_code)