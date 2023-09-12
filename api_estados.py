import datetime

import requests

from dynamodb import DynamoDB
from mongo import MongoDB

class Country:
    def __init__(self, name: str):
        self.__name = name
        self.__states: list[str] = []
        self.__country = {}
        self.__base = ""
        self.__country_id = ""
        self.get_states_api()

    def get_states_api(self):
        url = "https://www.universal-tutorial.com/api/getaccesstoken"
        headers = {'api-token': 'CSNmSIg0NxEWru79-xbj8XUia1e_7QHj7Nfcz4yRzzItS-0MCLPuuW6zHnhXF1-qMfM',
                   'Accept': 'application/json',
                   'user-email': 'csiguenzavelasquez@gmail.com'}
        response = requests.get(url, headers=headers).json()

        url = "https://www.universal-tutorial.com/api/countries/"
        headers = {'Authorization': 'Bearer ' + response['auth_token'],
                   'Accept': 'application/json'}

        response = requests.get(url, headers=headers).json()
        for countries in response:
            if str(countries['country_name']) == self.__name:
                self.__country['name'] = str(countries['country_name'])
                self.__country['country_id'] = str(countries['country_short_name'])
                self.__country_id = str(countries['country_short_name'])
                break
        url = "https://www.universal-tutorial.com/api/states/"+self.__name

        response = requests.get(url, headers=headers).json()
        self.__states = []
        for state in response:
            self.__states .append(str(state['state_name']))
        self.__country['states'] = self.__states
        self.get_symbol()

    def get_symbol(self):
        auxlist = []
        url = "https://restcountries.com/v3.1/name/"+self.__name
        response = requests.get(url).json()
        for info in response:
            if info['currencies']:
                for coin in info['currencies']:
                    auxlist.append(str(coin))

        self.__country['currencies'] = auxlist
        self.__base = auxlist[0]
    def get_states(self):
        return self.__states
    def insert_country_data(self):
        db = MongoDB()
        db.insert_dataC(self.__country)
    def get_weather(self):
        for state in self.__states:
            url = "http://api.weatherapi.com/v1/forecast.json?key=d7fbf6662aa24f3aaff20505232208&q=" + state

            response = requests.get(url).json()
            print('Departamento/Estado: ' + state)
            print('Fecha:' + response['forecast']['forecastday'][0]['date'])
            print('Min: ' + response['forecast']['forecastday'][0]['day']['mintemp_c'] + 'C°')
            print('Max: ' + response['forecast']['forecastday'][0]['day']['maxtemp_c'] + 'C°')
            print('Promedio: ' + response['forecast']['forecastday'][0]['day']['avgtemp_c' + 'C°'])

    def insert_weather(self, date):
        #date = datetime.date(2023, 5, 27)
        db = MongoDB()
        while date <= datetime.date.today():
            country_weather = {'_id': str(date) + self.__country_id+"-W", 'country_id': self.__country_id, 'state_weather': []}
            for state in self.get_states():
                url = "http://api.weatherapi.com/v1/history.json?key=c1c948ad023a40d78f263757231209&q=" + state + "&dt=" + str(
                    date)
                response = requests.get(url).json()
                weather_data = {}
                weather_data['Min'] = str(response['forecast']['forecastday'][0]['day']['mintemp_c'])
                weather_data['Max'] = str(response['forecast']['forecastday'][0]['day']['maxtemp_c'])
                weather_data['Promedio'] = str(response['forecast']['forecastday'][0]['day']['avgtemp_c'])
                country_weather['state_weather'].append({'state_name': state, 'weather_data': weather_data})
            date += datetime.timedelta(days=1)
            print(date)
            db.insert_dataCW(country_weather)

    def insert_country_coin(self):
        auxdate = str(datetime.date.today())
        url = f"https://api.exchangerate.host/timeseries?start_date=2023-05-01&end_date={auxdate}&base={self.__base}&symbols=GTQ,USD,EUR"

        response = requests.get(url).json()
        rates_data = response['rates']
        db = MongoDB()
        print(f"Tipo de Cambio de Moneda en {self.__name}")
        print('   Fecha    |    GTQ     |    USD     | EUR')
        print('----------------------------------------')

        for date, rates in rates_data.items():
            coin_value = {'_id': str(date) + self.__country_id+"-C", 'country_id': self.__country_id, 'base': self.__base}
            coin_data = {}
            coin_data['GTQ'] = str(rates.get('GTQ'))
            coin_data['USD'] = str(rates.get('USD'))
            coin_data['EUR'] = str(rates.get('EUR'))
            coin_value['currencies_value'] = coin_data
            # print(coin_value)
            db.insert_dataCC(coin_value)
