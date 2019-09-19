from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from config.token import token
from bot_handler.bot_handler import startBot, getLink, getBanelco, unknownCommand, inlineCommand

if __name__ == '__main__':
    updater = Updater(token, use_context = True)
    dispatcher = updater.dispatcher
    print("Bot started")

    dispatcher.add_handler(CommandHandler('start', startBot))
    dispatcher.add_handler(CommandHandler('link', getLink))
    dispatcher.add_handler(CommandHandler('banelco', getBanelco))
    dispatcher.add_handler(InlineQueryHandler(inlineCommand))
    dispatcher.add_handler(MessageHandler(Filters.command, unknownCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, unknownCommand))

    updater.start_polling()
    updater.idle()