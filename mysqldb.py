import pymongo
import mysql.connector
import datetime


# Configurar la conexión a DynamoDB
mongo = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo['dbproyecto']
mongo_country = mongo_db['country']
mongo_countryc = mongo_db['country_coin']
mongo_countryw = mongo_db['country_weather']

# Establecer la conexión a MySQL
conexion_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Cralsive1620",
    database="dbProyecto"
)


cursor_mysql = conexion_mysql.cursor()

# Función para extraer datos de DynamoDB
def extraer_datos_de_mongoCountry():
    datos_mongodb = []
    datos_mongodb_states = []
    mongo_dataC = mongo_country.find()
    for item in mongo_dataC:
        datos_mongodb.append((item['name'], item['country_id'], item['currencies'][0]))
        for item2 in item['states']:
            datos_mongodb_states.append((item2, item['country_id']))
    return datos_mongodb, datos_mongodb_states


def extraer_datos_de_mongodbCoin():
    datos_mongodb = []
    for item in mongo_countryc.find():

        datos_mongodb.append((item['_id'], item['base'], item['currencies_value']['GTQ'],
                              item['currencies_value']['USD'], item['currencies_value']['EUR'],
                              item['country_id']))
    return datos_mongodb

def extraer_datos_de_mongodbWeather():
    datos_mongodb = []
    datos_mongodb_weather = []
    for item in mongo_countryw.find():
        datos_mongodb.append((item['_id'], item['_id'][:10], item['country_id']))
        for item2 in item['state_weather']:
            datos_mongodb_weather.append((item2['state_name'],
                               item2['weather_data']['Max'], item2['weather_data']['Min'],
                               item2['weather_data']['Promedio'], item['_id']))

    return datos_mongodb, datos_mongodb_weather

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


def query_MysqlCountry(busqueda: str):
    consulta = "SELECT * FROM tblcountry WHERE name = %s"
    valor_a_buscar = busqueda

    cursor_mysql.execute(consulta, (valor_a_buscar,))

    # Obtiene los resultados
    resultados = cursor_mysql.fetchall()
    return resultados

def query_dataCC(busqueda):
    consulta = "SELECT * FROM tblcountrycoin WHERE tblcountry_country_id = %s"
    valor_a_buscar = busqueda
    cursor_mysql.execute(consulta, (valor_a_buscar,))
    # Obtiene los resultados
    resultados = cursor_mysql.fetchall()
    response_gtq = []
    response_usd = []
    response_eur = []
    base = ''
    for item in resultados:
       # print(item)
        response_gtq.append((item[0][:10], item[2]))
        response_usd.append((item[0][:10], item[3]))
        response_eur.append((item[0][:10], item[4]))
        base = item[5]

    return response_usd, response_eur, response_gtq, base
def query_dataestados(busqueda):
    consulta = "SELECT COUNT(id) FROM tblestados WHERE tblcountry_country_id = %s"
    valor_a_buscar = busqueda

    cursor_mysql.execute(consulta, (valor_a_buscar,))

    # Obtiene los resultados
    resultados = cursor_mysql.fetchall()
    return resultados[0][0]


def query_dataweather(busqueda):
    consulta = "SELECT * FROM tblcountry_weather WHERE tblcountry_country_id = %s LIMIT 1"
    valor_a_buscar = busqueda
    cursor_mysql.execute(consulta, (valor_a_buscar,))
    # Obtiene los resultados
    resultados = cursor_mysql.fetchall()

    consulta = "SELECT * FROM tblweather WHERE tblcountry_weather_id = %s"
    cursor_mysql.execute(consulta, (resultados[0][0],))
    resultados = cursor_mysql.fetchall()

    aux = []
    response = {}
    for item in resultados:
        aux.append(str(item[1]))
        response[str(item[1])] = [[], [], []]
    for state in aux:
        consulta = "SELECT * FROM tblweather WHERE state_name = %s"
        cursor_mysql.execute(consulta, (state,))
        resultados = cursor_mysql.fetchall()
        for item in resultados:
            response[state][0].append((item[5][:10], item[2]))
            response[state][1].append((item[5][:10], item[4]))
            response[state][2].append((item[5][:10], item[3]))
    return response


def query_dataweather_matplotlib(country_id: str):
    data_matplotlib = []
    date = datetime.date(2023, 1, 1)
    date_end = datetime.date(2023, 9, 26)
    while date <= date_end:
        response_end = {}
        value = str(date) + country_id + '-W'
        consulta = "SELECT * FROM tblweather WHERE tblcountry_weather_id = %s"
        cursor_mysql.execute(consulta, (value,))
        resultados = cursor_mysql.fetchall()
        response_end['_id'] = value
        response_end['country_id'] = country_id
        response_end['state_weather'] = []
        for state in resultados:
            aux = {}
            aux['state_name'] = state[1]
            aux['weather_data'] = {
                'Min': state[3],
                'Max': state[2],
                'Promedio': state[4]
            }
            response_end['state_weather'].append(aux)
        data_matplotlib.append(response_end)
        date += datetime.timedelta(days=1)
    return data_matplotlib
