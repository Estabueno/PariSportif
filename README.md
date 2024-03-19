# PariSportif

Ce projet comprend des scripts Python conçus pour récupérer et stocker des données de matchs de football, ainsi qu'une interface Web pour visualiser ces données. 

## 1. Récupération des données

### 1.1. Scripts de récupération de données
- **Recover_Data_PL.py** et **Recover_Data_Liga.py** : Ces scripts utilisent les bibliothèques requests et BeautifulSoup pour extraire les informations de deux sites web différents : 
    - [Premier League](https://www.enligne.parionssport.fdj.fr/paris-football/angleterre/premier-league)
    - [La Liga](https://www.enligne.parionssport.fdj.fr/paris-football/espagne/laliga)
    
    Les données extraites incluent les noms des équipes, les cotes pour les matchs nuls, et les cotes pour les équipes à domicile et à l'extérieur. Les données sont renvoyées sous forme de dictionnaires.

## 2. Stockage des données

### 2.1. Scripts de stockage de données
- **DataBasePL.py** et **DataBaseLiga.py** : Ces scripts utilisent les données récupérées par les scripts de récupération pour les ligues "Premier League" et "La Liga". Ils créent des tables dans des bases de données SQLite (**Match_Pl.db** et **Match_Liga.db**) avec les informations suivantes :
    - **Table Matchs** : Match (clé primaire), Équipe Domicile, Cotes Équipe Domicile, Cotes Nul, Équipe Extérieure, Cotes Équipe Extérieure.
    - **Table WinLoss** : Match (clé primaire), Statistiques Victoire/Défaite/Match Nul pour l'équipe à domicile, Statistiques Victoire/Défaite/Match Nul pour l'équipe à l'extérieur.
    - **Table Url_Logo** : Match (clé primaire), URL du logo de l'équipe à domicile, URL du logo de l'équipe à l'extérieur.

## 3. Interface Web

### 3.1. Dashboard
Le fichier **Dashboard.py** contient une interface Dash permettant de visualiser les données stockées de manière interactive. Elle affiche les matchs, les cotes et les pronostics sous forme de tableau. Cette interface offre la possibilité de filtrer les données par championnat (Premier League ou La Liga) et affiche le titre du championnat sélectionné. De plus, des liens sont fournis pour voir les pronostics spécifiques à chaque match.

## 4. Instructions d'utilisation

Pour utiliser ce projet, suivez ces étapes :
1. Exécutez les scripts **DataBasePL.py** et **DataBaseLiga.py** pour récupérer les données et les stocker dans les bases de données correspondantes (**Match_Pl.db** et **Match_Liga.db**).
2. Exécutez le script **Dashboard.py** pour visualiser les données à l'aide de l'interface Dash.
