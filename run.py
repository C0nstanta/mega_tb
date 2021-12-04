from config import TOKEN
from uuid import uuid4


from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          ConversationHandler)

from telegram import Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext

from libs.clip import ClipEmbedding, SentenceTransformer

SEARCHER = range(1)

clip = ClipEmbedding()

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(bot: Update, context: CallbackContext) -> None:
    bot.message.reply_text(f"Hey!\n"
                           f"You just need to enter some keywords\n"
                           f"and our system will advise you the most suitable content.\n"
                           f"\n"
                           f"Enter your request, please.")
    return SEARCHER


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def searcher(bot: Update, context: CallbackContext):
    print(bot.message.text)
    bot.message.reply_text(f"We advise you to watch the movie: any-{bot.message.text}")

    return SEARCHER


def main() -> None:

    rs_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^/start$'), start)],
        states={
            SEARCHER: [MessageHandler(Filters.text & ~(Filters.command), searcher)
            ]

        },
        fallbacks=[]
    )

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(rs_handler)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(
    #     listen='0.0.0.0',
    #     port=PORT,
    #     url_path=TOKEN,
    #     webhook_url=f'https://62.141.41.190:8443/{TOKEN}',
    #     key='private.key',
    #     cert='cert.pem')


    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()