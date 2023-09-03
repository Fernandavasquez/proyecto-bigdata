import boto3
import mysql.connector


# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  # Cambia la región si es necesario
table_name = 'nombre_de_la_tabla_dynamo'
table = dynamodb.Table(table_name)

# Configuración de MySQL
mysql_config = {
    'user': 'root',
    'password': 'Ferchis03',
    'host': 'localhost',  # O la dirección IP de tu servidor MySQL
    'database': 'bdrproyecto',
    'raise_on_warnings': True,
}

# Intenta establecer la conexión a MySQL
try:
    mysql_connection = mysql.connector.connect(**mysql_config)

    if mysql_connection.is_connected():
        print("Conexión exitosa a MySQL")
        mysql_cursor = mysql_connection.cursor()

        # Escanea todos los elementos en la tabla DynamoDB
        response = table.scan()

        for item in response['Items']:
            # Procesa los datos de DynamoDB y ejecuta una inserción en MySQL
            mysql_insert_query = "INSERT INTO country (name, country_id) VALUES (Guatemala, 1)"
            data_to_insert = (item['name'], item['campo_dynamodb2'])

            mysql_cursor.execute(mysql_insert_query, data_to_insert)
            mysql_connection.commit()

        print("Datos insertados en MySQL correctamente.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Asegúrate de cerrar la conexión cuando hayas terminado
    if 'mysql_connection' in locals() and mysql_connection.is_connected():
        mysql_cursor.close()
        mysql_connection.close()
        print("Conexión a MySQL cerrada")
