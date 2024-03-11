# Import des modules nécessaires de Dash, SQLite et autres
from dash import Dash, html, dcc, callback, Output, Input, dash_table
from dash.exceptions import PreventUpdate
import os
import sqlite3

# Définition des styles externes pour l'application
external_stylesheets = ['https://use.fontawesome.com/releases/v5.8.1/css/all.css']

# Création de l'application Dash
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Vérification de l'existence des fichiers de base de données
Liga = 'Match_Liga.db'
Premier_League = 'Match_Pl.db'

if os.path.isfile(Liga) and os.path.isfile(Premier_League):
    # Connexion aux bases de données
    connexion_liga = sqlite3.connect(Liga, check_same_thread=False)
    connexion_pl = sqlite3.connect(Premier_League, check_same_thread=False)

    # Création des curseurs pour exécuter les requêtes SQL
    cursor_liga = connexion_liga.cursor()
    cursor_pl = connexion_pl.cursor()
    cursor_urlPl = connexion_pl.cursor()
    cursor_winLoss = connexion_pl.cursor()

    # Exécution des requêtes SQL pour récupérer toutes les lignes des tables
    cursor_liga.execute('SELECT * FROM Matchs')
    cursor_pl.execute('SELECT * FROM Matchs')
    cursor_urlPl.execute('SELECT * FROM Url_Logo')
    cursor_winLoss.execute('SELECT * FROM WinLoss')

    # Récupération de toutes les lignes des résultats
    resultats_liga = cursor_liga.fetchall()
    resultats_pl = cursor_pl.fetchall()
    url_pl = cursor_urlPl.fetchall()
    winLoss = cursor_winLoss.fetchall()

    # Fermeture des curseurs et des connexions aux bases de données
    cursor_liga.close()
    cursor_pl.close()
    cursor_urlPl.close()
    cursor_winLoss.close()
    connexion_liga.close()
    connexion_pl.close()
else:
    print("La base de données n'existe pas, veuillez exécuter les programmes DataBaseLiga.py et DataBasePl.py.")

# Définition du layout de l'application
app.layout = html.Div(
    children=[
        html.Div(id='page-content'),
        dcc.Location(id='url', refresh=True),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
        dcc.RadioItems(
            id='championship-button',
            options=[
                {'label': 'Premier League', 'value': 'PL'},
                {'label': 'Liga', 'value': 'Liga'}
            ],
            value='PL',
            labelStyle={'display': 'block'},
        ),
        html.H1(id='championship-title'),
        html.Div(
            dash_table.DataTable(
                id='match-table',
                columns=[
                    {'name': 'Matchs', 'id': 'match'},
                    {'name': 'Cotes', 'id': 'cote'},
                    {'name': 'Prono', 'id': 'prono', 'presentation': 'markdown'},
                ],
                data=[],
                style_table={'height': '900px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center'},
                style_data={'whiteSpace': 'normal'},
                markdown_options={'link_target': '_blank'},
            )
        ),
    ],
)

