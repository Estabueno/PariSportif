import requests
from bs4 import BeautifulSoup

TEAM_URLS = [
    ("https://www.premierleague.com/clubs/1/Arsenal/squad?se=578", "Arsenal"),
    ("https://www.premierleague.com/clubs/2/Aston-Villa/squad?se=578", "Aston Villa"),
    ("https://www.premierleague.com/clubs/127/Bournemouth/squad?se=578", "Bournemouth"),
    ("https://www.premierleague.com/clubs/130/Brentford/squad?se=578", "Brentford"),
    ("https://www.premierleague.com/clubs/131/Brighton-and-Hove-Albion/squad?se=578", "Brighton and Hove Albion"),
    ("https://www.premierleague.com/clubs/43/Burnley/squad?se=578", "Burnley"),
    ("https://www.premierleague.com/clubs/4/Chelsea/squad?se=578", "Chelsea"),
    ("https://www.premierleague.com/clubs/6/Crystal-Palace/squad?se=578", "Crystal Palace"),
    ("https://www.premierleague.com/clubs/7/Everton/squad?se=578", "Everton"),
    ("https://www.premierleague.com/clubs/34/Fulham/squad?se=578", "Fulham"),
    ("https://www.premierleague.com/clubs/10/Liverpool/squad?se=578", "Liverpool"),
    ("https://www.premierleague.com/clubs/163/Luton-Town/squad?se=578", "Luton Town"),
    ("https://www.premierleague.com/clubs/11/Manchester-City/squad?se=578", "Manchester City"),
    ("https://www.premierleague.com/clubs/12/Manchester-United/squad?se=578", "Manchester United"),
    ("https://www.premierleague.com/clubs/23/Newcastle-United/squad?se=578", "Newcastle United"),
    ("https://www.premierleague.com/clubs/15/Nottingham-Forest/squad?se=578", "Nottingham Forest"),
    ("https://www.premierleague.com/clubs/18/Sheffield-United/squad?se=578", "Sheffield United"),
    ("https://www.premierleague.com/clubs/21/Tottenham-Hotspur/squad?se=578", "Tottenham Hotspur"),
    ("https://www.premierleague.com/clubs/25/West-Ham-United/squad?se=578", "West Ham United"),
    ("https://www.premierleague.com/clubs/38/Wolverhampton-Wanderers/squad?se=578", "Wolverhampton Wanderers")
]

def get_top_scorer(url, team_name):
    response = requests.get(url)
    top_scorer = {'name': '', 'goals': 0}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_element = soup.find('ul', class_='squadListContainer')

        if ul_element:
            for div_element in ul_element.find_all('li', class_='stats-card'):
                player_name_element = div_element.find('div', class_='stats-card__player-name')
                player_name = ' '.join([name_part.text.strip() for name_part in player_name_element.find_all('div')])
                goals = 0
                stats_elements = div_element.find_all('li')

                for stat_element in stats_elements:
                    stat = stat_element.text.strip()
                    if 'goals' in stat and 'goalsConceded' not in stat:
                        goals = int(stat.split()[0])
                        break

                if goals > top_scorer['goals']:
                    top_scorer['name'] = player_name
                    top_scorer['goals'] = goals

            return team_name, top_scorer['name'], top_scorer['goals']
        else:
            return f'No <ul> element with class "squadListContainer" found in {url}.'
    else:
        return f'Error {response.status_code} while requesting {url}.'

print('Le meilleur buteur de chaque équipe trié en fonction du nombre de buts marqué')
# tri des équipes par le nombre de buts marqués
sorted_teams = sorted(TEAM_URLS, key=lambda x: get_top_scorer(x[0], x[1])[2], reverse=True)

# résultats triés
for url, team_name in sorted_teams:
    team_name, top_scorer_name, goals = get_top_scorer(url, team_name)
    print(f"{team_name}: {top_scorer_name} - {goals} goals")
