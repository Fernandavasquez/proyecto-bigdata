import datetime
import requests
from mongo import MongoDB


class Country:
    def __init__(self, name: str):
        self.__name = name
        self.__states: list[str] = []
        self.__country = {}
        self.__base = ""
        self.__country_id = ""
        self.get_states_api()
        self.exists: bool

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
        exist = False
        for countries in response:
            if str(countries['country_name']) == self.__name:
                self.__country['name'] = str(countries['country_name'])
                self.__country['country_id'] = str(countries['country_short_name'])
                self.__country_id = str(countries['country_short_name'])
                exist = True
                break

        if exist:
            self.exists = True
            url = "https://www.universal-tutorial.com/api/states/" + self.__name

            response = requests.get(url, headers=headers).json()
            self.__states = []
            for state in response:
                self.__states.append(str(state['state_name']))
            self.__country['states'] = self.__states
            self.get_symbol()
        else:
            self.exists = False
            print('El pais que busca no existe...')

    def get_symbol(self):
        auxlist = []
        url = "https://restcountries.com/v3.1/name/" + self.__name
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

    def insert_weather(self, date):
        db = MongoDB()
        while date <= datetime.date.today():
            country_weather = {'_id': str(date) + self.__country_id + "-W", 'country_id': self.__country_id,
                               'state_weather': []}
            if db.get_country_weather_id(country_weather['_id']):
                for state in self.get_states():
                    url = "http://api.weatherapi.com/v1/history.json?key=c1c948ad023a40d78f263757231209&q=" + state + "&dt=" + str(
                        date)
                    response = requests.get(url).json()
                    if 'error' not in response:
                        weather_data = {'Min': str(response['forecast']['forecastday'][0]['day']['mintemp_c']),
                                        'Max': str(response['forecast']['forecastday'][0]['day']['maxtemp_c']),
                                        'Promedio': str(response['forecast']['forecastday'][0]['day']['avgtemp_c'])}
                        country_weather['state_weather'].append({'state_name': state, 'weather_data': weather_data})
                print(date)
                db.insert_dataCW(country_weather)

            date += datetime.timedelta(days=1)

    def insert_country_coin(self):
        db = MongoDB()
        auxdate = str(datetime.date.today())
        url = f"https://api.exchangerate.host/timeseries?start_date=2023-01-01&end_date={auxdate}&base={self.__base}&symbols=GTQ,USD,EUR"

        response = requests.get(url).json()
        rates_data = response['rates']

        for date, rates in rates_data.items():
            coin_value = {'_id': str(date) + self.__country_id + "-C", 'country_id': self.__country_id,
                          'base': self.__base}
            coin_data = {'GTQ': str(rates.get('GTQ')),
                         'USD': str(rates.get('USD')),
                         'EUR': str(rates.get('EUR'))}
            coin_value['currencies_value'] = coin_data
            db.insert_dataCC(coin_value)
