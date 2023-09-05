import boto3
import mysql.connector


# Configurar la conexión a DynamoDB
dynamodb = boto3.resource('dynamodb',
            aws_access_key_id='AKIA24QP3VLBMDCF3VBR',
            aws_secret_access_key='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',
            region_name='us-east-2')

# Nombre de la tabla DynamoDB
nombre_tabla_dynamodb = 'country'
nombre_tabla_dynamodb2 = 'country_coin'
nombre_tabla_dynamodb3 = 'country_weather'

# Establecer la conexión a MySQL
conexion_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ferchis03",
    database="dbProyecto"
)
# Crear un objeto cursor para interactuar con MySQL
cursor_mysql = conexion_mysql.cursor()

# Función para extraer datos de DynamoDB
def extraer_datos_de_dynamodbCountry(tabla_dynamodb):
    datos_dynamodb = []
    datos_dynamodb_states = []

    for item in tabla_dynamodb.scan()['Items']:
        datos_dynamodb.append((item['name'], item['country_id'], item['currencies'][0]))
        for item2 in item['states']:
            datos_dynamodb_states.append((item2, item['country_id']))


    return datos_dynamodb, datos_dynamodb_states


def extraer_datos_de_dynamodbCoin(tabla_dynamodb):
    datos_dynamodb = []

    for item in tabla_dynamodb.scan()['Items']:
        datos_dynamodb.append((item['id'], item['base'], item['currencies_value']['GTQ'],
                               item['currencies_value']['USD'], item['currencies_value']['EUR'],
                               item['country_id']))


    return datos_dynamodb

def extraer_datos_de_dynamodbWeather(tabla_dynamodb):
    datos_dynamodb = []
    datos_dynamodb_weather = []
    for item in tabla_dynamodb.scan()['Items']:
        datos_dynamodb.append((item['id'], item['id'][:10], item['country_id']))
        for item2 in item['state_weather']:
            datos_dynamodb_weather.append((item2['state_name'],
                               item2['weather_data']['Max'], item2['weather_data']['Min'],
                               item2['weather_data']['Promedio'], item['id']))

    return datos_dynamodb, datos_dynamodb_weather

# Función para insertar datos en MySQL
def insertar_datos_en_mysqlCountry(conexion_mysql, datos):
    insert_query = "INSERT INTO tblcountry (name, country_id, base) VALUES (%s, %s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")

def insertar_datos_en_mysqlStates(conexion_mysql, datos):
    insert_query = "INSERT INTO tblestados (name, tblcountry_country_id) VALUES (%s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")

def insertar_datos_en_mysqlCoin(conexion_mysql, datos):
    insert_query = "INSERT INTO tblcountrycoin (id_coin, base, GTQ, USD, EUR, tblcountry_country_id) VALUES (%s, %s,%s, %s, %s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")


def insertar_datos_en_mysqlCWeather(conexion_mysql, datos):
    insert_query = "INSERT INTO tblcountry_weather (id, date, tblcountry_country_id) VALUES (%s, %s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")

def insertar_datos_en_mysqlWeather(conexion_mysql, datos):
    insert_query = "INSERT INTO tblweather (state_name, min, max, promedio, tblcountry_weather_id) " \
                   "VALUES (%s, %s, %s, %s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")


def query_MysqlCountry(busqueda):
    consulta = "SELECT * FROM tblcountry WHERE name = %s"
    valor_a_buscar = busqueda

    cursor_mysql.execute(consulta, (valor_a_buscar,))

    # Obtiene los resultados
    resultados = cursor_mysql.fetchall()

    # Itera a través de los resultados
    for fila in resultados:
        # Accede a las columnas de la fila como fila[0], fila[1], etc.
        print(fila)

def query_dataCC(busqueda):
    consulta = "SELECT * FROM tblcountrycoin WHERE id_coin = %s"
    valor_a_buscar = busqueda

    cursor_mysql.execute(consulta, (valor_a_buscar,))

    # Obtiene los resultados
    resultados = cursor_mysql.fetchall()

    if len(resultados['Items']):
        print('El id de la moneda que busca no existe!')
    else:
        for i in resultados['Items']:
            print('LA BASE DE LA CONVERSION ES: ' + i['base'])
            print('LOS VALORES DE LA CONVERSION SON:')
            print(i['currencies_value'])
