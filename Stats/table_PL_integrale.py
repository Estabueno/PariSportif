import requests
from bs4 import BeautifulSoup

# URL de la page à scraper
url = 'https://www.premierleague.com/tables'

# Envoie une requête HTTP à l'URL
response = requests.get(url)

# Vérifie si la requête a réussi (statut 200)
if response.status_code == 200:
    # Analyse le contenu HTML de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouve l'élément <tbody> avec la classe 'league-table__tbody'
    tbody_element = soup.find('tbody', class_='league-table__tbody')

    # Vérifie si l'élément <tbody> existe
    if tbody_element:
        # Parcours les éléments <tr> à l'intérieur de l'élément <tbody>
        for tr_element in tbody_element.find_all("tr"):
            # Extrait le texte des éléments <td> entre les indices 1 et 9 inclus
            td_elements = tr_element.find_all("td")[1:10]

            # Stocke les valeurs dans des tableaux
            labels = ["Club", "Played", "Won", "Drawn", "Lost", "GF", "GA", "GD", "Points"]
            values = [td_element.text.strip() for td_element in td_elements]

            # Imprime les valeurs dans le format souhaité
            for label, value in zip(labels, values):
                print(f"{label}\t{value}")

            print()  # Ajoute une ligne vide entre les équipes

    else:
        print('Aucun élément <tbody> avec la classe "league-table__tbody" trouvé.')

else:
    print(f'Erreur {response.status_code} lors de la requête à {url}')
