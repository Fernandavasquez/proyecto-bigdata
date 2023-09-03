import datetime

import requests

from dynamodb import DynamoDB


class Country:
    def __init__(self, name: str):
        self.__name = name
        self.__states: list[str] = []
        self.get_states_api()

    def get_states_api(self):
        url = "https://www.universal-tutorial.com/api/states/"+self.__name
        headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJfZW1haWwiOiJjc2lndWVuemF2ZWxhc3F1ZXpAZ21haWwuY29tIiwiYXBpX3Rva2VuIjoiQ1NObVNJZzBOeEVXcnU3OS14Ymo4WFVpYTFlXzdRSGo3TmZjejR5Unp6SXRTLTBNQ0xQdXVXNnpIbmhYRjEtcU1mTSJ9LCJleHAiOjE2OTI3NTgwNDl9.bKEE9p70FrOQ0uNvJchMiUTt0t10p5J290mXwUnk4PY',
                   'Accept': 'application/json'}

        response = requests.get(url, headers=headers).json()
        for state in response:
            self.__states.append(str(state['state_name']))

    def get_states(self):
        return self.__states

    def get_weather(self):
        for state in self.__states:
            url = "http://api.weatherapi.com/v1/forecast.json?key=d7fbf6662aa24f3aaff20505232208&q=" + state

            response = requests.get(url).json()
            print('Departamento/Estado: ' + state)
            print('Fecha:' + response['forecast']['forecastday'][0]['date'])
            print('Min: ' + response['forecast']['forecastday'][0]['day']['mintemp_c'] + 'C°')
            print('Max: ' + response['forecast']['forecastday'][0]['day']['maxtemp_c'] + 'C°')
            print('Promedio: ' + response['forecast']['forecastday'][0]['day']['avgtemp_c' + 'C°'])

    def insert_weather(self):
        date = datetime.date(2023, 5, 27)

        db = DynamoDB()
        for i in range(0, 113):
            country_weather = {'id': str(date) + 'AD-W', 'country_id': 'AD', 'state_weather': []}
            for state in self.get_states():
                url = "http://api.weatherapi.com/v1/history.json?key=d7fbf6662aa24f3aaff20505232208&q=" + state + "&dt=" + str(
                    date)
                response = requests.get(url).json()
                weather_data = {}
                weather_data['Min'] = str(response['forecast']['forecastday'][0]['day']['mintemp_c'])
                weather_data['Max'] = str(response['forecast']['forecastday'][0]['day']['maxtemp_c'])
                weather_data['Promedio'] = str(response['forecast']['forecastday'][0]['day']['avgtemp_c'])
                country_weather['state_weather'].append({'state_name': state, 'weather_data': weather_data})
            date += datetime.timedelta(days=1)
            print(date)
            db.insert_data(country_weather)

    def get_exchange_rates(self, base):
        url = f"https://api.exchangerate.host/timeseries?start_date=2023-05-01&end_date=2023-08-21&base={base}&symbols=GTQ,USD,EUR"

        response = requests.get(url).json()
        rates_data = response['rates']
        db = DynamoDB()
        print(f"Tipo de Cambio de Moneda en {self.__name}")
        print('   Fecha    |    GTQ     |    USD     | EUR')
        print('----------------------------------------')

        for date, rates in rates_data.items():
            coin_value = {'id': str(date) + 'AD-C', 'country_id': 'AD', 'base': base}
            coin_data = {}
            coin_data['GTQ'] = str(rates.get('GTQ'))
            coin_data['USD'] = str(rates.get('USD'))
            coin_data['EUR'] = str(rates.get('EUR'))
            coin_value['currencies_value'] = coin_data
            # print(coin_value)
            db.insert_data(coin_value)
