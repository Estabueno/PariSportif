import requests
from bs4 import BeautifulSoup

url = "https://www.premierleague.com/stats/top/players/goals?se=578"

try:
    response = requests.get(url)
    response.raise_for_status() 
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.find('div', class_='table')


    if table:
        rows = table.find_all('tbody', class_='stats-table__container')
        print("Voici le classement des meilleurs buteurs de la PL : ")

        
        
        for row in rows:
            matches = row.find_all('a',class_='playerName')
            for match in matches:
                
                print(match.text)
    else:
        print("pas de Table.")

except Exception as e:
    print("erreur", e)
