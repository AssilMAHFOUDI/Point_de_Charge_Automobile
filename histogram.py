import mysql.connector
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(
    host="localhost",
    user="userp",
    passwd="0201",
    database="projectbase",
    auth_plugin="mysql_native_password"
)

# List of prise_types
prise_types = ['prise_type_ef', 'prise_type_2', 'prise_type_combo_ccs', 'prise_type_chademo', 'prise_type_autre']

# Execute separate queries for each prise_type and store counts
counts = {}
mycur = mydb.cursor()

for prise_type in prise_types:
    query = f"SELECT SUM({prise_type}) FROM pdc;"
    mycur.execute(query)
    count_result = mycur.fetchone()[0]
    counts[prise_type] = count_result

# Close the cursor and connection
mycur.close()
mydb.close()

# Assign colors for each prise_type
colors = ['blue', 'green', 'orange', 'red', 'purple']

# Create a bar chart using matplotlib with colors
plt.bar(counts.keys(), counts.values(), color=colors)
plt.xlabel('Prise Type')
plt.ylabel('Count')
plt.title('Count of Prise Types in pdc')
plt.show()
