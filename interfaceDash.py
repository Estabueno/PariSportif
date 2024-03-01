from dash import Dash, html, dcc, callback, Output, Input, dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import State
import os
import sqlite3

external_stylesheets = ['https://use.fontawesome.com/releases/v5.8.1/css/all.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

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

app.layout = html.Div(
    children=[
        dcc.RadioItems(
            id='championship-button',
            options=[
                {'label': 'Premier League', 'value': 'PL'},
                {'label': 'Liga', 'value': 'Liga'}
            ],
            value='PL',
            labelStyle={'display': 'block'}
        ),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
        html.H1(id='championship-title'),
        dash_table.DataTable(
            id='match-info-table',
            columns=[
                {'name': 'Match', 'id': 'match'},
                {'name': 'Cote', 'id': 'cote'},
                {'name': 'Prono', 'id': 'prono', 'presentation': 'markdown'},
            ],
            style_table={'height': '900px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center'},
            style_data={'whiteSpace': 'normal'},
        ),
    ]
)

@app.callback(
    [Output('match-info-table', 'data'),
     Output('championship-title', 'children')],
    [Input('championship-button', 'value')]
)

def update_match_info(championship):
    if championship == 'Liga':
        matches = resultats_liga
        championnat_label = 'Match de Liga'
    elif championship == 'PL':
        matches = resultats_pl
        championnat_label = 'Match de Premier League'

    match_info = [
        {
            'match': f"{match[1]} - {match[4]}",
            'cote': f"1:{match[2]} N:{match[3]} 2:{match[5]}",
            'prono': f'[Voir Prono](/prono/{championship}/{match[0]})',
        }
        for match in matches
    ]

    return match_info, championnat_label

if __name__ == '__main__':
    app.run_server(debug=True)
    