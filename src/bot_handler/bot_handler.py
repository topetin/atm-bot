from telegram import ReplyKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, KeyboardButton
from services.atm_service.atm_service import findAtms
from utils.element_formatter import formatPhotoUrl, formatAtmName
from data_handler.data_handler import saveAtmData
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
    updateContextUserData(context, latitude, longitude, atm_value)
    atmTypeFormatted = formatAtmName(atm_value)
    atmData = findAtms(atmTypeFormatted, latitude, longitude)
    sendAtmsToUser(update, context, atmData, latitude, longitude)


def checkLocation(update, context):
    atm_value = copy.copy(update.message.text)
    if 'latitude' in context.user_data and 'longitude' in context.user_data:
        latitude = copy.copy(context.user_data.get('latitude'))
        longitude = copy.copy(context.user_data.get('longitude'))
        updateContextUserData(context, latitude, longitude, atm_value)
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
    atm_value = copy.copy(context.user_data.get('atm'))
    latitude = copy.copy(context.user_data.get('latitude'))
    longitude = copy.copy(context.user_data.get('longitude'))
    atmTypeFormatted = formatAtmName(atm_value)
    atmData = findAtms(atmTypeFormatted, latitude, longitude)
    sendAtmsToUser(update, context, atmData, latitude, longitude)


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


def sendAtmsToUser(update, context, atmData, userLat, userLon):
    if len(atmData) == 0:
        return context.bot.send_message(
            chat_id = update.message.chat_id,
            text = "No encontramos cajeros cerca tuyo"
        )
    photoUrl = formatPhotoUrl(userLat, userLon, atmData)
    for atm in atmData:
        index = atmData.index(atm)
        saveAtmData(atm.get('red'), atm.get('id'), index)
        msg = f"{index+1}. Banco: {atm.get('banco')}. Direccion: {atm.get('ubicacion')}"
        context.bot.send_message(
            chat_id = update.message.chat_id,
            text = msg
        )
    context.bot.send_photo(
        chat_id = update.message.chat_id,
        photo = photoUrl
    )


def loadAtms(pattern):
    result = []
    pattern = re.escape(pattern)
    for atm in inlineResults():
        if re.match(pattern, atm.title, re.IGNORECASE) is not None:
            result.append(atm)
    return result


def inlineResults():
    return [InlineQueryResultArticle(id = 1, title = "Link", input_message_content = InputTextMessageContent("/link")), 
    InlineQueryResultArticle(id = 2, title = "Banelco", input_message_content = InputTextMessageContent("/banelco"))]


def updateContextUserData(context, latitude, longitude, atm_value):
    context.user_data.clear()
    context.user_data['atm'] = atm_value
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude