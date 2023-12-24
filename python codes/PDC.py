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

# Create a DataFrame for PDC data
df_pdc = df[['id_pdc_itinerance', 'puissance_nominale', 'prise_type_ef', 'prise_type_2',
             'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre', 'id_station_itinerance']]

# Replace NaN values with appropriate values or handle them as needed
df_pdc = df_pdc.replace({np.nan: None})

# Iterate over the rows and insert data into MySQL table
for index, row in df_pdc.iterrows():
    values = (
        row['id_pdc_itinerance'],
        row['puissance_nominale'],
        row['prise_type_ef'],
        row['prise_type_2'],
        row['prise_type_combo_ccs'],
        row['prise_type_chademo'],
        row['prise_type_autre'],
        row['id_station_itinerance']
    )

    # Insert data into the MySQL table
    mycur.execute("""
        INSERT INTO PDC (
            id_pdc_itinerance, puissance_nominale, prise_type_ef, prise_type_2,
            prise_type_combo_ccs, prise_type_chademo, prise_type_autre, id_station_itinerance
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, values)

# Commit the changes to the database
mydb.commit()

# Close the cursor and connection
mycur.close()
mydb.close()
