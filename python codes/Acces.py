import mysql.connector
import pandas as pd
import numpy as np

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

# Create a DataFrame for Acces data
df_acces = df[['id_station_itinerance', 'condition_acces', 'reservation', 'horaires']]

# Replace NaN values with appropriate values or handle them as needed
df_acces = df_acces.replace({np.nan: None})

# Iterate over the rows and insert data into MySQL table
for index, row in df_acces.iterrows():
    values = (
        row['id_station_itinerance'],
        row['condition_acces'],
        row['reservation'],
        row['horaires']
    )

    # Insert data into the MySQL table
    mycur.execute("""
        INSERT INTO Acces (
            id_station_itinerance, condition_acces, reservation, horaires
        ) VALUES (%s, %s, %s, %s)
    """, values)

# Commit the changes to the database
mydb.commit()

# Close the cursor and connection
mycur.close()
mydb.close()
