from telegram import ReplyKeyboardMarkup

def startBot(update, context):
    keyboard = [['Link'], ['Banelco']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard = True, resize_keyboard = True)
    context.bot.send_message(
        chat_id = update.message.chat_id, 
        text = "Hi! Are you looking for /banelco or /link?",
        reply_markup=reply_markup).wait()

def getLink(update, context):
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "eligio link"
    )

def getBanelco(update, context):
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "eligio link"
    )

def unknownCommand(update, context):
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "use /link or /banelco"
    )

def inlineCommand(update, context):
    context.bot.answer_inline_query(
        chat_id = update.inline_query.id,
        text = "eligio link"
    )