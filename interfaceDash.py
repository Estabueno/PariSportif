from dash import Dash, html
from bs4 import BeautifulSoup
import requests

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

app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(
    children=[
        html.H1("Equipe de Premier League"),
        
        # Afficher la liste
        html.Ul([html.Li(element) for element in get_TeamName()]),
    ]
)

if __name__ == '__main__':
    app.run(debug=True)