import boto3
import pymongo
from boto3.dynamodb.conditions import Key
import datetime


class DynamoDB:
    def __init__(self):
        self.__country_id = ''
        self.__client = boto3.client(
            'dynamodb',
            aws_access_key_id='AKIA24QP3VLBMDCF3VBR',
            aws_secret_access_key='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',
            region_name='us-east-2'
        )

        self.__dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIA24QP3VLBMDCF3VBR',
            aws_secret_access_key='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',
            region_name='us-east-2'
        )

        self.__ddb_exceptions = self.__client.exceptions
        # Configurcion de la conexión a MongoDB
        self.__mongo = pymongo.MongoClient('mongodb://localhost:27017/')
        self.__mongo_db = self.__mongo['dbproyecto']
        self.__mongo_country = self.__mongo_db['country']
        self.__mongo_countryc = self.__mongo_db['country_coin']
        self.__mongo_countryw = self.__mongo_db['country_weather']

    def insert_data_country(self, data: dict):
        try:
            self.__dynamodb.Table('country').put_item(
                Item=data
            )
            print('Insertado con exito! ')
        except self.__ddb_exceptions.ResourceInUseException:
            print('No se pudo insertar el elemento')


    def insert_data_country_coin(self, data: dict):
        try:
            self.__dynamodb.Table('country_coin').put_item(
                Item=data
            )
            print('Insertado con exito! ')
        except self.__ddb_exceptions.ResourceInUseException:
            print('No se pudo insertar el elemento')

    def insert_data_country_weather(self, data: dict):
        try:
            self.__dynamodb.Table('country_weather').put_item(
                Item=data
            )
            print('Insertado con exito! ')
        except self.__ddb_exceptions.ResourceInUseException:
            print('No se pudo insertar el elemento')

    def query_data_country(self, key_value: str):
        response = self.__dynamodb.Table('country').query(
            KeyConditionExpression=Key('name').eq(key_value)
        )
        if len(response['Items']) == 0:
            return 0
        else:
            return response['Items'][0]

    def get_country_id(self):
        return str(self.__country_id)

    def query_data_country_coin(self, country_id: str):
        response_gtq = []
        response_usd = []
        response_eur = []
        base = ''

        date = datetime.date(2023, 1, 1)
        date_end = datetime.date(2023, 9, 26)
        while date <= date_end:
            value = str(date) + country_id + '-C'
            response = self.__dynamodb.Table('country_coin').query(
                KeyConditionExpression=Key('id').eq(value)
            )
            response_gtq.append((response['Items'][0]['id'][:10], response['Items'][0]['currencies_value']['GTQ']))
            response_usd.append((response['Items'][0]['id'][:10], response['Items'][0]['currencies_value']['USD']))
            response_eur.append((response['Items'][0]['id'][:10], response['Items'][0]['currencies_value']['EUR']))
            base = response['Items'][0]['base']
            date += datetime.timedelta(days=1)
        return response_usd, response_eur, response_gtq, base

    def query_data_country_weather(self, country_id: str):
        response_end = {}
        response_data_matplotlib = []
        date = datetime.date(2023, 1, 1)
        date_end = datetime.date(2023, 9, 26)
        value = str(date) + country_id + '-W'
        response = self.__dynamodb.Table('country_weather').query(
            KeyConditionExpression=Key('id').eq(value)
        )
        if len(response['Items']) != 0:
            for item in response['Items'][0]['state_weather']:
                response_end[str(item['state_name'])] = [[], [], []]

            while date <= date_end:
                value = str(date) + country_id + '-W'
                response = self.__dynamodb.Table('country_weather').query(
                    KeyConditionExpression=Key('id').eq(value)
                )
                response_data_matplotlib.append(response['Items'][0])
                for state in response['Items'][0]['state_weather']:
                    response_end[state['state_name']][0].append((str(date), state['weather_data']['Min']))
                    response_end[state['state_name']][1].append((str(date), state['weather_data']['Promedio']))
                    response_end[state['state_name']][2].append((str(date), state['weather_data']['Max']))
                date += datetime.timedelta(days=1)
        return response_end, response_data_matplotlib

    def get_country_data_from_mongodb(self, country):
        list_country_data = []
        for item in self.__mongo_country.find({'name': country}):
            del item['_id']
            self.__country_id = item['country_id']
            list_country_data.append(item)
        return list_country_data

    def get_country_coin_data_from_mongodb(self):
        list_country_coin_data = []
        for item in self.__mongo_countryc.find({'country_id': self.__country_id}):
            item['id'] = item['_id']
            del item['_id']
            list_country_coin_data.append(item)
        return list_country_coin_data

    def get_country_weather_data_from_mongodb(self):
        list_country_weather_data = []
        for item in self.__mongo_countryw.find({'country_id': self.__country_id}):
            item['id'] = item['_id']
            del item['_id']
            list_country_weather_data.append(item)
        return list_country_weather_data
    