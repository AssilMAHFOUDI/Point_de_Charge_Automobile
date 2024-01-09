import customtkinter as ctk
import mysql.connector
import tkinter as tk
from tkinter import ttk

# Global list to store the displayed PDC IDs
displayed_pdc_ids = []

def display_query_results(query, tree):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="userp",
            passwd="0201",
            database="projectbase",
            auth_plugin="mysql_native_password"
        )
        mycur = mydb.cursor()
        mycur.execute(query)
        columns = [desc[0] for desc in mycur.description]
        results = mycur.fetchall()

        tree["columns"] = columns
        tree.delete(*tree.get_children())
        for col in columns:
            tree.heading(col, text=col, anchor=tk.CENTER)
            tree.column(col, width=300, minwidth=200, stretch=tk.NO)

        for i, row in enumerate(results):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert("", tk.END, values=row, tags=(tag,))

        mycur.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error: ", err)

def create_input_dialog(title, label_text, on_submit):
    dialog = ctk.CTkToplevel(app)
    dialog.title(title)
    dialog.geometry("300x150")

    label = ctk.CTkLabel(dialog, text=label_text)
    label.pack(pady=10)

    entry = ctk.CTkEntry(dialog)
    entry.pack(pady=10)

    submit_button = ctk.CTkButton(dialog, text="Submit", command=lambda: on_submit(entry.get(), dialog))
    submit_button.pack(pady=10)

def display_stations_by_insee(tree):
    def submit_insee_code(code, window):
        if code:
            query = f"SELECT id_station_itinerance, nom_enseigne, nom_station, code_insee_commune, nbre_pdc FROM Station WHERE code_insee_commune LIKE '{code}%';"
            display_query_results(query, tree)
        window.destroy()

    create_input_dialog("Enter INSEE Code", "Please enter the INSEE code:", submit_insee_code)

def display_stations_by_city(tree):
    def submit_city_name(name, window):
        if name:
            query = f"SELECT id_station_itinerance, nom_enseigne, nom_station, code_insee_commune, nbre_pdc FROM Station WHERE nom_station LIKE '%{name}%';"
            display_query_results(query, tree)
        window.destroy()

    create_input_dialog("Enter City Name", "Please enter the name of the city:", submit_city_name)

def display_pdc_information(tree):
    def submit_station_id(station_id, window):
        global displayed_pdc_ids
        if station_id:
            query = f"SELECT * FROM PDC WHERE id_station_itinerance = '{station_id}';"
            displayed_pdc_ids = fetch_pdc_ids(query)  # Fetch and store PDC IDs
            display_query_results(query, tree)
            show_tarification_button.pack(pady=10)  # Show the tarification button
        window.destroy()

    create_input_dialog("Enter Station ID", "Please enter the station ID:", submit_station_id)

def fetch_pdc_ids(query):
    pdc_ids = []
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="userp",
            passwd="0201",
            database="projectbase",
            auth_plugin="mysql_native_password"
        )
        mycur = mydb.cursor()
        mycur.execute(query)
        for row in mycur.fetchall():
            pdc_ids.append(row[0])  # Assuming the first column is the PDC ID
        mycur.close()
        mydb.close()
    except mysql.connector.Error as err:
        print("Error: ", err)
    return pdc_ids

def show_tarification(tree):
    global displayed_pdc_ids
    for pdc_id in displayed_pdc_ids:
        query = f"SELECT * FROM Tarification WHERE id_pdc_itinerance = '{pdc_id}';"
        display_query_results(query, tree)

def show_station_buttons():
    display_all_button.pack(pady=10)
    display_by_insee_button.pack(pady=10)
    display_by_city_button.pack(pady=10)
    display_pdc_button.pack(pady=10)
    return_button.pack(pady=10)
    amenageur_button.pack_forget()
    operateur_button.pack_forget()
    station_button.pack_forget()

def show_main_buttons():
    amenageur_button.pack(pady=10)
    operateur_button.pack(pady=10)
    station_button.pack(pady=10)
    display_all_button.pack_forget()
    display_by_insee_button.pack_forget()
    display_by_city_button.pack_forget()
    display_pdc_button.pack_forget()
    show_tarification_button.pack_forget()
    return_button.pack_forget()

def station_button_click():
    show_station_buttons()

# Create the main window
app = ctk.CTk()
app.title("Station Management System")
app.geometry("800x600")
app.configure(bg='#87CEEB')

frame = ctk.CTkFrame(app)
frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

tree = ttk.Treeview(frame)
tree.pack(side=tk.LEFT, fill=ctk.BOTH, expand=True)
tree.tag_configure('oddrow', background='white')
tree.tag_configure('evenrow', background='#A7CEEB')

scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(xscrollcommand=scrollbar.set)

# Buttons for station display options
display_all_button = ctk.CTkButton(app, text="Display All Stations", command=lambda: display_query_results("SELECT id_station_itinerance, nom_enseigne, nom_station, code_insee_commune, nbre_pdc FROM Station;", tree), fg_color="#87CEEB", text_color="black")
display_by_insee_button = ctk.CTkButton(app, text="Display Stations by INSEE Code", command=lambda: display_stations_by_insee(tree), fg_color="#87CEEB", text_color="black")
display_by_city_button = ctk.CTkButton(app, text="Display Stations by City Name", command=lambda: display_stations_by_city(tree), fg_color="#87CEEB", text_color="black")
display_pdc_button = ctk.CTkButton(app, text="Display PDC Information", command=lambda: display_pdc_information(tree), fg_color="#87CEEB", text_color="black")
show_tarification_button = ctk.CTkButton(app, text="Show Tarification", command=lambda: show_tarification(tree), fg_color="#87CEEB", text_color="black")
return_button = ctk.CTkButton(app, text="Return", command=show_main_buttons, fg_color="#87CEEB", text_color="black")

# Initial buttons
amenageur_button = ctk.CTkButton(app, text="Display Amenageur", command=lambda: display_query_results("SELECT * FROM Amenageur;", tree), fg_color="#87CEEB", text_color="black")
operateur_button = ctk.CTkButton(app, text="Display Operateur", command=lambda: display_query_results("SELECT * FROM Operateur;", tree), fg_color="#87CEEB", text_color="black")
station_button = ctk.CTkButton(app, text="Display Stations", command=station_button_click, fg_color="#87CEEB", text_color="black")

# Initially display the main buttons
show_main_buttons()

app.mainloop()
