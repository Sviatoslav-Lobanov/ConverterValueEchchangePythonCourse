import telebot
from config import keys, TOKEN
from extensions import *

bot = telebot.TeleBot(TOKEN)



# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text= 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> \
    <в какую валюту первести> \
    <количество перводимой валюты> \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text= 'Доступные валюты>'
    for key in keys.keys():
        text = "\n".join((text,key, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    # Вариант в котором ошибки пользователя возвращаются строкой и просто отправляются в чат
    # try:
    #     values = message.text.split(' ')
    #     if len(values) != 3:
    #         bot.reply_to(message, "Неверно введена команда используйте /help")
    #     else:
    #         quote, base, amount = values
    #         total_base = CryptoConverter.convert(quote, base, amount)
    #         if type(total_base) is str:  # Если вернулась строка, то это вернулась ошибка, выводим ее как есть и продолжаем работу бота
    #             bot.reply_to(message, total_base)
    #         else:
    #             text = f'Цена {amount} {quote} в {base} - {total_base}'
    #             bot.reply_to(message, text)
    # except Exception as e:
    #     bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Неверно введена команда, используйте /help")
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.reply_to(message, text)

bot.polling()