import datetime
from dynamodb import DynamoDB
from api_estados import Country

exitw = False
print('-------------------------------------------')
print('Inserte Nombre del Pais')
pais = input("Ingrese un pais: ")

new_country = Country(pais)

if new_country.exists:
    while not exitw:
        print('-------------------------------------------')
        print('1. Insertar Pais')
        print('2. Insertar Cambios de Moneda')
        print('3. Insertar Clima')
        print('4. SALIR')
        option = input('Ingrese una opcion: ')

        match option:
            case '1':
                new_country.insert_country_data()
            case '2':
                new_country.insert_country_coin()
            case '3':
                print('Ingrese la fecha de inico para obtener los datos YYYY-mm-dd:')
                year = int(input('Ingrese el año: '))
                month = int(input('Ingrese el mes: '))
                day = int(input('Ingrese el dia: '))
                date = datetime.date(year, month, day)
                new_country.insert_weather(date)

            case '4':
                exitw = True

        print('-----------------------------------------------------------')

