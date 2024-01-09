import mysql.connector
import pandas as pd
from tabulate import tabulate

def display_query_results(cursor, query, message=None):
    if message:
        print(message)
    cursor.execute(query)
    results = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(results, columns=columns)
    print(tabulate(df, headers='keys', tablefmt='grid'))

def post_station_options(cursor, station_id):
    print("\nSelect an option for more details:")
    print("1 - Display access information for the station")
    print("2 - Display all PDC (charging points) information of the station and their tarification")
    print("0 - Return to main menu")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        display_query_results(cursor, f"SELECT * FROM Acces WHERE id_station_itinerance = '{station_id}';")
    elif choice == '2':
        display_query_results(cursor, f"SELECT * FROM PDC WHERE id_station_itinerance = '{station_id}';")
        pdc_id = input("\nEnter ID of the PDC for tarification details or '0' to return: ")
        if pdc_id != '0':
            display_query_results(cursor, f"SELECT * FROM Tarification WHERE id_pdc_itinerance = '{pdc_id}';",
                                  message=f"\nTarification for PDC {pdc_id}:")
    elif choice == '0':
        return
    else:
        print("Invalid option, please try again.")

def main_menu():
    print("\nPlease choose an option:")
    print("1 - Display all 'Amenageur'")
    print("2 - Display all 'Operateur'")
    print("3 - Stations")
    print("0 - Exit")
    return input("Enter your choice: ")

def stations_menu():
    print("\nStations menu:")
    print("1 - Display all stations")
    print("2 - Display stations by code INSEE")
    print("3 - Display stations by city name")
    print("0 - Return to main menu")
    return input("Enter your choice: ")

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="userp",
    passwd="0201",
    database="projectbase",
    auth_plugin="mysql_native_password"
)
mycur = mydb.cursor()

# Main program loop
while True:
    choice = main_menu()
    
    if choice == '1':
        display_query_results(mycur, "SELECT * FROM Amenageur;")
    elif choice == '2':
        display_query_results(mycur, "SELECT * FROM Operateur;")
    elif choice == '3':
        option = stations_menu()
        
        if option == '1':
            display_query_results(mycur, "SELECT id_station_itinerance, nom_enseigne, nom_station, code_insee_commune, nbre_pdc FROM Station;")
        elif option == '2':
            code_insee = input("Enter the code INSEE: ")
            display_query_results(mycur, f"SELECT id_station_itinerance, nom_enseigne, nom_station, code_insee_commune, nbre_pdc FROM Station WHERE code_insee_commune LIKE '{code_insee}%';")
        elif option == '3':
            city_name = input("Enter the name of the city: ")
            display_query_results(mycur, f"SELECT id_station_itinerance, nom_enseigne, nom_station, code_insee_commune, nbre_pdc FROM Station WHERE nom_station LIKE '%{city_name}%';")
        
        # Ask for station ID to show more details
        station_id = input("\nEnter ID of the station for more details or '0' to return: ")
        if station_id != '0':
            post_station_options(mycur, station_id)
    
    elif choice == '0':
        print("Exiting program.")
        break
    else:
        print("Invalid option, please try again.")

# Close the cursor and disconnect from the server
mycur.close()
mydb.close()
