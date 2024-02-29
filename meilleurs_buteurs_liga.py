import requests
from bs4 import BeautifulSoup

url = "https://www.laliga.com/en-FR/stats/laliga-easports/scorers"

try:
    response = requests.get(url)
    response.raise_for_status() 
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.find('div', class_='styled__ContainerTable-sc-57jgok-0')


    if table:
        rows = table.find_all('table', class_='styled__TableStyled-sc-57jgok-1')
        print("Voici le classement des meilleurs buteurs de laliga : ")
        
        
        for row in rows:
            matches = row.find_all('td',class_='styled__TdStyled-sc-57jgok-4')
            for match in matches:
                print(match.text)
    else:
        print("pas de Table.")

except Exception as e:
    print("erreur", e)
