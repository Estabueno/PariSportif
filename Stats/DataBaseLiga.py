# Import des modules nécessaires
import sqlite3
import Recover_Data_Liga

# Connexion à la base de données (si elle n'existe pas, elle sera créée) 
conn = sqlite3.connect('Match_Liga.db')

# Création d'un curseur pour exécuter des requêtes SQL 
cur = conn.cursor()

# Création de la table si elle n'existe pas déjà 
cur.execute('''CREATE TABLE IF NOT EXISTS Matchs(
    Match INTEGER PRIMARY KEY, Equipe_Domicile TEXT, Cotes_Equipe_Domicile INTEGER, 
    Cotes_Nul INTEGER, Equipe_Extérieur TEXT,
    Cotes_Equipe_Extérieur INTEGER)''')

# Supprime les lignes de la table s'il elle a déjà été remplie.
cur.execute('DELETE FROM Matchs')

# Valider les modifications et fermer le curseur 
conn.commit()

# Supprime les pages inutiles
cur.execute('VACUUM')

# Récupération des données nécessaires
home_team_value = Recover_Data_Liga.Match_Liga()['home_team']
away_team_value = Recover_Data_Liga.Match_Liga()['away_team']
draw_bets_value = Recover_Data_Liga.Match_Liga()['draw'] 
home_bets_value = Recover_Data_Liga.Match_Liga()['home_bet'] 
away_bets_value = Recover_Data_Liga.Match_Liga()['away_bet'] 

# Remplissage de la table avec les données récupérées
for home, away, draw, home_bet, away_bet in zip(home_team_value, away_team_value, draw_bets_value, home_bets_value, away_bets_value):
    # Insertion de données dans la table Matchs
    cur.execute("INSERT INTO Matchs (Equipe_Domicile, Cotes_Equipe_Domicile, Cotes_Nul, Equipe_Extérieur, Cotes_Equipe_Extérieur) VALUES (?, ?, ?, ?, ?)", (home, home_bet, draw, away, away_bet)) 

# Valider les modifications et fermer le curseur 
conn.commit()

# Fermer la connexion à la base de données 
cur.close()
conn.close()