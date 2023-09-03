import boto3
import mysql.connector
import mysqlConection

db = mysqlConection
exitw = False

while not exitw:
    print('-------------------------------------------')
    print('1. Cargar Datos')
    print('2. Buscar un dato en especifico')
    print('3. Insertar un dato')
    print('4. SALIR')
    option = input('Ingrese una opcion: ')

    match option:
        case '1':
            # Obtener datos de DynamoDB
            datos_dynamodb = db.extraer_datos_de_dynamodbCountry(db.dynamodb.Table(db.nombre_tabla_dynamodb))
            datos_dynamodb2 = db.extraer_datos_de_dynamodbCoin(db.dynamodb.Table(db.nombre_tabla_dynamodb2))
            datos_dynamodb3 = db.extraer_datos_de_dynamodbWeather(db.dynamodb.Table(db.nombre_tabla_dynamodb3))
            # Insertar los datos en MySQL
            db.insertar_datos_en_mysqlCountry(db.conexion_mysql, datos_dynamodb)
            db.insertar_datos_en_mysqlCoin(db.conexion_mysql, datos_dynamodb2)
            db.insertar_datos_en_mysqlWeather(db.conexion_mysql, datos_dynamodb3)
        case '2':

            print('Table Country Query')
            # Solicitar al usuario que ingrese el país a buscar
            busqueda = input("Ingrese el nombre del pais a buscar")
            db.query_MysqlCountry(busqueda)




        case '3':
            pass

        case '4':
            exitw = True


# Cerrar la conexión a MySQL
db.cursor_mysql.close()
db.conexion_mysql.close()
