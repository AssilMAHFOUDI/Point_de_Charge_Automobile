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

# Create a DataFrame for Tarification data
df_tarification = df[['id_pdc_itinerance', 'gratuit', 'paiement_acte', 'paiement_cb',
                      'paiement_autre', 'tarification']]

#Replace NaN values with "Unknown" for specified columns
columns_to_replace = ['tarification']
df[columns_to_replace] = df[columns_to_replace].fillna('Unknown')


# Replace NaN values with appropriate values or handle them as needed
df_tarification = df_tarification.replace({np.nan: None})

# Iterate over the rows and insert data into MySQL table
for index, row in df_tarification.iterrows():
    values = (
        row['id_pdc_itinerance'],
        row['gratuit'],
        row['paiement_acte'],
        row['paiement_cb'],
        row['paiement_autre'],
        row['tarification']
    )

    # Insert data into the MySQL table
    mycur.execute("""
        INSERT INTO Tarification (
            id_pdc_itinerance, gratuit, paiement_acte, paiement_cb,
            paiement_autre, tarification
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, values)

# Commit the changes to the database
mydb.commit()

# Close the cursor and connection
mycur.close()
mydb.close()
