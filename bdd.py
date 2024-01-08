import mysql.connector
import pandas as pd
from tabulate import tabulate

def display_query_results(cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(results, columns=columns)
    print(tabulate(df, headers='keys', tablefmt='grid'))

def main_menu():
    print("\nPlease choose an option:")
    print("1 - Display all 'Amenageur'")
    print("2 - Display all 'Operateur'")
    print("3 - More options...")
    print("0 - Exit")
    return input("Enter your choice: ")

def more_options():
    print("\nMore options:")
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
        option = more_options()
        
        if option == '1':
            display_query_results(mycur, "SELECT * FROM Station;")
        elif option == '2':
            code_insee = input("Enter the code INSEE: ")
            display_query_results(mycur, f"SELECT nom_station, adresse_station, code_insee_commune FROM station WHERE code_insee_commune LIKE '{code_insee}%';")
    
        elif option == '3':
            city_name = input("Enter the name of the city: ")
            display_query_results(mycur, f"SELECT * FROM Station WHERE nom_station LIKE '%{city_name}%';")
        elif option == '0':
            continue
        else:
            print("Invalid option, please try again.")
    elif choice == '0':
        print("Exiting program.")
        break
    else:
        print("Invalid option, please try again.")

# Close the cursor and disconnect from the server
mycur.close()
mydb.close()
