from config import TOKEN

from telegram import Update, InlineQueryResultPhoto
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(bot, update) -> None:
    """Handle the inline query."""
    query = bot.inline_query.query

    if query == "":
        return

    print(query)
    # user_id = bot.inline_query.from_user.id
    # image_dict = text_sender.send_data(query, size=True, user_id=user_id)
    # results = [
    #         InlineQueryResultPhoto(
    #             id=str(uuid4()),
    #             photo_url=image_dict['paths'][idx],
    #             thumb_url=image_dict['paths'][idx],
    #             photo_width=image_dict['width'][idx],
    #             photo_height=image_dict['height'][idx],
    #         )
    #         for idx in range(len(image_dict['paths']))
    # ]
    # bot.inline_query.answer(results)



def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(InlineQueryHandler(inlinequery, run_async=True))

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