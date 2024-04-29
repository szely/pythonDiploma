import requests
import xml.etree.ElementTree as ET


def get_currency_rate(from_to_currency=None):
    """
    :param from_to_currency is list ['USD', 'RUB'] whole list char_code_currency see here
     https://www.cbr.ru/scripts/XML_daily.asp
    :return: float_number
    """

    list_foreign_currency = [currency for currency in from_to_currency if currency != 'RUB']
    list_ration_currency = []
    current_currency_rate = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')

    def get_parameter_currency_from_response(searching_value, char_code_currency):
        """
        :param searching_value = "Nominal" or "Value"
        :param char_code_currency ex('RUB', USD'), char_code_currency see here https://www.cbr.ru/scripts/XML_daily.asp
        :return: if searching_value is Nominal - int, else is float
        """
        paramentr = ET.fromstring(current_currency_rate.text). \
            find(f'./Valute[CharCode="{char_code_currency}"]/{searching_value}').text
        if searching_value == 'Nominal':
            return int(paramentr)
        else:
            return float(paramentr.replace(',', '.'))

    def get_currency_ratio_with_rub(foreign_currency):
        nominal = get_parameter_currency_from_response("Nominal", foreign_currency)
        rub_for_nominal_currency = get_parameter_currency_from_response("Value", foreign_currency)
        count_currency_for_one_rub = nominal / rub_for_nominal_currency
        return count_currency_for_one_rub

    for currency in list_foreign_currency:
        list_ration_currency.append(get_currency_ratio_with_rub(currency))

    if from_to_currency[0] == 'RUB':
        return list_ration_currency[0]
    elif from_to_currency[1] == 'RUB':
        return 1 / list_ration_currency[0]
    else:
        return list_ration_currency[1] / list_ration_currency[0]

print(get_currency_rate(['EUR', 'RUB'] ))



def get_rate(day):
    headers = {'content-type': 'text/xml'}
    body = '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' '  <soap:Body>    <KeyRateXML xmlns="http://web.cbr.ru/">' \
    f'      <fromDate>{day}</fromDate>      <ToDate>{day}</ToDate>' \
    '    </KeyRateXML>  </soap:Body> </soap:Envelope>'
    response = requests.post(url, data=body,headers=headers)
    keyrate = response.text.split("<Rate>")[1].split("</Rate>")[0]
    return keyrate
