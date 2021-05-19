import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

# Вариант работы через возврат строкой ошибки пользователя без вызова исключения
        # if quote == base:
        #     return "Валюты в операции конвертации должны отличаться используйте /help"
        #
        # try:
        #     quote_ticker = keys[quote]
        # except KeyError:
        #     return f"Валюты нет в списке -{quote} используйте /values"
        # try:
        #     base_ticker = keys[base]
        # except KeyError:
        #     return f"Валюты нет в списке - {base} используйте /values"
        # try:
        #     amount = float(amount)
        # except ValueError:
        #     return f"Укажите количество переводимой валюты в виде числа - {amount}"

        if quote == base:
           raise APIException("Валюты в операции конвертации должны отличаться - используйте /help")

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюты {quote} нет в списке - используйте /values")
        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюты {base}  нет в списке - используйте /values")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Укажите количество переводимой валюты в виде числа - {amount}")

        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}') # из урока с другим API
        rg = requests.get(f"http://api.exchangeratesapi.io/latest?access_key=1688aa182150b274a8543c27c68c0149&base=EUR&symbols={quote_ticker}")
        rb = requests.get(f"http://api.exchangeratesapi.io/latest?access_key=1688aa182150b274a8543c27c68c0149&base=EUR&symbols={base_ticker}")
        total_base = round(json.loads(rb.content)['rates'][base_ticker] / json.loads(rg.content)['rates'][quote_ticker] * amount,3)

        return total_base