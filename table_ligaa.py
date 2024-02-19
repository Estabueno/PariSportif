import requests
from bs4 import BeautifulSoup

url = 'https://www.laliga.com/en-GB/laliga-easports/standing'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('div', class_='styled__ContainerAccordion-sc-e89col-11')

    count = 0  # compter les lignes affichées

    print("Classement\tÉquipe\tPoints\tMJ\tG\tD\tN\tButs\tEncaissés\tDifference")

    for table in tables:
        team_containers = table.find_all('div', class_='styled__StandingTabBody-sc-e89col-0')

        for team_container in team_containers:
            team_data = team_container.find_all('div', class_='styled__Td-sc-e89col-10')

            values = []

            for data in team_data:
                values.append(data.text.strip())

            print("\t".join(values))
            count += 1  

            if count == 20: 
                break

        if count == 20:
            break
