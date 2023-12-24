import mysql.connector
import pandas as pd
import numpy as np  # Import numpy for NaN handling

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="userp",  # Corrected to "userp"
    passwd="0201",
    database="projectbase",
    auth_plugin="mysql_native_password"
)

# Create a cursor
mycur = mydb.cursor()

# Read CSV file into a DataFrame
#csv_file_path = r"C:\Users\assil\Desktop\mcd projet\Point_de_Charge_Automobile\sigeif.csv"   # Replace with the actual path to your new CSV file
csv_file_path=r"C:\Users\assil\Desktop\mcd projet\Point_de_Charge_Automobile\mobive.csv"
df = pd.read_csv(csv_file_path)

# Replace NaN values with "Unknown" for specified columns
#columns_to_replace = ['adresse_station']
#df[columns_to_replace] = df[columns_to_replace].fillna('Unknown')

# Replace remaining NaN values with None (NULL) for MySQL compatibility
df = df.replace({np.nan: None})

# Iterate over the rows and insert data into MySQL table
for index, row in df.iterrows():
    values = (
        row['id_station_itinerance'],
        row['nom_enseigne'],
        row['nom_station'],
        row['implantation_station'],
        row['adresse_station'],
        row['code_insee_commune'],
        row['coordonneesXY'],
        row['nbre_pdc'],
        row['accessibilite_pmr'],
        row['restriction_gabarit'],
        row['station_deux_roues'],
        row['date_mise_en_service'],
        row['date_maj'],
        row['nom_amenageur'],
        row['nom_operateur'],
        row['contact_operateur']
    )

    # Insert data into the MySQL table
    mycur.execute("""
        INSERT INTO Station (
            id_station_itinerance, nom_enseigne, Nom_station, implantation_station,
            adresse_station, code_insee_commune, coordonneesXY, nbre_pdc,
            accessibilite_pmr, restriction_gabarit, station_deux_roues,
            date_mise_en_service, date_maj, nom_amenageur, nom_operateur, contact_operateur
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)

# Commit the changes to the database
mydb.commit()

# Close the cursor and connection
mycur.close()
mydb.close()
