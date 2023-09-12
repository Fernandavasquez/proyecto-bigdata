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
        self.__country.insert_one(data)
        print('Insertado con exito! ')

    def insert_dataCC(self, data: dict):
        self.__country_coin.insert_one(data)
        print('Insertado con exito! ')

    def insert_dataCW(self, data: dict):
        self.__country_weather.insert_one(data)
        print('Insertado con exito! ')

    def query_dataC(self, key_value: dict):
        response = self.__country.find(key_value)

        # if len(response['Items']) == 0:
        #     print('El nombre del pais que busca no existe!')
        # else:
        #     for i in response['Items']:
        #         print('Pais: ' + i['name'] + ' -> ' + ' Simbolo: ' + i['currencies'][0] + ' -> ' + 'Estados:' + str(
        #             len(i['states'])))
        #         self.__country_id = i['country_id']

    def query_dataCC(self, key_value: dict):
        response = self.__country_coin.find(key_value)
        # if len(response['Items']) == 0:
        #     print('El id de la moneda que busca no existe!')
        # else:
        #     for i in response['Items']:
        #         print('LA BASE DE LA CONVERSION ES: ' + i['base'])
        #         print('LOS VALORES DE LA CONVERSION SON:')
        #         print(i['currencies_value'])
    def query_dataCW(self, key_value: dict):
        response = self.__country_weather.find(key_value)
        # if len(response['Items']) == 0:
        #     print('El id del clima que busca no existe!')
        # else:
        #     for i in response['Items']:
        #         for x in i['state_weather']:
        #             print(x['state_name'])
        #             print(x['weather_data'])
        #             print('--------------------------------')
    def get_country_id(self):
        return str(self.__country_id)