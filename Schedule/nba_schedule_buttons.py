from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
import os
from dotenv import load_dotenv
from Schedule.nba_schedule_request import today_schedule
from datetime import datetime, timedelta

load_dotenv()
nba_key = os.getenv("NBA_API_KEY")


class NBASchedule:
    @staticmethod
    async def handle_today_sch(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == '1':
            date = datetime.today()
            schedule_list = today_schedule(nba_key, date)
            game_info = "\n".join(schedule_list)

            # Add a button to go back to the 'nba' menu
            keyboard = [
                [
                    InlineKeyboardButton("Tomorrow Schedule", callback_data='tomorrow'),
                ],
                [
                    InlineKeyboardButton("Back to NBA Menu", callback_data='back'),
                ],
            ]
            back_to_nba_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(text=game_info, parse_mode="HTML", reply_markup=back_to_nba_markup)

    @staticmethod
    async def handle_tmro_sch(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == 'tomorrow':
            today_date = datetime.today()
            tomro_date = today_date + timedelta(days=1)
            tmro_list = today_schedule(nba_key, tomro_date)
            game_info = "\n".join(tmro_list)

            # Add a button to go back to the 'nba' menu
            keyboard = [
                [
                    InlineKeyboardButton("Yesterday Schedule", callback_data="1"),
                ],
                [
                    InlineKeyboardButton("Back to NBA Menu", callback_data='back'),
                ],
            ]
            back_to_nba_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(text=game_info, parse_mode="HTML", reply_markup=back_to_nba_markup)