# Définition de la fonction de callback pour mettre à jour les informations sur les matchs
@callback(
    [Output('page-content', 'children'),
     Output('match-table', 'data'),
     Output('championship-title', 'children'),
     Output('championship-title', 'style'),
     Output('match-table', 'style_table'),
     Output('championship-button', 'style')],
    [Input('url', 'pathname'),
     Input('championship-button', 'value'),
     Input('match-table', 'data')],
)
def update_match_info(pathname, championship, match_info):
    if pathname is None or championship is None:
        raise PreventUpdate

    # Sélection du championnat et récupération des informations correspondantes
    if championship == 'Liga':
        matches = resultats_liga
        championnat_label = 'Match de Liga'
    elif championship == 'PL':
        matches = resultats_pl
        championnat_label = 'Match de Premier League'

    # Formatage des informations sur les matchs pour l'affichage dans le tableau
    match_info = [
        {
            'match': f"{match[1]} - {match[4]}",
            'cote': f"1:{match[2]} N:{match[3]} 2:{match[5]}",
            'prono': f'[Voir Prono](/prono/{championship}/{match[0]})',
        }
        for match in matches
    ]

    # Mise en forme spécifique si l'URL indique une page de pronostics
    if pathname.startswith(f'/prono'):
        # Séparation de la chaîne en fonction du caractère '/'
        parts = pathname.split('/')
        # Récupération des parties pertinentes
        if len(parts) >= 4:
            championship = parts[2]
            index_match = parts[3]
        if championship == 'Liga':
            matches = resultats_liga
            for i, match in enumerate(matches):
                if i >= int(index_match):
                    break
                team1 = match[1]
                team2 = match[4]
            layout2 = html.Div([
                dcc.Link('Voir le tableau des Matchs', href='/'),
                html.Div(f"MATCH", id='match', style={'position': 'absolute', 'top': '50px', 'left': '690px', 'font-size': '30px', 'width': '200px'}),
                html.Div(f"{team1}", id='team1', style={'position': 'absolute', 'top': '150px', 'left': '100px', 'font-size': '30px', 'width': '200px'}),
                html.Div(f"VS", id='VS', style={'position': 'absolute', 'top': '150px', 'left': '720px', 'font-size': '30px', 'width': '200px'}),
                html.Div(f"{team2}", id='team2', style={'position': 'absolute', 'top': '150px', 'left': '1200px', 'font-size': '30px', 'width': '200px'}),
            ])
        else:
            matches = resultats_pl
            for i, (match, url, win_loss) in enumerate(zip(matches, url_pl, winLoss)):
                if i >= int(index_match):
                    break
                team1 = match[1]
                team2 = match[4]
                url1 = url[1]
                url2 = url[2]
                win1 = win_loss[1]
                win2 = win_loss[2]
                print(win1)
            layout2 = html.Div([
                dcc.Link('Voir le tableau des Matchs', href='/'),
                html.Div(f"MATCH", id='match', style={'position': 'absolute', 'top': '50px', 'left': '690px', 'font-size': '30px', 'width': '200px'}),
                html.Div(f"{team1}", id='team1', style={'position': 'absolute', 'top': '150px', 'left': '100px', 'font-size': '30px', 'width': '200px'}),
                html.Div(f"VS", id='VS', style={'position': 'absolute', 'top': '150px', 'left': '720px', 'font-size': '30px', 'width': '200px'}),
                html.Div(f"{team2}", id='team2', style={'position': 'absolute', 'top': '150px', 'left': '1200px', 'font-size': '30px', 'width': '200px'}),
                html.Img(
                    src=str(url1),
                    style={'position': 'absolute', 'top': '135px', 'left': '300px'}
                ),
                html.Img(
                    src=str(url2),
                    style={'position': 'absolute', 'top': '135px', 'left': '1120px'}
                ),
                html.Div(children=generate_circle_series(win1), style={'position': 'absolute', 'top': '190px', 'left': '100px', 'font-size': '20px', 'width': '200px'}),
                html.Div(children=generate_circle_series(win2), style={'position': 'absolute', 'top': '190px', 'left': '1200px', 'font-size': '20px', 'width': '200px'}),
            ])
        return layout2, [], None, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    elif pathname == f'/':
        return [], match_info, championnat_label, {}, {}, {}
    else:
        return [], match_info, championnat_label, {}, {}, {}

# Fonction utilitaire pour créer un cercle coloré en fonction de la lettre
def create_circle(letter):
    color_mapping = {'W': 'green', 'D': 'orange', 'L': 'red'}
    return html.Span(
        style={'display': 'inline-block', 'width': '20px', 'height': '20px', 'border-radius': '60%', 'background-color': color_mapping.get(letter, 'black')}
    )

# Fonction utilitaire pour générer une série de cercles
def generate_circle_series(word):
    return [create_circle(letter) for letter in word]

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
