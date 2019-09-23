from telegram import ReplyKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, KeyboardButton
from services.atms.atm_service import getAtmData 
import re
import copy

def startBot(update, context):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("/link")], [KeyboardButton("/banelco")]], resize_keyboard = True)
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "Hola! Que tipo de cajero estas buscando?",
        reply_markup = reply_markup).wait()

def onLocation(update, context):
    atm_value = copy.copy(context.user_data.get('atm'))
    longitude = update.message.location.longitude
    latitude = update.message.location.latitude
    context.user_data.clear()
    context.user_data['atm'] = atm_value
    context.user_data['longitude'] = longitude
    context.user_data['latitude'] = latitude

    atmType = copy.copy(atm_value)
    atmTypeFormatted = atmType[1:].upper()
    atmData = getAtmData(atmTypeFormatted, -34.5606129, -58.4662056, 0.5, 3)
    print('buscar atm', context.user_data)

def checkLocation(update, context):
    atm_value = copy.copy(update.message.text)
    if 'latitude' in context.user_data and 'longitude' in context.user_data:
        latitude = copy.copy(context.user_data.get('latitude'))
        longitude = copy.copy(context.user_data.get('longitude'))
        context.user_data.clear()
        context.user_data['atm'] = atm_value
        context.user_data['latitude'] = latitude
        context.user_data['longitude'] = longitude
        return askNewLocation(update, context)
    getLocation(update, context, atm_value)

def askNewLocation(update, context):
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Mantener ubicacion")], [KeyboardButton("Cambiar ubicacion")]], one_time_keyboard = True, resize_keyboard = True)
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "Seguis aca?"
    )
    context.bot.send_location(
        chat_id = update.message.chat_id,
        latitude = context.user_data.get('latitude'),
        longitude = context.user_data.get('longitude'),
        reply_markup = reply_markup).wait()

def getLocation (update, context, atm_value):
    context.user_data.clear()
    context.user_data['atm'] = atm_value
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Compartir ubicacion", request_location = True)]], one_time_keyboard = True, resize_keyboard = True)
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "Donde estas?",
        reply_markup = reply_markup).wait()

def keepLocation(update, context):
    print('buscar atm', context.user_data)

def changeLocation(update, context):
    getLocation(update, context, context.user_data.get('atm'))

def unknownCommand(update, context):
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text = "Usa los comandos /link o /banelco para encontrar el cajero mas cercano"
    )

def getInlineCommand(update, context):
    query = update.inline_query.query
    update.inline_query.answer(loadAtms(query))

def loadAtms(pattern):
    result = []
    pattern = re.escape(pattern)
    for atm in inlineResults():
        if re.match(pattern, atm.title, re.IGNORECASE) is not None:
            result.append(atm)
    return result

def inlineResults():
    return [
        InlineQueryResultArticle(
            id = 1,
            title = "Link",
            input_message_content = InputTextMessageContent("/link")),
        InlineQueryResultArticle(
            id = 2,
            title = "Banelco",
            input_message_content = InputTextMessageContent("/banelco"))]