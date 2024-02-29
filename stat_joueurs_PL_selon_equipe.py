import requests
from bs4 import BeautifulSoup

def get_team_stats(team_name):
    team_urls = {
        'Manchester City': 'https://www.premierleague.com/clubs/11/Manchester-City/squad?se=578',
        'Arsenal': 'https://www.premierleague.com/clubs/1/Arsenal/squad?se=578',
        'Aston Villa': 'https://www.premierleague.com/clubs/2/Aston-Villa/squad?se=578',
        'Bournemouth': 'https://www.premierleague.com/clubs/127/Bournemouth/squad?se=578',
        'Brentford': 'https://www.premierleague.com/clubs/130/Brentford/squad?se=578',
        'Brighton': 'https://www.premierleague.com/clubs/131/Brighton-and-Hove-Albion/squad?se=578',
        'Burnley': 'https://www.premierleague.com/clubs/43/Burnley/squad?se=578',
        'Chelsea': 'https://www.premierleague.com/clubs/4/Chelsea/squad?se=578',
        'Crystal Palace': 'https://www.premierleague.com/clubs/6/Crystal-Palace/squad?se=578',
        'Everton': 'https://www.premierleague.com/clubs/7/Everton/squad?se=578',
        'Fulham': 'https://www.premierleague.com/clubs/34/Fulham/squad?se=578',
        'Liverpool': 'https://www.premierleague.com/clubs/10/Liverpool/squad?se=578',
        'Luton Town': 'https://www.premierleague.com/clubs/163/Luton-Town/squad?se=578',
        'Manchester United': 'https://www.premierleague.com/clubs/12/Manchester-United/squad?se=578',
        'Newcastle United': 'https://www.premierleague.com/clubs/23/Newcastle-United/squad?se=578',
        'Nottingham Forest': 'https://www.premierleague.com/clubs/15/Nottingham-Forest/squad?se=578',
        'Sheffield United': 'https://www.premierleague.com/clubs/18/Sheffield-United/squad?se=578',
        'Tottenham Hotspur': 'https://www.premierleague.com/clubs/21/Tottenham-Hotspur/squad?se=578',
        'West Ham United': 'https://www.premierleague.com/clubs/25/West-Ham-United/squad?se=578',
        'Wolverhampton ':'https://www.premierleague.com/clubs/38/Wolverhampton-Wanderers/squad?se=578',
    }

    if team_name in team_urls:
        url = team_urls[team_name]

        response = requests.get(url)

        # stocker les informations des joueurs
        players_info = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Trouve <ul> avec la classe 'squadListContainer'
            ul_element = soup.find('ul', class_='squadListContainer')

            if ul_element:
                # <div> à l'intérieur de <ul>
                for div_element in ul_element.find_all('li', class_='stats-card'):
                    # nom du joueur
                    player_name_element = div_element.find('div', class_='stats-card__player-name')
                    player_name = ' '.join([name_part.text.strip() for name_part in player_name_element.find_all('div')])

                    # stocke les statistiques du joueur
                    stats_elements = div_element.find_all('li')
                    stats = [stat.text.strip() for stat in stats_elements]
                    player_stats = '\n'.join(stats)

                    # Ajoute les informations du joueur à la liste
                    players_info.append(f'{player_name}:\n{player_stats}\n')

                return players_info

            else:
                return [f'Aucun élément <ul> avec la classe "squadListContainer" trouvé pour {team_name}.']

        else:
            return [f'Erreur {response.status_code} lors de la requête à {url}']

    else:
        return [f'Équipe {team_name} non reconnue.']

team_name_input = input("Entrez le nom de l'équipe (par exemple, Manchester City, Arsenal) : ")

results = get_team_stats(team_name_input)
for result in results:
    print(result)
