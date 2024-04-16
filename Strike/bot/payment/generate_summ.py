import requests

async def generate_payment_link(amount, invoice_id):
    # Замените значения на ваши данные
    merchant_login = 'Strike58'
    password1 = 'NKiBzQeqKE8Mjg52l4j2'
    password2 = 'JPkE8mM12kTbuMs9jc0A'

    # Формирование параметров запроса
    params = {
        'MerchantLogin': merchant_login,
        'OutSum': amount,
        'InvoiceID': invoice_id,
        'Description': 'Описание платежа',
        'Password': password1,
        'Password2': password2,
        'encoding': 'utf-8'
    }

    # Отправка запроса на генерацию платежной ссылки
    response = requests.post('https://auth.robokassa.ru/Merchant/Index.aspx', data=params)

    # Извлечение платежной ссылки из ответа
    payment_link = response.url

    return payment_link
