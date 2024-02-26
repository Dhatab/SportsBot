from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResult
import requests
import os, json
from dotenv import load_dotenv
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

# Load environment variables from .env file
load_dotenv()

# Access for telegram Bot
nba_key = os.getenv("NBA_API_KEY")


def inline_player_list(page=1, query=None):
    player_info = players.get_active_players()

    headshot_url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"
    stats_list = []

    players_per_page = 5
    start_index = (page - 1) * players_per_page
    end_index = start_index + players_per_page

    filtered_players = list(
        filter(lambda player: query.lower() in player['full_name'].lower(), player_info)) if query else player_info

    for player in filtered_players[start_index:end_index]:
        player_id = player['id']
        player_name = player['full_name']

        result_article = InlineQueryResultArticle(
            thumbnail_url=f"{headshot_url}{player_id}.png",
            thumbnail_width=32,
            thumbnail_height=32,
            id=player_id,
            title=player_name,
            input_message_content=InputTextMessageContent(get_player_stats(player_id), parse_mode="HTML"))

        stats_list.append(result_article)

    return stats_list


def get_player_stats(player_id):
    player = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_json = player.get_dict()

    # Extract Player info and stats
    player_common_info = player_info_json["resultSets"][0]["rowSet"][0]
    player_headline_stats = player_info_json["resultSets"][1]["rowSet"][0]

    # Extract PTS, AST, and REB
    full_name = player_common_info[3]  # Index 3 corresponds to PTS in the rowSet
    jersey = player_common_info[14]  # Index 4 corresponds to AST in the rowSet
    position = player_common_info[15]  # Index 5 corresponds to REB in the rowSet
    team_name = player_common_info[19]  # Index 5 corresponds to REB in the rowSet

    # Extract PTS, AST, and REB
    pts = player_headline_stats[3]  # Index 3 corresponds to PTS in the rowSet
    ast = player_headline_stats[4]  # Index 4 corresponds to AST in the rowSet
    reb = player_headline_stats[5]  # Index 5 corresponds to REB in the rowSet

    text = (f"{full_name} (#{jersey})\n"
            f"Position: {position}\n"
            f"Team: {team_name}\n"
            f"\n"
            f"<b>2023-24 Stats:</b>\n"
            f"PTS: {pts}, AST: {ast}, REB: {reb}")

    return text
