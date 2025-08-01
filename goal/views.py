import http.client
import json
from django.shortcuts import render # type: ignore
from django.core.cache import cache
from Football import config
from collections import defaultdict
from datetime import datetime
import pytz  # For timezone handling


def index(request):
    return render(request, "home.html")


def leagues(request):
    league_ids = [39,140,78,135,61,2,3,848,323,4]  # Example list of league IDs
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


def players(request):
    team_id = request.GET.get("team_id")
    cache_key = f"team_squad_{team_id}"
    data_json = cache.get(cache_key)

    if not data_json:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }
        conn.request("GET", f"/players/squads?team={team_id}", headers=headers)
        res = conn.getresponse()

        if res.status == 200:
            data = res.read()
            data_json = json.loads(data.decode("utf-8"))
            cache.set(cache_key, data_json, timeout=86400)
        else:
            # Log the error and show message
            print(f"Error: {res.status}")
            return render(request, "players.html", {"error": f"API request failed with status {res.status}"})
        conn.close()

    # Check if the response contains any players
    team_data = data_json.get("response", [])
    if not team_data:
        # No players found, return an error message
        return render(request, "players.html", {"error": "No players found for this team."})
    else:
        # Proceed if players exist
        team_data = team_data[0]  # Assuming first item in the list is the desired squad data
        return render(request, "players.html", {"team_data": team_data})


def fixture_details(request):
    fixture_id = request.GET.get("id")
    cache_key = f"fixtures_{fixture_id}"

    # Check if data is already cached
    data_json = cache.get(cache_key)
    if data_json:
        # If data is cached, retrieve it
        fixture_data = data_json.get("response", [])[0]  # Fetch the first response
    else:
        # If not cached, fetch from API
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": config.API_KEY,
        }
        conn.request("GET", f"/fixtures/?id={fixture_id}", headers=headers)
        res = conn.getresponse()

        if res.status == 200:
            data = res.read()
            data_json = json.loads(data.decode("utf-8"))
            fixture_data = data_json.get("response", [])[0]  # Fetch first response

            # Cache the fetched data for 24 hours (86400 seconds)
            cache.set(cache_key, data_json, timeout=86400)
        else:
            fixture_data = None

        conn.close()
        
    try:
        iso_date = fixture_data["fixture"]["date"]
        datetime_obj = datetime.fromisoformat(iso_date)
        ist_timezone = pytz.timezone("Asia/Kolkata")
        datetime_ist = datetime_obj.astimezone(ist_timezone)
        formatted_date = datetime_ist.strftime("%a, %B %d, %I:%M %p").lstrip("0")
        fixture_data["fixture"]["formatted_date"] = formatted_date
    except ValueError as e:
        print(f"Error parsing date: {e}")
        fixture_data["fixture"]["formatted_date"] = "Invalid date format"

    return render(request, "fixture_details.html", {"fixture": fixture_data})


def lineup(request):    
    return render(request, "lineup.html")

def events(request):
    return render(request, "events.html")

def fixture_stats(request):
    return render(request, "fixture_stats.html")

def player_profile(request):
    player_id = request.GET.get("id")  # This is the key fix
    cache_key = f"player_stats_{player_id}"
    data_json = cache.get(cache_key)

    if not data_json:
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': config.API_KEY  
        }
        conn.request("GET", f"/players/profiles?player={player_id}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_json = json.loads(data.decode("utf-8"))
        cache.set(cache_key, data_json, 60 * 60)  # Cache for 1 hour

    players_data = data_json.get('response', [])
    return render(request, "player_stats.html", {"players": players_data})