# Import des modules nécessaires
import sqlite3
import Recover_Data_PL

# Connexion à la base de données (si elle n'existe pas, elle sera créée) 
conn = sqlite3.connect('Match_Pl.db')

# Création d'un curseur pour exécuter des requêtes SQL 
cur = conn.cursor()

# Création des tables si elles n'existent pas déjà
cur.execute('''CREATE TABLE IF NOT EXISTS Matchs(
    Match INTEGER PRIMARY KEY, Equipe_Domicile TEXT, Cotes_Equipe_Domicile REAL, 
    Cotes_Nul REAL, Equipe_Extérieur TEXT,
    Cotes_Equipe_Extérieur REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS WinLoss(
    Match INTEGER PRIMARY KEY, HomeWinLossDraw TEXT, AwayWinLossDraw TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Url_Logo(
    Match INTEGER PRIMARY KEY, Equipe_Domicile_Url TEXT, Equipe_Extérieur_Url TEXT)''')

# Supprime les lignes de la table s'il elle a déjà été remplie.
cur.execute('DELETE FROM Matchs')
cur.execute('DELETE FROM WinLoss')
cur.execute('DELETE FROM Url_Logo')

# Valider les modifications et fermer le curseur 
conn.commit()

# Supprime les pages inutiles
cur.execute('VACUUM')

# Récupération des données nécessaires
home_team_value = Recover_Data_PL.Match_PL()['home_team']
away_team_value = Recover_Data_PL.Match_PL()['away_team']
draw_bets_value = Recover_Data_PL.Match_PL()['draw'] 
home_bets_value = Recover_Data_PL.Match_PL()['home_bet'] 
away_bets_value = Recover_Data_PL.Match_PL()['away_bet'] 

home_winLoss = Recover_Data_PL.Win_Lose()['home_stat']
away_winLoss = Recover_Data_PL.Win_Lose()['away_stat']

home_url = Recover_Data_PL.get_TeamLogo()['home_url']
away_url = Recover_Data_PL.get_TeamLogo()['away_url']

# Remplissage des tables avec les données récupérées
for home, away, draw, home_bet, away_bet in zip(home_team_value, away_team_value, draw_bets_value, home_bets_value, away_bets_value):
    # Insertion de données dans la table Matchs
    cur.execute("INSERT INTO Matchs (Equipe_Domicile, Cotes_Equipe_Domicile, Cotes_Nul, Equipe_Extérieur, Cotes_Equipe_Extérieur) VALUES (?, ?, ?, ?, ?)", (home, home_bet, draw, away, away_bet)) 
    
i = 0
for home, away in zip(home_team_value, away_team_value):
    # Insertion de données dans la table WinLoss
    cur.execute("INSERT INTO WinLoss (HomeWinLossDraw, AwayWinLossDraw) VALUES (?, ?)", (''.join(home_winLoss[i]),''.join(away_winLoss[i]))) 
    i+=1
    
for home, away in zip(home_url, away_url):
    # Insertion de données dans la table Url_Logo
    cur.execute("INSERT INTO Url_Logo (Equipe_Domicile_Url, Equipe_Extérieur_Url) VALUES (?, ?)", (home, away)) 
    
    
# # Test unitaire (à décommenter pour l'utiliser)
# print("Test unitaire pour avoir le nom des équipes à domicile qui ont plus de 1.8 de cote : ")
# # Exécutez la requête SQL
# request = "SELECT Equipe_Domicile FROM Matchs WHERE CAST(REPLACE(Cotes_Equipe_Domicile, ',', '.') AS REAL) > 1.8;"
# cur.execute(request)

# # Récupérez les résultats de la requête
# results = cur.fetchall()

# # Affichez les résultats
# for result in results:
#     home_team = result
#     print(f"Equipe : {home_team}")
    
# Valider les modifications et fermer le curseur 
conn.commit()

# Fermer la connexion à la base de données 
cur.close()
conn.close()