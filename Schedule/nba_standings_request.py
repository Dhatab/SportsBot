import http.client
import json
import os
import pytz
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone

# Load environment variables from .env file
load_dotenv()

# Access for telegram Bot
nba_key = os.getenv("NBA_API_KEY")
standing_list = []


def today_standings(api):
    global standing_list
    standing_list.clear()

    current_year = str(datetime.now().year - 1)

    # Construct the API request URL for today's NBA games
    connection = http.client.HTTPSConnection("api.sportradar.us")
    base_url = f"/nba/trial/v8/en/seasons/{current_year}/REG/rankings.json?api_key={nba_key}"

    # Send request
    connection.request("GET", base_url)
    response = connection.getresponse()

    # Process the API response (parse JSON data)
    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        # Extract and display information about each team in each conference
        for conf in data["conferences"]:
            conference_name = conf['name']
            standing_list.append(f"\n<b>{conference_name}:</b>")

            # Separate teams into Western and Eastern conferences
            western_teams = []
            eastern_teams = []

            for div in conf['divisions']:
                for team in div['teams']:
                    team_name = team['name']
                    conference_ranking = team['rank']['conference']

                    # Organize teams by conference
                    if conference_name == "WESTERN CONFERENCE":
                        western_teams.append((team_name, conference_ranking))
                    elif conference_name == "EASTERN CONFERENCE":
                        eastern_teams.append((team_name, conference_ranking))

            # Sort teams within each conference by ranking
            western_teams.sort(key=lambda x: x[1])
            eastern_teams.sort(key=lambda x: x[1])

            # Append sorted teams to the standing_list
            for team_name, conference_ranking in western_teams:
                standing_list.append(f"{conference_ranking}. {team_name} ")
            for team_name, conference_ranking in eastern_teams:
                standing_list.append(f"{conference_ranking}.  {team_name}")

            # today_list.append(f"{game['home']['name']} vs {game['away']['name']} \n{game['venue']['name']} \n{frmt_schedule}")
    else:
        print("Failed to fetch NBA games data.")

    return standing_list  # Return the list of formatted game information


