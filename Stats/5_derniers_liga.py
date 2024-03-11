import requests
from bs4 import BeautifulSoup

team_urls = [
    "https://www.laliga.com/en-FR/clubs/athletic-club/results",
    "https://www.laliga.com/en-FR/clubs/atletico-de-madrid/results",
    "https://www.laliga.com/en-FR/clubs/c-a-osasuna/results",
    "https://www.laliga.com/en-FR/clubs/cadiz-cf/results",
    "https://www.laliga.com/en-FR/clubs/d-alaves/results",
    "https://www.laliga.com/en-FR/clubs/fc-barcelona/results",
    "https://www.laliga.com/en-FR/clubs/getafe-cf/results",
    "https://www.laliga.com/en-FR/clubs/girona-fc/results",
    "https://www.laliga.com/en-FR/clubs/granada-cf/results",
    "https://www.laliga.com/en-FR/clubs/rayo-vallecano/results",
    "https://www.laliga.com/en-FR/clubs/rc-celta/results",
    "https://www.laliga.com/en-FR/clubs/rcd-mallorca/results",
    "https://www.laliga.com/en-FR/clubs/real-betis/results",
    "https://www.laliga.com/en-FR/clubs/real-madrid/results",
    "https://www.laliga.com/en-FR/clubs/real-sociedad/results",
    "https://www.laliga.com/en-FR/clubs/sevilla-fc/results",
    "https://www.laliga.com/en-FR/clubs/ud-almeria/results",
    "https://www.laliga.com/en-FR/clubs/ud-las-palmas/results",
    "https://www.laliga.com/en-FR/clubs/valencia-cf/results",
    "https://www.laliga.com/en-FR/clubs/villarreal-cf/results",
]

try:
    for url in team_urls:
        response = requests.get(url)
        response.raise_for_status() 
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")

        table = soup.find('div', class_='styled__ListStyled-sc-1nkmudg-0')

        if table:
            rows = table.find_all('tr', class_='styled__TableRow-sc-43wy8s-4')
            
            last_five_matches = []  
            
            for row in rows:
                matches = row.find_all('td', class_='styled__TableCell-sc-43wy8s-5')
                if len(matches) >= 3:  
                    last_five_matches.append(matches[2].text.strip())
            
            # les cinq derniers match
            for match in last_five_matches[-5:]:
                print(match)
            print("-------------------------")
            
        else:
            print("Pas de Table.")

except Exception as e:
    print("Erreur:", e)
