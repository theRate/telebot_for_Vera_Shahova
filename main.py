import requests
import telebot
from datetime import datetime
from config import TOKEN, ADMIN_CHAT_ID, CHANNEL_ID

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    message_text = f'Привет, {message.from_user.first_name},' \
                   f'осталось сделать последний шаг, чтобы забрать мой авторский гайд «Искусство проявления себя».' \
                   f'\n\nПодпишись на мой канал, там ты найдёшь упражнения для красивого голоса и грамотной речи,' \
                   f'прямые эфиры и много другой полезной информации.'

    mark = telebot.types.InlineKeyboardMarkup()
    mark.add(telebot.types.InlineKeyboardButton('Подписаться на канал', url='https://t.me/ShahVera'))
    mark.add(telebot.types.InlineKeyboardButton('Я подписан', callback_data=message.from_user.id))
    bot.send_message(message.chat.id, message_text, reply_markup=mark)


def check_sub_channel(chat_member):
    check = bot.get_chat_member(CHANNEL_ID, chat_member)

    if check.status != 'left':
        return True
    return False


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    user = callback.from_user.id

    if check_sub_channel(user):
        message_text = f'Отлично😉!\nДержи мой гайд «Искусство проявления себя», изучай и начинай проявляться!\n\n' \
                       f'Всё получится!'
        bot.send_document(user, open('гайд Искусство проявления себя.pdf', 'rb'))
        bot.send_message(user, message_text)
    else:
        mark = telebot.types.InlineKeyboardMarkup()
        mark.add(telebot.types.InlineKeyboardButton('Подписаться на канал', url='https://t.me/ShahVera'))
        mark.add(telebot.types.InlineKeyboardButton('Я подписан', callback_data=callback.from_user.id))
        bot.send_message(user, 'Я не нашла тебя среди подписчиков😊, давай попробуем ещё раз!', reply_markup=mark)


def create_error_message(error: Exception) -> str:
    return f'{datetime.now()} >>> {error.__class__} >>> {error}'


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage? \
        chat_id={ADMIN_CHAT_ID}&text={create_error_message(e)}')
