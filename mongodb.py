import pymongo


class MongoDB:
    def __init__(self):
        self.__myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.__mydb = self.__myclient["dbproyecto"]
        self.__country = self.__mydb["country"]
        self.__country_id = ""
        self.__country_coin = self.__mydb["country_coin"]
        self.__country_weather = self.__mydb["country_weather"]

    def insert_dataC(self, data: dict):
        if self.__country.find_one({'name': data['name']}) is None:
            self.__country.insert_one(data)
            print('Insertado con exito! ')

    def insert_dataCC(self, data: dict):
        if self.__country_coin.find_one({'_id': data['_id']}) is None:
            self.__country_coin.insert_one(data)
            print('Insertado con exito! ')

    def insert_dataCW(self, data: dict):
        if self.__country_weather.find_one({'_id': data['_id']}) is None:
            self.__country_weather.insert_one(data)
            print('Insertado con exito! ')

    def query_data_c(self, key_value: dict):
        response = self.__country.find_one(key_value)
        return response

    def query_data_countrycoin(self, key_value: dict):
        response_gtq = []
        response_usd = []
        response_eur = []
        base = ''
        for item in self.__country_coin.find(key_value):
            response_gtq.append((item['_id'][:10], item['currencies_value']['GTQ']))
            response_usd.append((item['_id'][:10], item['currencies_value']['USD']))
            response_eur.append((item['_id'][:10], item['currencies_value']['EUR']))
            base = item['base']
        return response_usd, response_eur, response_gtq, base

    def query_data_countryweather(self, key_value: dict):
        response = {}
        aux = self.__country_weather.find_one(key_value)
        for item in aux['state_weather']:
            response[str(item['state_name'])] = [[], [], []]
        for item in self.__country_weather.find(key_value):
            for state in item['state_weather']:
                response[state['state_name']][0].append((item['_id'][:10], state['weather_data']['Min']))
                response[state['state_name']][1].append((item['_id'][:10], state['weather_data']['Promedio']))
                response[state['state_name']][2].append((item['_id'][:10], state['weather_data']['Max']))
        return response

    def get_information_data(self):
        data = self.__country.find()
        countries = []
        for country in data:
            countries.append(country)
        return countries


    def get_country_id(self):
        return str(self.__country_id)

    def get_country_weather_id(self, id_weather: str):
        return self.__country_weather.find_one({'_id': id_weather}) is None
