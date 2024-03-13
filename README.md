# PariSportif
Scripts Python pour la récupération et stockage de données de matchs de football.
Ce projet contient des scripts Python conçus pour récupérer des données de matchs de football à partir de sites web, les traiter et les stocker dans des bases de données SQLite distinctes pour les ligues "La Liga" et "Premier League". Il inclut également une interface Web construite avec Dash pour visualiser les données stockées.

1. Récupération des données
1.1. Recover_Data_PL.py et Recover_Data_Liga.py
Ces scripts utilisent les bibliothèques requests et BeautifulSoup pour extraire les informations de deux sites web différents (https://www.enligne.parionssport.fdj.fr/paris-football/angleterre/premier-league et https://www.enligne.parionssport.fdj.fr/paris-football/espagne/laliga).

Ils récupèrent les noms des équipes, les cotes pour les matchs nuls, et les cotes pour les équipes à domicile et à l'extérieur.

Les données sont renvoyées sous forme de dictionnaires.

2. Stockage des données
2.1. DataBasePL.py et DataBaseLiga.py
Ces scripts utilisent les données récupérées par les scripts de récupération pour les ligues "Premier League" et "La Liga".

Ils créent des tables dans des bases de données SQLite (Match_Pl.db et Match_Liga.db) avec les informations suivantes :

Table Matchs : Match (clé primaire), Équipe Domicile, Cotes Équipe Domicile, Cotes Nul, Équipe Extérieure, Cotes Équipe Extérieure.
Table WinLoss : Match (clé primaire), Statistiques Victoire/Défaite/Match Nul pour l'équipe à domicile, Statistiques Victoire/Défaite/Match Nul pour l'équipe à l'extérieur.
Table Url_Logo : Match (clé primaire), URL du logo de l'équipe à domicile, URL du logo de l'équipe à l'extérieur.

2.2. Interface Web (Dashboard.py)
L'interface Dash permet de visualiser les données stockées de manière interactive.
Elle affiche les matchs, les cotes et les pronostics sous forme de tableau.
Possibilité de filtrer les données par championnat (Premier League ou La Liga).
Affiche le titre du championnat sélectionné.
Liens pour voir les pronostics spécifiques à chaque match.

4. Instructions d'utilisation
Assurez-vous d'avoir les bibliothèques nécessaires installées (requests, beautifulsoup4, sqlite3, dash, dash_table, dash_bootstrap_components).

Exécutez les scripts dans l'ordre suivant :

DataBasePL.py et DataBaseLiga.py pour récupérer les données.
interfaceDash.py pour visualiser les données.

Les bases de données résultantes (Match_Pl.db et Match_Liga.db) seront créées avec les tables correspondantes.

Remarque
Les bases de données SQLite peuvent être consultées avec n'importe quel outil de gestion de base de données compatible SQLite.
