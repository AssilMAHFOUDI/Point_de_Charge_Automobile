import mysql.connector
import pandas as pd

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="userp",
    passwd="0201",
    database="projectbase",
    auth_plugin="mysql_native_password"
)

# Create a cursor
mycur = mydb.cursor()

# Read CSV file into a DataFrame
#csv_file_path = r"C:\Users\assil\Desktop\mcd projet\Point_de_Charge_Automobile\sigeif.csv"  # Replace with the actual path to your CSV file
csv_file_path=r"C:\Users\assil\Desktop\mcd projet\Point_de_Charge_Automobile\mobive.csv"
df = pd.read_csv(csv_file_path)

# Extract relevant columns from the DataFrame
df_selected_columns = df[['nom_amenageur', 'contact_amenageur']]

# Iterate over the rows and insert data into MySQL table
for index, row in df_selected_columns.iterrows():
    nom_amenageur = row['nom_amenageur']
    contact_amenageur = row['contact_amenageur']
    
    # Insert or update data into the MySQL table
    mycur.execute("""
        INSERT INTO amenageur (nom_amenageur, contact_amenageur) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE contact_amenageur = VALUES(contact_amenageur)
    """, (nom_amenageur, contact_amenageur))
    
    

# Commit the changes to the database
mydb.commit()

# Close the cursor and connection
mycur.close()
mydb.close()



