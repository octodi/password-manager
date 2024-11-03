#imports
import keyring
import tkinter as tk
import hashlib
from tkinter import ttk
from tkinter import *
import mysql.connector
import random
import os

#Mainwindow executes after entering right Master Password
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        with open("config.txt", "r") as config_file:
            host,username= config_file.read().split()

        password = keyring.get_password("my_password_manager", "mysql_password")

        db = mysql.connector.connect(host=host,user=username,password=password,database="password_manager")
        def create_password_manager_table():
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS password_manager ( id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, website VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL )")
            db.commit()

        create_password_manager_table()

        # Add the Name, Username, Website, and Password fields in tkinter
        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(self)
        name_entry.grid(row=0, column=1)

        username_label = tk.Label(self, text="Username:")
        username_label.grid(row=1, column=0)
        username_entry = tk.Entry(self)
        username_entry.grid(row=1, column=1)

        website_label = tk.Label(self, text="Website:")
        website_label.grid(row=2, column=0)
        website_entry = tk.Entry(self)
        website_entry.grid(row=2, column=1)

        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=3, column=0)
        password_entry = tk.Entry(self, show="*")
        password_entry.grid(row=3, column=1)

        # Password Generate Button
        generate_button = tk.Button(self, text="Generate Password")
        generate_button.grid(row=4, column=2)

        save_button = tk.Button(self, text="Save")
        save_button.grid(row=5, column=1)

        length_label = tk.Label(self, text="Length:")
        length_label.grid(row=4, column=0)

        length_entry = tk.Entry(self)
        length_entry.grid(row=4, column=1)

        #Create Random password of desired length
        def generate_password():
            length = int(length_entry.get())
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-"
            password = "".join(random.choice(chars) for i in range(length))
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)


        generate_button["command"] = generate_password

        def save_details(name, username, website, password):
            cursor = db.cursor()
            cursor.execute("INSERT INTO password_manager (id, name, username, website, password) VALUES (NULL, %s, %s, %s, %s)", (name, username, website, password))
            db.commit()
            show_details()
        # Attach save_details function to the Save button
        save_button["command"] = lambda: save_details(
            name_entry.get(),
            username_entry.get(),
            website_entry.get(),
            password_entry.get()
            )

        # Treeview widget to show the saved details
        tree = ttk.Treeview(self)
        tree["columns"] = ("name","username", "website", "password")
        tree.heading("name", text="Name")
        tree.heading("username", text="Username")
        tree.heading("website", text="Website")
        tree.heading("password", text="Password")
        tree.grid(row=6, column=0, columnspan=2)

        # Delete the selected item from the Treeview widget and the database
        def delete_item():
            item = tree.selection()[0]
            item_values = tree.item(item)["values"]
            cursor = db.cursor()
            cursor.execute("DELETE FROM password_manager WHERE name = %s AND username = %s", (item_values[0], item_values[1]))
            db.commit()

            tree.detach(item)

        delete_button = tk.Button(self, text="Delete", command=delete_item)

        delete_button.grid(row=7, column=1, sticky="nsew")
        def show_details():
            for i in tree.get_children():
                tree.delete(i)

            cursor = db.cursor()
            cursor.execute("SELECT * FROM password_manager")
            rows = cursor.fetchall()

            for row in rows:
                tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4]))

        show_details()

