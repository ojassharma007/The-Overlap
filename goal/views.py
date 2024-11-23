import http.client
import json
from django.shortcuts import render # type: ignore
from django.core.cache import cache
from Football import config
from collections import defaultdict


def index(request):
    return render(request, "home.html")


def leagues(request):
    league_ids = [39,140,78,135,61,2,3,848,323]  # Example list of league IDs
    cache_key = "all_leagues_data"
    all_leagues_data = cache.get(cache_key)

    if not all_leagues_data:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }
        all_leagues_data = []
        for league_id in league_ids:
            try:
                conn.request("GET", f"/leagues?id={league_id}", headers=headers)
                res = conn.getresponse()
                if res.status == 200:
                    data = res.read()
                    data_json = json.loads(data.decode("utf-8"))
                    leagues_data = data_json.get("response", [])
                    all_leagues_data.extend(leagues_data)
                else:
                    print(f"Error: {res.status}")
            except Exception as e:
                print(f"Exception occurred: {e}")

        conn.close()
        cache.set(cache_key, all_leagues_data, timeout=86400)  # Cache for 24 hours

    return render(request, "leagues.html", {"leagues": all_leagues_data})


def fixtures(request):
    fixture_id = request.GET.get("id")
    cache_key = f"fixtures_{fixture_id}"
    data_json = cache.get(cache_key)

    if not data_json:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }

        conn.request(
            "GET", f"/fixtures?league={fixture_id}&season=2024", headers=headers
        )
        res = conn.getresponse()
        if res.status == 200:
            data = res.read()
            data_json = json.loads(data.decode("utf-8"))  # Parse JSON response data
        else:
            print(f"Error: {res.status}")
        conn.close()
        cache.set(cache_key, data_json, timeout=86400)  # Cache for 24 hours
        

    return render(request, "fixtures.html", {"data": data_json})


def standings(request):
    standings_id = request.GET.get("id")
    cache_key = f"standings_{standings_id}"
    data_json = cache.get(cache_key)

    if not data_json:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }

        conn.request(
            "GET", f"/standings?league={standings_id}&season=2024", headers=headers
        )
        res = conn.getresponse()
        if res.status == 200:
            data = res.read()
            data_json = json.loads(data.decode("utf-8"))  # Parse JSON response data
        else:
            print(f"Error: {res.status}")
        conn.close()
        cache.set(cache_key, data_json, timeout=86400)  # Cache for 24 hours

    standings_data = data_json.get("response", [])
    return render(request, "standings.html", {"standings": standings_data})


def teams(request):
    league_id = request.GET.get("id")
    cache_key = f"teams_{league_id}"
    data_json = cache.get(cache_key)

    if not data_json:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }

        conn.request("GET", f"/teams?league={league_id}&season=2024", headers=headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read()
            data_json = json.loads(data.decode("utf-8"))  # Parse JSON response data
            cache.set(cache_key, data_json, timeout=86400)  # Cache for 24 hours
        else:
            print(f"Error: {res.status}")
            data_json = {"response": []}  # Handle API error gracefully
        conn.close()

    teams_data = data_json.get("response", [])
    return render(request, "teams.html", {"data": teams_data, "league_id" : league_id})


def all_leagues(request):
    league_id = request.GET.get("id")
    cache_key = f"teams_{league_id}"
    data_json = cache.get(cache_key)

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": config.API_KEY,
    }

    # Requesting current leagues
    conn.request("GET", "/leagues", headers=headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read()
        data_json = json.loads(data.decode("utf-8"))  # Parse JSON response data
        cache.set(cache_key, data_json, timeout=86400)  # Cache for 24 hours
    else:
        print(f"Error: {res.status}")
        data_json = {"response": []}  # Handle API error gracefully
    conn.close()

    # Extracting the leagues data from the response
    leagues_data = data_json.get("response", [])

    # Passing the leagues data to the template
    return render(request, "alleagues.html", {"leagues": leagues_data})


def stats(request):
    team_id = request.GET.get("team_id")
    league_id = request.GET.get("league_id")
    cache_key = f"stats_{team_id}_{league_id}"
    data_json = cache.get(cache_key)

    if not data_json:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }

        conn.request(
            "GET",
            f"/teams/statistics?season=2024&team={team_id}&league={league_id}",
            headers=headers,
        )
        res = conn.getresponse()
        if res.status == 200:
            data = res.read()
            data_json = json.loads(data.decode("utf-8"))  # Parse JSON response data
            cache.set(cache_key, data_json, timeout=86400)  # Cache for 24 hours

        else:
            print(f"Error: {res.status}")
            data_json = {"response": {}}  # Handle API error gracefully
        conn.close()

    stats_data = data_json.get("response", {})
    return render(request, "stats.html", {"stats": stats_data})

def live_fixtures(request):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': config.API_KEY  
    }
    conn.request("GET", "/fixtures?live=all", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))
    
    fixtures_data = data_json.get('response', [])
    
    return render(request, 'live_fixtures.html', {'fixtures': fixtures_data})
