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
    database="bdproyectoa"
)


# Crear un objeto cursor para interactuar con MySQL
cursor_mysql = conexion_mysql.cursor()


# Función para extraer datos de DynamoDB
def extraer_datos_de_dynamodbCountry(tabla_dynamodb):
    datos_dynamodb = []

    for item in tabla_dynamodb.scan()['Items']:
        datos_dynamodb.append((item['name'], item['country_id']))

    return datos_dynamodb

def extraer_datos_de_dynamodbCoin(tabla_dynamodb):
    datos_dynamodb = []

    for item in tabla_dynamodb.scan()['Items']:
        datos_dynamodb.append((item['id'], item['country_id']))

    return datos_dynamodb

def extraer_datos_de_dynamodbWeather(tabla_dynamodb):
    datos_dynamodb = []

    for item in tabla_dynamodb.scan()['Items']:
        datos_dynamodb.append((item['id'], item['country_id']))

    return datos_dynamodb

# Función para insertar datos en MySQL
def insertar_datos_en_mysqlCountry(conexion_mysql, datos):
    insert_query = "INSERT INTO tblcountry (name, country_id) VALUES (%s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")

def insertar_datos_en_mysqlCoin(conexion_mysql, datos):
    insert_query = "INSERT INTO tblcountrycoin (id_coin, country_id) VALUES (%s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")


def insertar_datos_en_mysqlWeather(conexion_mysql, datos):
    insert_query = "INSERT INTO tblCountry_weather (id_weather, country_id) VALUES (%s, %s)"

    try:
        cursor_mysql.executemany(insert_query, datos)
        conexion_mysql.commit()
        print("Datos insertados en MySQL correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos en MySQL: {err}")

# Obtener datos de DynamoDB
datos_dynamodb = extraer_datos_de_dynamodbCountry(dynamodb.Table(nombre_tabla_dynamodb))
datos_dynamodb2 = extraer_datos_de_dynamodbCoin(dynamodb.Table(nombre_tabla_dynamodb2))
datos_dynamodb3 = extraer_datos_de_dynamodbWeather(dynamodb.Table(nombre_tabla_dynamodb3))
# Insertar los datos en MySQL
insertar_datos_en_mysqlCountry(conexion_mysql, datos_dynamodb)
insertar_datos_en_mysqlCoin(conexion_mysql, datos_dynamodb2)
insertar_datos_en_mysqlWeather(conexion_mysql, datos_dynamodb3)
#2

# Cerrar la conexión a MySQL
cursor_mysql.close()
conexion_mysql.close()
