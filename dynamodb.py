import boto3
import pymongo
from boto3.dynamodb.conditions import Key


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
            print('El nombre del pais que busca no existe!')
        else:
            for i in response['Items']:
                print('Pais: ' + i['name'] + ' -> ' + ' Simbolo: ' + i['currencies'][0] + ' -> ' + 'Estados:' + str(len(i['states'])))
                self.__country_id = i['country_id']

    def get_country_id(self):
        return str(self.__country_id)

    def query_data_country_coin(self, key_value: str):
        response = self.__dynamodb.Table('country_coin').query(
            KeyConditionExpression=Key('id').eq(key_value)
        )
        if len(response['Items']) == 0:
            print('El id de la moneda que busca no existe!')
        else:
            for i in response['Items']:
                print('LA BASE DE LA CONVERSION ES: ' + i['base'])
                print('LOS VALORES DE LA CONVERSION SON:')
                print(i['currencies_value'])

    def query_data_country_weather(self, key_value: str):
        response = self.__dynamodb.Table('country_weather').query(
            KeyConditionExpression=Key('id').eq(key_value)
        )
        if len(response['Items']) == 0:
            print('El id del clima que busca no existe!')
        else:
            for i in response['Items']:
                for x in i['state_weather']:
                    print(x['state_name'])
                    print(x['weather_data'])
                    print('--------------------------------')

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
    