import requests
import os
import sys
import json
# import schedule
# import time
# import locale


def get_ranking(league):
    """
    Utilisation de l'api http://api.football-data.org/
    pour récupérer le classement d'un championnat
    """
    ranking = {}
    url = "http://api.football-data.org/v1/soccerseasons/" + str(league) + "/leagueTable"
    api_key = "09fe2c72430f482d8a40307334ca6147"
    headers = {'X-Auth-Token': api_key}

    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:    # This is the correct syntax
        print(e)
        sys.exit(1)

    json_file = r.json()
    i = 0

    for team in json_file['standing']:
        ranking[i] = {
            'position': team['position'],
            'team': team['teamName'],
            'playedGames': team['playedGames'],
            'points': team['points']
        }
        i += 1

    # enregistrement dans un fichier
    f = os.path.join(os.path.dirname(__file__), 'json/ranking_ligue1.json')
    with open(f, 'w') as outfile:
        json.dump(ranking, outfile)


def get_last_next_match(team):
    """
    Utilisation de l'api http://api.football-data.org/
    pour récupérer le dernier résultat d'une équipe
    et le prochain match
    """
    last_result = {}
    next_match = {}
    data = {}
    url = "http://api.football-data.org/v1/teams/" + str(team) + "/fixtures"
    api_key = "09fe2c72430f482d8a40307334ca6147"
    headers = {'X-Auth-Token': api_key}

    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:    # This is the correct syntax
        print(e)
        sys.exit(1)

    json_file = r.json()
    i = 0

    for match in json_file['fixtures']:
        if match['status'] == "FINISHED":
            i += 1
        else:
            break

    # dernier match joué
    json_last_result = json_file['fixtures'][i-1]

    last_result['date'] = json_last_result['date']
    last_result['homeTeam'] = {
        'name': json_last_result['homeTeamName'],
        'img': get_infos_team(json_last_result['_links']['homeTeam']['href'])['img']
    }
    last_result['awayTeam'] = {
        'name': json_last_result['awayTeamName'],
        'img': get_infos_team(json_last_result['_links']['awayTeam']['href'])['img']
    }
    last_result['result'] = json_last_result['result']
    last_result['matchday'] = json_last_result['matchday']

    # prochain match
    json_next_match = json_file['fixtures'][i]

    next_match['date'] = json_next_match['date']
    next_match['homeTeam'] = {
        'name': json_next_match['homeTeamName'],
        'img': get_infos_team(json_next_match['_links']['homeTeam']['href'])['img']
    }
    next_match['awayTeam'] = {
        'name': json_next_match['awayTeamName'],
        'img': get_infos_team(json_next_match['_links']['awayTeam']['href'])['img']
    }
    next_match['matchday'] = json_next_match['matchday']

    data['last_result'] = last_result;
    data['next_match'] = next_match

    # enregistrement dans un fichier
    f = os.path.join(os.path.dirname(__file__), 'json/last_next_match.json')
    with open(f, 'w') as outfile:
        json.dump(data, outfile)


def get_infos_team(url):
    """
    Utilisation de l'api http://api.football-data.org/
    pour récupérer le prochain match d'une équipe
    """
    infos = {}
    api_key = "09fe2c72430f482d8a40307334ca6147"
    headers = {'X-Auth-Token': api_key}

    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:    # This is the correct syntax
        print(e)
        sys.exit(1)

    json_file = r.json()

    infos['name'] = json_file['name']
    infos['shortName'] = json_file['shortName']
    infos['squadMarketValue'] = json_file['squadMarketValue']
    infos['img'] = json_file['crestUrl']

    return infos

get_ranking(396)
get_last_next_match(529)

# # récupérer classement apres chaque matchs de ligue 1
# schedule.every().friday.at("23:00").do(get_ranking, 396)
# schedule.every().saturday.at("19:30").do(get_ranking, 396)
# schedule.every().saturday.at("23:00").do(get_ranking, 396)
# schedule.every().sunday.at("16:00").do(get_ranking, 396)
# schedule.every().sunday.at("19:00").do(get_ranking, 396)
# schedule.every().sunday.at("23:00").do(get_ranking, 396)
#
# # récupérer les matchs
# schedule.every().friday.at("23:00").do(get_last_next_match, 529)
# schedule.every().saturday.at("19:30").do(get_last_next_match, 529)
# schedule.every().saturday.at("23:00").do(get_last_next_match, 529)
# schedule.every().sunday.at("16:00").do(get_last_next_match, 529)
# schedule.every().sunday.at("19:00").do(get_last_next_match, 529)
# schedule.every().sunday.at("23:00").do(get_last_next_match, 529)
#
# schedule.every().thursday.at("22:18").do(get_last_next_match, 529)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
