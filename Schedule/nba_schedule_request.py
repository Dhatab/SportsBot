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
schedule_list = []
standing_list = []


def today_schedule(api, date):
    global schedule_list
    schedule_list.clear()

    # Get today's date
    today_date = date.strftime("%Y/%m/%d")
    frmt_date = date.strftime("%m/%d/%Y")

    # Construct the API request URL for today's NBA games
    connection = http.client.HTTPSConnection("api.sportradar.us")
    base_url = f"/nba/trial/v8/en/games/{today_date}/schedule.json?api_key={nba_key}"

    # Send request
    connection.request("GET", base_url)
    response = connection.getresponse()

    # Process the API response (parse JSON data)
    if response.status == 200:
        schedule_list.append(f"<b>Games Scheduled For {frmt_date}:</b>")
        data = json.loads(response.read().decode('utf-8'))
        # Extract and display information about the scheduled NBA games for tonight
        for game in data["games"]:
            scheduled_datetime_str = game['scheduled']

            # Convert scheduled datetime string to Eastern Time (ET)
            utc_datetime = datetime.strptime(scheduled_datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            eastern_tz = pytz.timezone('US/Eastern')
            eastern_dt = utc_datetime.replace(tzinfo=pytz.utc).astimezone(eastern_tz)
            frmt_schedule = eastern_dt.strftime("%I:%M %p %Z")
            schedule_list.append(
                f"{game['home']['name']} vs {game['away']['name']} \n{game['venue']['name']} \n{frmt_schedule}\n")
    else:
        print("Failed to fetch NBA games data.")

    return schedule_list  # Return the list of formatted game information



