# API FOR SPORTS RADAR, THIS IS HOW YOU COULD MAKE IT WORK
# PROBLEM IS THEY HAVE NO GOOD ROUTES FOR API TO GO FROM PLAYER TO STATS
# NEED TO CALL SCHEDULE THEN TEAM THEN PLAYER THEN ID THEN PROFILE THEN STATS


#def nba_stats(api):
#     # Define the API endpoint URL
#     endpoint_url = "https://api.sportradar.us/nba/trial/v8/en/seasons/2023/REG/leaders.json"
#     # Define the parameters for the API request
#     params = {
#         "api_key": api
#     }
#
#     # Make the API request
#     response = requests.get(endpoint_url, params=params)
#
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#
#         # Extract the top players based on minutes played
#         points_category = next(category for category in data['categories'] if
#                                category['name'] == 'points' and category['type'] == 'average')
#         top_players = points_category['ranks'][:100]
#
#         # Print the top players
#         for player_data in top_players:
#             ##Player Info
#             player_rank = player_data['rank']
#             player_name = player_data['player']['full_name']
#             player_fname = player_data['player']['first_name']
#             player_lname = player_data['player']['last_name']
#             player_jersey = player_data['player']['jersey_number']
#             player_ref = player_data['player']['reference']
#
#             ##Team info
#             team_market = player_data['teams'][0]['market']
#             team_name = player_data['teams'][0]['name']
#
#             ##Stats Average
#             player_ppg = player_data['average']['points']
#             player_apg = player_data['average']['assists']
#             player_rpg = player_data['average']['rebounds']
#             player_spg = player_data['average']['steals']
#             player_bpg = player_data['average']['blocks']
#
#             # Create an InlineQueryResultArticle object
#             return (
#                 f"Player: {player_name} (No.{player_jersey})\n"
#                 f"Team: {team_market} {team_name}\n"
#                 f"{player_ppg} points per game\n"
#                 f"{player_apg} assist per game\n"
#                 f"{player_rpg} rebounds per game\n"
#                 f"{player_spg} steals per game\n"
#                 f"{player_bpg} blocks per game\n")



# async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.inline_query.query
#
#     page = int(context.args[0]) if context.args else 1  # Get page number from arguments if provided
#
#     # Pass an empty string as query if no query is provided
#     stats_list = inline_player_list(page=page, query=query.lower() if query else "")
#
#     await update.inline_query.answer(stats_list, cache_time=0)

# def inline_player_list(page=1, query=None):
#     player_info = players.get_active_players()
#
#     headshot_url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/"
#     stats_list = []
#
#     players_per_page = 5
#     start_index = (page - 1) * players_per_page
#     end_index = start_index + players_per_page
#
#     filtered_players = list(
#         filter(lambda player: query.lower() in player['full_name'].lower(), player_info)) if query else player_info
#
#     for player in filtered_players[start_index:end_index]:
#         player_id = player['id']
#         player_name = player['full_name']
#
#         result_article = InlineQueryResultArticle(
#             thumbnail_url=f"{headshot_url}{player_id}.png",
#             thumbnail_width=32,
#             thumbnail_height=32,
#             id=player_id,
#             title=player_name,
#             input_message_content=InputTextMessageContent(get_player_stats(player_id),parse_mode="HTML"))
#
#         stats_list.append(result_article)
#
#     return stats_list