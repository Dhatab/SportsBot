from typing import Any, Coroutine

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import ContextTypes, CallbackContext, InlineQueryHandler, ChosenInlineResultHandler
import os, time
from dotenv import load_dotenv
from Schedule.nba_schedule_request import today_schedule
from Schedule.nba_schedule_buttons import NBASchedule
from Schedule.nba_standings_request import today_standings
from Schedule.nba_stats_request import inline_player_list, get_player_stats

load_dotenv()
nba_key = os.getenv("NBA_API_KEY")
keyboard = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message on `/start`."""
    global keyboard
    keyboard = [
        [
            InlineKeyboardButton("Box Scores", callback_data='0'),
            InlineKeyboardButton("Schedule", callback_data="1"),
        ],
        [
            InlineKeyboardButton("Standings", callback_data="2"),
            InlineKeyboardButton("Stats", callback_data="3"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == '0':
        nba_keyboard = [
            [InlineKeyboardButton("Back", callback_data='back')]
        ]
        nba_reply_markup = InlineKeyboardMarkup(nba_keyboard)
        # Edit the message with the new inline keyboard
        await query.edit_message_reply_markup(reply_markup=nba_reply_markup)

    elif query.data == '1':
        # Handle the '1' callback data using NBAHandler
        await NBASchedule.handle_today_sch(update, context)

    elif query.data == '2':
        standing_list = today_standings(nba_key)
        game_info = "\n".join(standing_list)
        await query.edit_message_text(text=game_info, parse_mode="HTML")  # Assuming nba_key is defined elsewhere
        await query.message.reply_text('Please choose:', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == '3':
        await query.edit_message_text('Please open the menu and select the /stats command.'
                                      '\nIn the message bar begin typing the first or last name of any player.'
                                      '\n Also know this process works in group chats if you just message '
                                      '@MrSports_bot')
        await query.message.reply_text('Please choose:', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'tomorrow':
        await NBASchedule.handle_tmro_sch(update, context)

    elif query.data == 'back':
        await back_button(update, context)


async def back_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text('Please choose:', reply_markup=reply_markup)


async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, ) -> None:
    query = update.inline_query.query

    page = int(context.args[0]) if context.args else 1  # Get page number from arguments if provided

    # Pass an empty string as query if no query is provided
    stats_list = inline_player_list(page=page, query=query.lower() if query else "")

    await update.inline_query.answer(stats_list, cache_time=0)


async def on_result_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.to_dict())
    result = update.chosen_inline_result
    result_id = result.result_id
    user = result.from_user.id
    # await context.bot.send_message(chat_id=user,text=get_player_stats(result_id), parse_mode="HTML")
