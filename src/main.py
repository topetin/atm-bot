from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from config.token import botToken
from bot_handler.bot_handler import startBot, unknownCommand, getInlineCommand, onLocation, checkLocation, keepLocation, changeLocation


if __name__ == '__main__':
    updater = Updater(botToken, use_context = True)
    dispatcher = updater.dispatcher
    print("Bot started")

    dispatcher.add_handler(CommandHandler('start', startBot))
    dispatcher.add_handler(CommandHandler('link', checkLocation))
    dispatcher.add_handler(CommandHandler('banelco', checkLocation))
    dispatcher.add_handler(InlineQueryHandler(getInlineCommand))
    dispatcher.add_handler(MessageHandler(Filters.command, unknownCommand))
    dispatcher.add_handler(MessageHandler(Filters.regex('Mantener ubicacion'), keepLocation))
    dispatcher.add_handler(MessageHandler(Filters.regex('Cambiar ubicacion'), changeLocation))
    dispatcher.add_handler(MessageHandler(Filters.text, unknownCommand))
    dispatcher.add_handler(MessageHandler(Filters.location, onLocation))

    updater.start_polling()
    updater.idle()