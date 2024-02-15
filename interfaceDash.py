from dash import Dash, html
import os
import sqlite3

# Nom de le base de données
nom_liga = 'Match_Liga.db'
# Nom de le base de données
nom_pl = 'Match_Pl.db'

# Vérifiez si le fichier de la base de données existe
if os.path.isfile(nom_liga) and os.path.isfile(nom_pl):
    # Si le fichier existe, connexion à la base de données
    connexion_1 = sqlite3.connect(nom_liga, check_same_thread=False)
    connexion_2 = sqlite3.connect(nom_pl, check_same_thread=False)

    # Créez un objet curseur pour exécuter des requêtes SQL
    cursor_1 = connexion_1.cursor()
    cursor_2 = connexion_2.cursor()

    # Exécutez une requête SQL pour récupérer toutes les lignes de la table
    cursor_1.execute('SELECT * FROM Matchs')
    cursor_2.execute('SELECT * FROM Matchs')

    # Récupérez toutes les lignes de résultats
    resultats_Liga = cursor_1.fetchall()
    resultats_Pl = cursor_2.fetchall()

    # Fermez le curseur et la connexion à la base de données
    cursor_1.close()
    cursor_2.close()
    connexion_1.close()
    connexion_2.close()
else:
    print("La base de données n'existe pas, veuillez exécuter les programme DataBaseLiga.py et DataBasePl.py.")

app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(
    children=[
        html.H1("Equipe de Premier League"),
        # Afficher la liste
        html.Ul([html.Li(element) for element in resultats_Pl]),
        html.P(" "),
        html.H1("Equipe de Liga"),
        html.Ul([html.Li(element) for element in resultats_Liga])
    ]
)

if __name__ == '__main__':
    app.run(debug=True)