from telegram import ForceReply, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, InlineQueryHandler, ChosenInlineResultHandler
import os
from handlers import start, button, inline_query_handler, on_result_chosen
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Access for telegram Bot
bot = os.getenv("TELEGRAM_BOT_TOKEN")


# Starts the BOT
def main() -> None:
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot).build()

    # How to handle each command
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", start))
    application.add_handler(InlineQueryHandler(inline_query_handler))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(ChosenInlineResultHandler(on_result_chosen))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
