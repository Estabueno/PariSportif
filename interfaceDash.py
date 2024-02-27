from dash import Dash, html, dcc, callback, Output, Input
import os
import sqlite3

external_stylesheets = ['https://use.fontawesome.com/releases/v5.8.1/css/all.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Vérifier si le fichier de la base de données existe
nom_liga = 'Match_Liga.db'
nom_pl = 'Match_Pl.db'

if os.path.isfile(nom_liga) and os.path.isfile(nom_pl):
    # Si le fichier existe, connexion à la base de données
    connexion_liga = sqlite3.connect(nom_liga, check_same_thread=False)
    connexion_pl = sqlite3.connect(nom_pl, check_same_thread=False)

    # Créez un objet curseur pour exécuter des requêtes SQL
    cursor_liga = connexion_liga.cursor()
    cursor_pl = connexion_pl.cursor()

    # Exécutez une requête SQL pour récupérer toutes les lignes de la table
    cursor_liga.execute('SELECT * FROM Matchs')
    cursor_pl.execute('SELECT * FROM Matchs')

    # Récupérez toutes les lignes de résultats
    resultats_liga = cursor_liga.fetchall()
    resultats_pl = cursor_pl.fetchall()

    # Fermez le curseur et la connexion à la base de données
    cursor_liga.close()
    cursor_pl.close()
    connexion_liga.close()
    connexion_pl.close()
else:
    print("La base de données n'existe pas, veuillez exécuter les programmes DataBaseLiga.py et DataBasePl.py.")

def format_match_info(match):
    return [
        f"{match[1]} - {match[4]}",
        html.P(f"1:{match[2]} N:{match[3]} 2:{match[5]}"),
        html.P(" "),
    ]

app.layout = html.Div(
    children=[
        dcc.RadioItems(
            id='championship-radio',
            options=[
                {'label': 'Liga', 'value': 'Liga'},
                {'label': 'Premier League', 'value': 'Premier League'}
            ],
            value='Liga',
            labelStyle={'display': 'block'}
        ),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
        html.H1("Matchs de Football"),
        html.Div(id='match-info-container')
    ]
)

@app.callback(
    Output('match-info-container', 'children'),
    [Input('championship-radio', 'value')]
)
def update_match_info(championship):
    if championship == 'Liga':
        matches = resultats_liga
    elif championship == 'Premier League':
        matches = resultats_pl
    else:
        return [html.P("Championnat non valide")]

    match_info = [
        format_match_info(match) for match in matches
    ]

    return [html.Div(info) for info in match_info]

if __name__ == '__main__':
    app.run_server(debug=True)
