from config import TOKEN
from uuid import uuid4


from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          ConversationHandler)

from telegram import Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext

from libs.clip_new import ClipEmbedding

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

    recommend_film = clip.get_recommend(bot.message.text)
    head_text = '<b><i>5 Movies You Have to Watch:</i></b>\n\n'

    body_text = '\n'.join(['<b>' + str(idx + 1) + '</b>'
                '<b>'
                    '<a href="https://www.youtube.com/watch?v=' + row['youtubeId'] + '" > ' + row['title'] + '</a>'
                '</b>'
                for idx, row in recommend_film.iterrows()])

    footer = '\n\nThis representation may not be optimal because the dataset has only a base of 1000 films.'

    bot.message.reply_text(head_text + body_text + footer, parse_mode='HTML')
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