#StartPage executes after the MySQL Configuration
class StartPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login/Signup")
        self.logo_img = PhotoImage(file="logo.png")

        label = tk.Label(self, text="Welcome to My Password Manager")
        label.grid(row=0, column=0, columnspan=3)

        canvas = Canvas(self, width=200, height=200)
        canvas.create_image(100, 100, image=self.logo_img)
        canvas.grid(column=1, row=1)

        #Login and Singup Button
        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.grid(row=2, column=0)
        signup_button = tk.Button(self, text="Signup", command=self.signup)
        signup_button.grid(row=2, column=2)

        with open("config.txt", "r") as config_file:
            host, username = config_file.read().split()

        # Retrieve the MySQL password from keyring
        password = keyring.get_password("my_password_manager", "mysql_password")

        db = mysql.connector.connect(
        host=host,
        user=username,
        password=password
        )
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS password_manager")
        db.commit()
        db.close()
        cursor.close()

        #Creating user_details table in password_manager database
        def user_details_table():
            with open("config.txt", "r") as config_file:
                host,username= config_file.read().split()
            # Retrieve the MySQL password from keyring
            password = keyring.get_password("my_password_manager", "mysql_password")
            mydb = mysql.connector.connect(host=host,user=username,password=password,database="password_manager")
            cursor = mydb.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS user_details ( id INTEGER PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255) NOT NULL, cred VARCHAR(255) NOT NULL )")
            mydb.commit()
            cursor.close()

        user_details_table()

    #Signup Window
    def signup(self):
        signup_window = tk.Toplevel(self)
        signup_window.title("Signup")

        email_label = tk.Label(signup_window, text="Email:")
        email_label.grid(row=0, column=0)
        email_entry = tk.Entry(signup_window)
        email_entry.grid(row=0, column=1)

        cred_label = tk.Label(signup_window, text="Master Password:")
        cred_label.grid(row=1, column=0)
        cred_entry = tk.Entry(signup_window, show="*")
        cred_entry.grid(row=1, column=1)

        submit_button = tk.Button(signup_window, text="Submit", command=lambda: self.save_signup_details(signup_window,email_entry.get(), cred_entry.get()))
        submit_button.grid(row=2, column=1)

    #Saving details got from Signup window
    def save_signup_details(self, window, email, cred):
        with open("config.txt", "r") as config_file:
            host, username = config_file.read().split()
        # Retrieve the MySQL password from keyring
        password = keyring.get_password("my_password_manager", "mysql_password")
        db = mysql.connector.connect(host=host, user=username, password=password, database="password_manager")
        cursor = db.cursor()
        cursor.execute("SELECT email FROM user_details WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            error_message = tk.Label(window, text="This Email Already Exists")
            error_message.grid(row=3, column=0, columnspan=2)
        else:
            hashed_password = hashlib.sha512(cred.encode()).hexdigest()

            # Save the email and hashed password to the SQL table
            cursor.execute("INSERT INTO user_details (email, cred) VALUES (%s, %s)", (email, hashed_password))
            db.commit()
            cursor.close()
            db.close()
            window.destroy()
            self.login()

    #Login Window
    def login(self):
        # Create a new window for login
        login_window = tk.Toplevel(self)
        login_window.title("Login")

        email_label = tk.Label(login_window, text="Email:")
        email_label.grid(row=0, column=0)
        email_entry = tk.Entry(login_window)
        email_entry.grid(row=0, column=1)

        cred_label = tk.Label(login_window, text="Master Password:")
        cred_label.grid(row=1, column=0)
        cred_entry = tk.Entry(login_window, show="*")
        cred_entry.grid(row=1, column=1)

        submit_button = tk.Button(login_window, text="Submit", command=lambda: self.check_user(login_window,email_entry.get(), cred_entry.get()))
        submit_button.grid(row=2, column=1)

    #Checking if the user exists in the table user_details
    def check_user(self, window, email, cred):
        with open("config.txt", "r") as config_file:
            host, username = config_file.read().split()
        # Retrieve the MySQL password from keyring
        password = keyring.get_password("my_password_manager", "mysql_password")
        db = mysql.connector.connect(host=host, user=username, password=password, database="password_manager")
        cursor = db.cursor()
        cursor.execute("SELECT cred FROM user_details WHERE email = %s", (email,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            print("Please Signup first")
        else:
            # Hash the entered password
            hashed_password = hashlib.sha512(cred.encode()).hexdigest()

            if hashed_password == result[0][0]:
                self.destroy()
                main_window = MainWindow()
                main_window.mainloop()
            else:
                error_message = tk.Label(window, text="Incorrect password. Please try again.")
                error_message.grid(row=3, column=0, columnspan=2)

#MySQL configuration window
class ConfigWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MySQL Configuration")
        #Enters for Host, Username, Passowrd
        host_label = tk.Label(self, text="Host:")
        host_label.grid(row=0, column=0)
        self.host_entry = tk.Entry(self)
        self.host_entry.grid(row=0, column=1)

        user_label = tk.Label(self, text="Username:")
        user_label.grid(row=1, column=0)
        self.user_entry = tk.Entry(self)
        self.user_entry.grid(row=1, column=1)

        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1)

        submit_button = tk.Button(self, text="Submit", command=self.submit_config)
        submit_button.grid(row=3, column=1)

    #Save config to config.txt file
    def submit_config(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        # Store the MySQL password using keyring
        keyring.set_password("my_password_manager", "mysql_password", password)

        # Write the host and user to the config file
        with open("config.txt", "w") as config_file:
            config_file.write(host + "\n")
            config_file.write(user + "\n")

        self.destroy()
        start_page = StartPage()
        start_page.mainloop()

def config_file_check():
    if os.path.isfile("config.txt") and os.path.getsize("config.txt") > 0:
        start_page=StartPage()
        start_page.mainloop()
    else:
        mysql_config=ConfigWindow()
        mysql_config.mainloop()

config_file_check()
