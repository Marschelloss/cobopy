import requests
from logzero import logger

telegram_base_url = 'https://api.telegram.org/bot'


def send_message(bot_id, bot_token, chat_id, msg):
    api_url = "%s%s:%s/sendMessage" % (telegram_base_url, bot_id, bot_token)
    params = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'MarkdownV2'}
    try:
        resp = requests.get(api_url, params=params)
        if resp.status_code == 200:
            logger.debug("Successfully sent message to telegram: %s" % resp.content)
        else:
            logger.error("Error while sending telegram message: %s" % resp.content)
    except Exception as e:
        logger.error("Error while sending telegram message: %s" % e)


def send_photo(bot_id, bot_token, chat_id, photo, caption):
    api_url = "%s%s:%s/sendPhoto" % (telegram_base_url, bot_id, bot_token)
    params = {
        'chat_id': chat_id,
        'photo': photo,
        'caption': caption,
        'parse_mode': 'MarkdownV2'
    }
    return requests.get(api_url, params=params)

