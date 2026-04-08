import json
import random
import string
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

# ---------------------------- GENERATE KEY (RUN ONLY ONCE) ---------------------------- #
# Uncomment below 2 lines ONLY once to generate key
# key = Fernet.generate_key()
# print(key)

# After running once, paste your key here and comment above lines
KEY = b'oVcvBwqgRHLjh4aGdtKAwg4L_rMVIr8QZpkA2b7yyx8='
fernet = Fernet(KEY)

# ---------------------------- PASSWORD GENERATOR ---------------------------- #
def generate_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(characters) for _ in range(12))

    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ---------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website == "" or password == "":
        messagebox.showwarning(title="Error", message="Fields cannot be empty!")
        return

    encrypted_password = fernet.encrypt(password.encode()).decode()

    new_data = {
        website: {
            "username": username,
            "password": encrypted_password
        }
    }

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

    messagebox.showinfo(title="Success", message="Password saved securely!")

# ---------------------------- SEARCH PASSWORD ---------------------------- #
def search():
    website = website_entry.get()

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found!")
        return

    if website in data:
        username = data[website]["username"]
        encrypted_password = data[website]["password"]
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()

        messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {decrypted_password}")
    else:
        messagebox.showerror(title="Not Found", message="No details found!")

# ---------------------------- UI ---------------------------- #
window = Tk()
window.title("Smart Password Manager")
window.config(padx=40, pady=40)

Label(text="Website").grid(row=0, column=0)
Label(text="Email").grid(row=1, column=0)
Label(text="Password").grid(row=2, column=0)

website_entry = Entry(width=30)
website_entry.grid(row=0, column=1)
website_entry.focus()

username_entry = Entry(width=30)
username_entry.grid(row=1, column=1)

password_entry = Entry(width=21)
password_entry.grid(row=2, column=1)

Button(text="Generate", command=generate_password).grid(row=2, column=2)
Button(text="Save", width=36, command=save).grid(row=3, column=1, columnspan=2)
Button(text="Search", command=search).grid(row=0, column=2)

window.mainloop()