from telegram.ext import Updater, CommandHandler
from config.token import token

if __name__ == '__main__':
    updater = Updater(token, use_context = True)
    dispatcher = updater.dispatcher

    print('hola')
    # dispatcher.add_handler(CommandHandler('Link', listLink))
    # dispatcher.add_handler(CommandHandler('Banelco', listBanelco))

    # updater.start_polling()
    # updater.idle()