import mysql.connector
import matplotlib.pyplot as plt
import random

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="userp",
    passwd="0201",
    database="projectbase",
    auth_plugin="mysql_native_password"
)

# Query to count the number of rows for each 2-digit code_insee_commune prefix
count_query = """
SELECT LEFT(code_insee_commune, 2) AS insee_prefix, COUNT(*) AS count
FROM station
GROUP BY insee_prefix;
"""

# Execute the query and store the results
mycur = mydb.cursor()
mycur.execute(count_query)
query_results = mycur.fetchall()

# Close the cursor and connection
mycur.close()
mydb.close()

# Extracting data for plotting
insee_prefixes = [result[0] for result in query_results]
counts = [result[1] for result in query_results]

# Generating a random color for each bar
colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
          for i in range(len(insee_prefixes))]

# Plotting the bar chart
plt.figure(figsize=(12, 6))

plt.bar(insee_prefixes, counts, color=colors)
plt.xlabel('Departement')
plt.ylabel('Count of stations')
plt.title('Count of stations by Department')

# Show the plots
plt.tight_layout()
plt.show()
