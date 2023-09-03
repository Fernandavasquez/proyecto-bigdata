import boto3
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

    def insert_dataC(self, data: dict):
        try:
            self.__dynamodb.Table('country').put_item(
                Item=data
            )
            print('Insertado con exito! ')
        except self.__ddb_exceptions.ResourceInUseException:
            print('No se pudo insertar el elemento')


    def insert_dataCC(self, data: dict):
        try:
            self.__dynamodb.Table('country_coin').put_item(
                Item=data
            )
            print('Insertado con exito! ')
        except self.__ddb_exceptions.ResourceInUseException:
            print('No se pudo insertar el elemento')

    def insert_dataCW(self, data: dict):
        try:
            self.__dynamodb.Table('country_weather').put_item(
                Item=data
            )
            print('Insertado con exito! ')
        except self.__ddb_exceptions.ResourceInUseException:
            print('No se pudo insertar el elemento')


    def query_dataC(self, key_value: str):
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

    def query_dataCC(self, key_value: str):
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

    def query_dataCW(self, key_value: str):
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


    def show_table(self):
        response = self.__dynamodb.Table('country').scan()
        if len(response['Items']) == 0:
            print('Tabla vacia, agregue elementos')
        else:
            for i in response['Items']:
                print(i)
