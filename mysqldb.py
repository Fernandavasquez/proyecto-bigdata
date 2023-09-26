import pymongo
import mysql.connector


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
    password="Ferchis03",
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
