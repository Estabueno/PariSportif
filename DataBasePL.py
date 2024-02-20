import sqlite3
import Recover_Data_PL

# Connexion à la base de données (si elle n'existe pas, elle sera créée) 
conn = sqlite3.connect('Match_Pl.db')

# Création d'un curseur pour exécuter des requêtes SQL 
cur = conn.cursor()

# Création de la table si elle n'existe pas déjà 
cur.execute('''CREATE TABLE IF NOT EXISTS Matchs(
    Match INTEGER PRIMARY KEY, Equipe_Domicile TEXT, Cotes_Equipe_Domicile INTEGER, 
    Cotes_Nul INTEGER, Equipe_Extérieur TEXT,
    Cotes_Equipe_Extérieur INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS WinLoss(
    Match INTEGER PRIMARY KEY, Equipe_Domicile TEXT, HomeWinLossDraw TEXT, 
    Equipe_Extérieur TEXT,
    AwayWinLossDraw TEXT)''')

# Supprime les lignes de la table s'il elle a déjà été remplie.
cur.execute('DELETE FROM Matchs')
cur.execute('DELETE FROM WinLoss')

# Valider les modifications et fermer le curseur 
conn.commit()

# Supprime les pages inutiles
cur.execute('VACUUM')

home_team_value = Recover_Data_PL.Match_PL()['home_team']
away_team_value = Recover_Data_PL.Match_PL()['away_team']
draw_bets_value = Recover_Data_PL.Match_PL()['draw'] 
home_bets_value = Recover_Data_PL.Match_PL()['home_bet'] 
away_bets_value = Recover_Data_PL.Match_PL()['away_bet'] 

home_winLoss = Recover_Data_PL.Win_Lose()['home_stat']
away_winLoss = Recover_Data_PL.Win_Lose()['away_stat']

for home, away, draw, home_bet, away_bet in zip(home_team_value, away_team_value, draw_bets_value, home_bets_value, away_bets_value):
    # Insertion de données dans la table
    cur.execute("INSERT INTO Matchs (Equipe_Domicile, Cotes_Equipe_Domicile, Cotes_Nul, Equipe_Extérieur, Cotes_Equipe_Extérieur) VALUES (?, ?, ?, ?, ?)", (home, home_bet, draw, away, away_bet)) 
    
i = 0
for home, away in zip(home_team_value, away_team_value):
    # Insertion de données dans la table
    cur.execute("INSERT INTO WinLoss (Equipe_Domicile, HomeWinLossDraw, Equipe_Extérieur, AwayWinLossDraw) VALUES (?, ?, ?, ?)", (home, ''.join(home_winLoss[i]), away, ''.join(away_winLoss[i]))) 
    i+=1
    
# Valider les modifications et fermer le curseur 
conn.commit()

# Valider les modifications et fermer le curseur conn.commit()
cur.close()

# Fermer la connexion à la base de données 
conn.close()