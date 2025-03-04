import sqlite3
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from pathlib import Path
import os
import random
import datetime

#-------------------------------Utility Functions-------------------------------#


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Rupert Jay Laureano\Documents\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_hover_button(x, y, width, height, normal_image_path, hover_image_path, command):
    normal_image = PhotoImage(file=relative_to_assets(normal_image_path))
    hover_image = PhotoImage(file=relative_to_assets(hover_image_path))

    button = Button(
        image=normal_image,
        borderwidth=0,
        highlightthickness=0,
        command=command,
        relief="flat"
    )
    button.image = normal_image
    button.place(x=x, y=y, width=width, height=height)

    def on_hover(event):
        button.config(image=hover_image)

    def on_leave(event):
        button.config(image=normal_image)

    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)

#-------------------------------Database Setup-------------------------------#
def create_database():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (fullname TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

#-------------------------------Registration Interface-------------------------------#

def register_user():
    fullname = entry_1.get()
    username = entry_2.get()
    password = entry_3.get()

    if not fullname or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)", (fullname, username, password))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Registration successful!")
    window.destroy()  # Close the registration window
    login_interface()  # Open the login window

def registration_interface():
    global window, entry_1, entry_2, entry_3
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        36.0,
        191.0,
        anchor="nw",
        text="- Users must register using their respective credentials\n\n- Students 10-digit student number\n\n- Athletes: 11-digit number\n\n- Employees and Staff: 9-digit number\n\n- Admins: Must log in using ‘ADMIN’ as the UserId",
        fill="#000000",
        font=("InknutAntiqua Regular", 14 * -1)
    )

    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))
    canvas.create_rectangle(23.0, 151.0, 983.0, 181.0, fill="#FAEECA", outline="")
    canvas.create_text(32.0, 149.0, anchor="nw", text="REGISTRATION FORM", fill="#000000", font=("InknutAntiqua Bold", 18 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(111.0, 53.0, image=image_image_1)

    canvas.create_text(500.0, 196.0, anchor="nw", text="Full Name:", fill="#271717", font=("InknutAntiqua Regular", 12 * -1))
    canvas.create_text(500.0, 270.0, anchor="nw", text="User Id:", fill="#271717", font=("InknutAntiqua Regular", 12 * -1))
    canvas.create_text(500.0, 346.0, anchor="nw", text="Password:", fill="#271717", font=("InknutAntiqua Regular", 12 * -1))

    entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_1.place(x=500.0, y=221.0, width=315.0, height=34.0)

    entry_2 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_2.place(x=500.0, y=295.0, width=315.0, height=34.0)

    entry_3 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*")
    entry_3.place(x=500.0, y=371.0, width=315.0, height=34.0)

    button_1 = Button(
        text="Register",
        borderwidth=0,
        highlightthickness=0,
        command=register_user,
        relief="flat"
    )
    button_1.place(x=500.0, y=447.0, width=315.0, height=36.0)

    button_2 = Button(
        text="Already Registered? Login",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), login_interface()],
        relief="flat"
    )
    button_2.place(x=500.0, y=489.0, width=315.0, height=36.0)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Login Interface-------------------------------#
def login():
    username = entry_4.get()
    password = entry_5.get()

    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Successful", f"Welcome, {user[0]}!")
        open_customer_interface()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def login_interface():
    global window, entry_4, entry_5
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen", fill="#E6B528", font=("Avenir Next", 36 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(111.0, 53.0, image=image_image_1)

    entry_4 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_4.place(x=342.0, y=294.0, width=315.0, height=34.0)

    canvas.create_text(343.0, 269.0, anchor="nw", text="User Id:", fill="#271717", font=("Avenir Next", 12 * -1))

    entry_5 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*")
    entry_5.place(x=342.0, y=366.0, width=315.0, height=34.0)

    canvas.create_text(343.0, 341.0, anchor="nw", text="Password:", fill="#271717", font=("Avenir Next", 12 * -1))

    # Button 3 (Login) with hover effect
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=login,
        relief="flat"
    )
    button_3.place(x=393.0, y=431.0, width=213.0, height=39.0)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Customer Interface-------------------------------#
def open_customer_interface():
    window.destroy()
    customer_interface()

def open_vmes_canteen_interface():
    window.destroy()
    vmes_canteen_interface()

def open_angelspizza_canteen_interface():
    window.destroy()
    angelspizza_canteen_interface()

def open_belgianwaffle_canteen_interface():
    window.destroy()
    belgianwaffle_canteen_interface()

def open_jamaican_canteen_interface():
    window.destroy()
    jamaican_canteen_interface()

def open_chefbabs_canteen_interface():
    window.destroy()
    chefbabs_canteen_interface()

def open_vardasburger_canteen_interface():
    window.destroy()
    vardasburger_canteen_interface()

def customer_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(111.0, 53.0, image=image_image_1)

    # Buttons for different canteen options
    create_hover_button(81.0, 203.0, 361.0, 65.0, "button_4.png", "button_hover_4.png", open_vmes_canteen_interface)
    create_hover_button(81.0, 318.0, 361.0, 65.0, "button_5.png", "button_hover_5.png", open_chefbabs_canteen_interface)
    create_hover_button(81.0, 454.0, 361.0, 65.0, "button_6.png", "button_hover_6.png", open_vardasburger_canteen_interface)
    create_hover_button(555.0, 203.0, 361.0, 65.0, "button_7.png", "button_hover_7.png", open_angelspizza_canteen_interface)
    create_hover_button(555.0, 318.0, 361.0, 65.0, "button_8.png", "button_hover_8.png", open_belgianwaffle_canteen_interface)
    create_hover_button(555.0, 454.0, 361.0, 65.0, "button_9.png", "button_hover_9.png", open_jamaican_canteen_interface)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Vmes Canteen Interface-------------------------------#
def vmes_canteen_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Menu rectangles
    menu_rectangles = [
        (15.0, 200.0, 217.0, 253.0),
        (15.0, 260.0, 217.0, 313.0),
        (15.0, 320.0, 217.0, 373.0),
        (15.0, 380.0, 217.0, 433.0),
        (15.0, 442.0, 217.0, 495.0),
        (15.0, 504.0, 217.0, 557.0)
    ]

    for rect in menu_rectangles:
        canvas.create_rectangle(*rect, fill="#D9D9D9", outline="")

    # Menu items structure: (x, y, text)
    menu_items = [
        (20.0, 217.0, "Chicken Adobo....................P90"),
        (21.0, 277.0, "Pork Giniling.......................P90"),
        (20.0, 337.0, "Chicken Curry.....................P90"),
        (20.0, 398.0, "Chicken Inasal....................P90"),
        (20.0, 460.0, "Adobong Sitao....................P90"),
        (20.0, 523.0, "Extra Rice..........................P20")
    ]

    # Create menu texts with explicit text parameter
    for x, y, text in menu_items:
        canvas.create_text(
            x,
            y,
            text=text,  # Explicit text parameter added here
            anchor="nw",
            fill="#000000",
            font=("Inter", 13 * -1)
        )

    rect_id = canvas.create_rectangle(
        330, 146, 672, 531, fill="#D9D9D9", outline=""
    )

    # Menu title
    canvas.create_rectangle(15.0, 142.0, 317.0, 194.0, fill="#E6B528", outline="")
    canvas.create_text(122.0, 142.0, anchor="nw", text="Menu", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen ", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    # Display area
    canvas.create_rectangle(682.0, 193.36483764648438, 984.0, 531.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(682.0, 140.0, 984.0, 193.36483001708984, fill="#E6B528", outline="")
    canvas.create_text(760.0, 140.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Load images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(111.0, 53.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(501.0, 338.0, image=image_image_2)

    image_image_3 = PhotoImage(file=relative_to_assets("Chicken Adobo.png"))
    image_image_4 = PhotoImage(file=relative_to_assets("Pork Giniling.png"))
    image_image_5 = PhotoImage(file=relative_to_assets("Chicken Curry.png"))
    image_image_6 = PhotoImage(file=relative_to_assets("Chicken Inasal.png"))
    image_image_7 = PhotoImage(file=relative_to_assets("Adobong Sitao.png"))
    image_image_8 = PhotoImage(file=relative_to_assets("Extra Rice.png"))

    # Function to display food images
    def display_food(image):
        canvas.itemconfig(image_2, image=image)

    # Function to add item to order list
    order_list = []

    def add_to_order():
        # Get the currently displayed food item
        current_image = canvas.itemcget(image_2, "image")
        if current_image == str(image_image_3):
            order_list.append("Chicken Adobo - P90")
        elif current_image == str(image_image_4):
            order_list.append("Pork Giniling - P90")
        elif current_image == str(image_image_5):
            order_list.append("Chicken Curry - P90")
        elif current_image == str(image_image_6):
            order_list.append("Chicken Inasal - P90")
        elif current_image == str(image_image_7):
            order_list.append("Adobong Sitao - P90")
        elif current_image == str(image_image_8):
            order_list.append("Extra Rice - P20")
        update_order_list()

    # Function to remove item from order list
    def remove_from_order():
        if order_list:
            order_list.pop()
            update_order_list()

    # Function to update the order list display
    def update_order_list():
        canvas.delete("order_text")
        y_offset = 210
        for item in order_list:
            canvas.create_text(690.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1), tags="order_text")
            y_offset += 30

    # Function to handle order button click
    def place_order():
        if order_list:
            window.destroy()  # Close the current canteen interface
            payment_interface(order_list)  # Open the payment interface with the order list
        else:
            messagebox.showerror("Error", "No items in the order list.")

    # Buttons for displaying food images
    button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
    button_13 = Button(image=button_image_13, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_3), relief="flat")
    button_13.place(x=225.0, y=200.0, width=92.0, height=53.0)

    button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
    button_14 = Button(image=button_image_14, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_4), relief="flat")
    button_14.place(x=225.0, y=260.0, width=93.0, height=53.0)

    button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
    button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_5), relief="flat")
    button_15.place(x=225.0, y=320.0, width=92.0, height=53.0)

    button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
    button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_6), relief="flat")
    button_16.place(x=225.0, y=380.0, width=92.0, height=53.0)

    button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
    button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_7), relief="flat")
    button_17.place(x=225.0, y=442.0, width=92.0, height=53.0)

    button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
    button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_8), relief="flat")
    button_18.place(x=225.0, y=504.0, width=92.0, height=53.0)

    # Add to order button
    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(image=button_image_10, borderwidth=0, highlightthickness=0, command=add_to_order, relief="flat")
    button_10.place(x=331.0, y=539.0, width=169.0, height=33.0)

    # Remove from order button
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(image=button_image_11, borderwidth=0, highlightthickness=0, command=remove_from_order, relief="flat")
    button_11.place(x=506.0, y=539.0, width=166.0, height=33.0)

    # Place order button
    button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
    button_12 = Button(image=button_image_12, borderwidth=0, highlightthickness=0, command=place_order, relief="flat")
    button_12.place(x=682.0, y=540.0, width=302.0, height=33.0)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Angel's Pizza Interface-------------------------------#
def angelspizza_canteen_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Menu rectangles
    menu_rectangles = [
        (15.0, 200.0, 217.0, 253.0),
        (15.0, 260.0, 217.0, 313.0),
        (15.0, 320.0, 217.0, 373.0),
        (15.0, 380.0, 217.0, 433.0),
        (15.0, 442.0, 217.0, 495.0),
        (15.0, 504.0, 217.0, 557.0)
    ]

    for rect in menu_rectangles:
        canvas.create_rectangle(*rect, fill="#D9D9D9", outline="")

    # Menu items structure: (x, y, text)
    menu_items = [
        (20.0, 217.0, "Creamy Spinach x1 slice......P95"),
        (21.0, 277.0, "All Meat x1 slice..................P95"),
        (20.0, 337.0, "Angel's Pepperoni x1 slice....P95"),
        (20.0, 398.0, "Garlic Shrimp x1 slice..........P95"),
        (20.0, 460.0, "Angel's Supreme x1 slice.....P95"),
        (20.0, 523.0, "Pizza Overload x1 slice........P95")
    ]

    # Create menu texts with explicit text parameter
    for x, y, text in menu_items:
        canvas.create_text(
            x,
            y,
            text=text,  # Explicit text parameter added here
            anchor="nw",
            fill="#000000",
            font=("Inter", 13 * -1)
        )

    rect_id = canvas.create_rectangle(
        330, 146, 672, 531, fill="#D9D9D9", outline=""
    )

    # Menu title
    canvas.create_rectangle(15.0, 142.0, 317.0, 194.0, fill="#E6B528", outline="")
    canvas.create_text(122.0, 142.0, anchor="nw", text="Menu", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen ", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    # Display area
    canvas.create_rectangle(682.0, 193.36483764648438, 984.0, 531.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(682.0, 140.0, 984.0, 193.36483001708984, fill="#E6B528", outline="")
    canvas.create_text(760.0, 140.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Load images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(111.0, 53.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(501.0, 338.0, image=image_image_2)

    image_image_9 = PhotoImage(file=relative_to_assets("Creamy Spinach Dip.png"))
    image_image_10 = PhotoImage(file=relative_to_assets("All Meat.png"))
    image_image_11 = PhotoImage(file=relative_to_assets("Angel's Pepperoni.png"))
    image_image_12 = PhotoImage(file=relative_to_assets("Garlic Shrimp.png"))
    image_image_13 = PhotoImage(file=relative_to_assets("Angel's Supreme.png"))
    image_image_14 = PhotoImage(file=relative_to_assets("Pizza Overload.png"))

    # Function to display food images
    def display_food(image):
        canvas.itemconfig(image_2, image=image)

    # Function to add item to order list
    order_list = []

    def add_to_order():
        # Get the currently displayed food item
        current_image = canvas.itemcget(image_2, "image")
        if current_image == str(image_image_9):
            order_list.append("Creamy Spinach Dip - P95")
        elif current_image == str(image_image_10):
            order_list.append("All Meat - P95")
        elif current_image == str(image_image_11):
            order_list.append("Angel's Pepperoni - P95")
        elif current_image == str(image_image_12):
            order_list.append("Garlic Shrimp - P95")
        elif current_image == str(image_image_13):
            order_list.append("Angel's Supreme - P95")
        elif current_image == str(image_image_14):
            order_list.append("Pizza Overload - P95")
        update_order_list()

    # Function to remove item from order list
    def remove_from_order():
        if order_list:
            order_list.pop()
            update_order_list()

    # Function to update the order list display
    def update_order_list():
        canvas.delete("order_text")
        y_offset = 210
        for item in order_list:
            canvas.create_text(690.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1), tags="order_text")
            y_offset += 30

    # Function to handle order button click
    def place_order():
        if order_list:
            window.destroy()  # Close the current canteen interface
            payment_interface(order_list)  # Open the payment interface with the order list
        else:
            messagebox.showerror("Error", "No items in the order list.")

    # Buttons for displaying food images
    button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
    button_13 = Button(image=button_image_13, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_9), relief="flat")
    button_13.place(x=225.0, y=200.0, width=92.0, height=53.0)

    button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
    button_14 = Button(image=button_image_14, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_10), relief="flat")
    button_14.place(x=225.0, y=260.0, width=93.0, height=53.0)

    button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
    button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_11), relief="flat")
    button_15.place(x=225.0, y=320.0, width=92.0, height=53.0)

    button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
    button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_12), relief="flat")
    button_16.place(x=225.0, y=380.0, width=92.0, height=53.0)

    button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
    button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_13), relief="flat")
    button_17.place(x=225.0, y=442.0, width=92.0, height=53.0)

    button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
    button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_14), relief="flat")
    button_18.place(x=225.0, y=504.0, width=92.0, height=53.0)

    # Add to order button
    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(image=button_image_10, borderwidth=0, highlightthickness=0, command=add_to_order, relief="flat")
    button_10.place(x=331.0, y=539.0, width=169.0, height=33.0)

    # Remove from order button
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(image=button_image_11, borderwidth=0, highlightthickness=0, command=remove_from_order, relief="flat")
    button_11.place(x=506.0, y=539.0, width=166.0, height=33.0)

    # Place order button
    button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
    button_12 = Button(image=button_image_12, borderwidth=0, highlightthickness=0, command=place_order, relief="flat")
    button_12.place(x=682.0, y=540.0, width=302.0, height=33.0)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Famous Belgian Waffles Interface-------------------------------#
def belgianwaffle_canteen_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Menu rectangles
    menu_rectangles = [
        (15.0, 200.0, 217.0, 253.0),
        (15.0, 260.0, 217.0, 313.0),
        (15.0, 320.0, 217.0, 373.0),
        (15.0, 380.0, 217.0, 433.0),
        (15.0, 442.0, 217.0, 495.0),
        (15.0, 504.0, 217.0, 557.0)
    ]

    for rect in menu_rectangles:
        canvas.create_rectangle(*rect, fill="#D9D9D9", outline="")

    # Menu items structure: (x, y, text)
    menu_items = [
        (20.0, 217.0, "Banana Chocolate................P75"),
        (21.0, 277.0, "Cookies & Cream.................P75"),
        (20.0, 337.0, "Chocolate Custard................P75"),
        (20.0, 398.0, "Strawberry Custard...............P75"),
        (20.0, 460.0, "Choco Banana PB................P95"),
        (20.0, 523.0, "Blueberry Creamcheese........P95")
    ]

    # Create menu texts with explicit text parameter
    for x, y, text in menu_items:
        canvas.create_text(
            x,
            y,
            text=text,  # Explicit text parameter added here
            anchor="nw",
            fill="#000000",
            font=("Inter", 13 * -1)
        )

    rect_id = canvas.create_rectangle(
        330, 146, 672, 531, fill="#D9D9D9", outline=""
    )

    # Menu title
    canvas.create_rectangle(15.0, 142.0, 317.0, 194.0, fill="#E6B528", outline="")
    canvas.create_text(122.0, 142.0, anchor="nw", text="Menu", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen ", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    # Display area
    canvas.create_rectangle(682.0, 193.36483764648438, 984.0, 531.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(682.0, 140.0, 984.0, 193.36483001708984, fill="#E6B528", outline="")
    canvas.create_text(760.0, 140.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Load images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(111.0, 53.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(501.0, 338.0, image=image_image_2)

    image_image_15 = PhotoImage(file=relative_to_assets("Banana Chocolate.png"))
    image_image_16 = PhotoImage(file=relative_to_assets("Cookies & Cream.png"))
    image_image_17 = PhotoImage(file=relative_to_assets("Chocolate Custard.png"))
    image_image_18 = PhotoImage(file=relative_to_assets("Strawberry Custard.png"))
    image_image_19 = PhotoImage(file=relative_to_assets("Choco Banana Peanut Butter.png"))
    image_image_20 = PhotoImage(file=relative_to_assets("Blueberry Creamcheese.png"))

    # Function to display food images
    def display_food(image):
        canvas.itemconfig(image_2, image=image)
 
    # Function to add item to order list
    order_list = []

    def add_to_order():
        # Get the currently displayed food item
        current_image = canvas.itemcget(image_2, "image")
        if current_image == str(image_image_15):
            order_list.append("Banana Chocolate - 75")
        elif current_image == str(image_image_16):
            order_list.append("Cookies & Cream - P75")
        elif current_image == str(image_image_17):
            order_list.append("Chocolate Custard - P75")
        elif current_image == str(image_image_18):
            order_list.append("Strawberry Custard - P95")
        elif current_image == str(image_image_19):
            order_list.append("Choco Banana Peanut Butter - P95")
        elif current_image == str(image_image_20):
            order_list.append("Blueberry Creamcheese - P95")
        update_order_list()

    # Function to remove item from order list
    def remove_from_order():
        if order_list:
            order_list.pop()
            update_order_list()

    # Function to update the order list display
    def update_order_list():
        canvas.delete("order_text")
        y_offset = 210
        for item in order_list:
            canvas.create_text(690.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1), tags="order_text")
            y_offset += 30

    # Function to handle order button click
    def place_order():
        if order_list:
            window.destroy()  # Close the current canteen interface
            payment_interface(order_list)  # Open the payment interface with the order list
        else:
            messagebox.showerror("Error", "No items in the order list.")

    # Buttons for displaying food images
    button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
    button_13 = Button(image=button_image_13, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_15), relief="flat")
    button_13.place(x=225.0, y=200.0, width=92.0, height=53.0)

    button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
    button_14 = Button(image=button_image_14, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_16), relief="flat")
    button_14.place(x=225.0, y=260.0, width=93.0, height=53.0)

    button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
    button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_17), relief="flat")
    button_15.place(x=225.0, y=320.0, width=92.0, height=53.0)

    button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
    button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_18), relief="flat")
    button_16.place(x=225.0, y=380.0, width=92.0, height=53.0)

    button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
    button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_19), relief="flat")
    button_17.place(x=225.0, y=442.0, width=92.0, height=53.0)

    button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
    button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_20), relief="flat")
    button_18.place(x=225.0, y=504.0, width=92.0, height=53.0)

    # Add to order button
    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(image=button_image_10, borderwidth=0, highlightthickness=0, command=add_to_order, relief="flat")
    button_10.place(x=331.0, y=539.0, width=169.0, height=33.0)

    # Remove from order button
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(image=button_image_11, borderwidth=0, highlightthickness=0, command=remove_from_order, relief="flat")
    button_11.place(x=506.0, y=539.0, width=166.0, height=33.0)

    # Place order button
    button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
    button_12 = Button(image=button_image_12, borderwidth=0, highlightthickness=0, command=place_order, relief="flat")
    button_12.place(x=682.0, y=540.0, width=302.0, height=33.0)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Jamaican Interface-------------------------------#
def jamaican_canteen_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Menu rectangles
    menu_rectangles = [
        (15.0, 200.0, 217.0, 253.0),
        (15.0, 260.0, 217.0, 313.0),
        (15.0, 320.0, 217.0, 373.0),
        (15.0, 380.0, 217.0, 433.0),
        (15.0, 442.0, 217.0, 495.0),
        (15.0, 504.0, 217.0, 557.0)
    ]

    for rect in menu_rectangles:
        canvas.create_rectangle(*rect, fill="#D9D9D9", outline="")

    # Menu items structure: (x, y, text)
    menu_items = [
        (20.0, 217.0, "de Original Beef...................P50"),
        (21.0, 277.0, "Beef Pinatubo......................P50"),
        (20.0, 337.0, "Cheezy Beef........................P55"),
        (20.0, 398.0, "Chezzy Beef Pinatubo..........P55"),
        (20.0, 460.0, "Cheezy Tuna.......................P55"),
        (20.0, 523.0, "Beefy Mushroom.................P55")
    ]

    # Create menu texts with explicit text parameter
    for x, y, text in menu_items:
        canvas.create_text(
            x,
            y,
            text=text,  # Explicit text parameter added here
            anchor="nw",
            fill="#000000",
            font=("Inter", 13 * -1)
        )

    rect_id = canvas.create_rectangle(
        330, 146, 672, 531, fill="#D9D9D9", outline=""
    )

    # Menu title
    canvas.create_rectangle(15.0, 142.0, 317.0, 194.0, fill="#E6B528", outline="")
    canvas.create_text(122.0, 142.0, anchor="nw", text="Menu", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen ", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    # Display area
    canvas.create_rectangle(682.0, 193.36483764648438, 984.0, 531.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(682.0, 140.0, 984.0, 193.36483001708984, fill="#E6B528", outline="")
    canvas.create_text(760.0, 140.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Load images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(111.0, 53.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(501.0, 338.0, image=image_image_2)

    image_image_21 = PhotoImage(file=relative_to_assets("Original Beef.png"))
    image_image_22 = PhotoImage(file=relative_to_assets("Beef Pinatubo.png"))
    image_image_23 = PhotoImage(file=relative_to_assets("Cheezy Beef.png"))
    image_image_24 = PhotoImage(file=relative_to_assets("Cheezy Beef Pinatubo.png"))
    image_image_25 = PhotoImage(file=relative_to_assets("Cheezy Tuna.png"))
    image_image_26 = PhotoImage(file=relative_to_assets("Beefy Mushroom.png"))

    # Function to display food images
    def display_food(image):
        canvas.itemconfig(image_2, image=image)
 
    # Function to add item to order list
    order_list = []

    def add_to_order():
        # Get the currently displayed food item
        current_image = canvas.itemcget(image_2, "image")
        if current_image == str(image_image_21):
            order_list.append("de Original Beef - 50")
        elif current_image == str(image_image_22):
            order_list.append("Beef Pinatubo - P50")
        elif current_image == str(image_image_23):
            order_list.append("Cheezy Beef - P55")
        elif current_image == str(image_image_24):
            order_list.append("Cheezy Beef Pinatubo - P55")
        elif current_image == str(image_image_25):
            order_list.append("Cheezy Tuna - P55")
        elif current_image == str(image_image_26):
            order_list.append("Beefy Mushroom - P55")
        update_order_list()

    # Function to remove item from order list
    def remove_from_order():
        if order_list:
            order_list.pop()
            update_order_list()

    # Function to update the order list display
    def update_order_list():
        canvas.delete("order_text")
        y_offset = 210
        for item in order_list:
            canvas.create_text(690.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1), tags="order_text")
            y_offset += 30

    # Function to handle order button click
    def place_order():
        if order_list:
            window.destroy()  # Close the current canteen interface
            payment_interface(order_list)  # Open the payment interface with the order list
        else:
            messagebox.showerror("Error", "No items in the order list.")
    # Buttons for displaying food images
    button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
    button_13 = Button(image=button_image_13, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_21), relief="flat")
    button_13.place(x=225.0, y=200.0, width=92.0, height=53.0)

    button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
    button_14 = Button(image=button_image_14, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_22), relief="flat")
    button_14.place(x=225.0, y=260.0, width=93.0, height=53.0)

    button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
    button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_23), relief="flat")
    button_15.place(x=225.0, y=320.0, width=92.0, height=53.0)

    button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
    button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_24), relief="flat")
    button_16.place(x=225.0, y=380.0, width=92.0, height=53.0)

    button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
    button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_25), relief="flat")
    button_17.place(x=225.0, y=442.0, width=92.0, height=53.0)

    button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
    button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_26), relief="flat")
    button_18.place(x=225.0, y=504.0, width=92.0, height=53.0)

    # Add to order button
    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(image=button_image_10, borderwidth=0, highlightthickness=0, command=add_to_order, relief="flat")
    button_10.place(x=331.0, y=539.0, width=169.0, height=33.0)

    # Remove from order button
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(image=button_image_11, borderwidth=0, highlightthickness=0, command=remove_from_order, relief="flat")
    button_11.place(x=506.0, y=539.0, width=166.0, height=33.0)

    # Place order button
    button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
    button_12 = Button(image=button_image_12, borderwidth=0, highlightthickness=0, command=place_order, relief="flat")
    button_12.place(x=682.0, y=540.0, width=302.0, height=33.0)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Chef Bab's Sisig Interface-------------------------------#
def chefbabs_canteen_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Menu rectangles
    menu_rectangles = [
        (15.0, 200.0, 217.0, 253.0),
        (15.0, 260.0, 217.0, 313.0),
        (15.0, 320.0, 217.0, 373.0),
        (15.0, 380.0, 217.0, 433.0),
        (15.0, 442.0, 217.0, 495.0),
        (15.0, 504.0, 217.0, 557.0)
    ]

    for rect in menu_rectangles:
        canvas.create_rectangle(*rect, fill="#D9D9D9", outline="")

    # Menu items structure: (x, y, text)
    menu_items = [
        (20.0, 217.0, "Crispy Pork Sisig.................P85"),
        (21.0, 277.0, "Pork Dinakdakan.................P85"),
        (20.0, 337.0, "Chicken Sisig......................P85"),
        (20.0, 398.0, "Beef Sisig...........................P90"),
        (20.0, 460.0, "Mushroom Sisig..................P80"),
        (20.0, 523.0, "Tofu Sisig...........................P80")
    ]

    # Create menu texts with explicit text parameter
    for x, y, text in menu_items:
        canvas.create_text(
            x,
            y,
            text=text,  # Explicit text parameter added here
            anchor="nw",
            fill="#000000",
            font=("Inter", 13 * -1)
        )

    rect_id = canvas.create_rectangle(
        330, 146, 672, 531, fill="#D9D9D9", outline=""
    )

    # Menu title
    canvas.create_rectangle(15.0, 142.0, 317.0, 194.0, fill="#E6B528", outline="")
    canvas.create_text(122.0, 142.0, anchor="nw", text="Menu", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen ", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    # Display area
    canvas.create_rectangle(682.0, 193.36483764648438, 984.0, 531.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(682.0, 140.0, 984.0, 193.36483001708984, fill="#E6B528", outline="")
    canvas.create_text(760.0, 140.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Load images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(111.0, 53.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(501.0, 338.0, image=image_image_2)

    image_image_27 = PhotoImage(file=relative_to_assets("Crispy Pork.png"))
    image_image_28 = PhotoImage(file=relative_to_assets("Pork Dinakdakan.png"))
    image_image_29 = PhotoImage(file=relative_to_assets("Chicken Sisig.png"))
    image_image_30 = PhotoImage(file=relative_to_assets("Beef Sisig.png"))
    image_image_31 = PhotoImage(file=relative_to_assets("Mushroom Sisig.png"))
    image_image_32 = PhotoImage(file=relative_to_assets("Tofu Sisig.png"))

    # Function to display food images
    def display_food(image):
        canvas.itemconfig(image_2, image=image)
 
    # Function to add item to order list
    order_list = []

    def add_to_order():
        # Get the currently displayed food item
        current_image = canvas.itemcget(image_2, "image")
        if current_image == str(image_image_27):
            order_list.append("Crispy Pork Sisig - 85")
        elif current_image == str(image_image_28):
            order_list.append("Pork Dinakdakan - P85")
        elif current_image == str(image_image_29):
            order_list.append("Chicken Sisig - P85")
        elif current_image == str(image_image_30):
            order_list.append("Beef Sisig - P90")
        elif current_image == str(image_image_31):
            order_list.append("Mushroom Sisig - P80")
        elif current_image == str(image_image_32):
            order_list.append("Tofu Sisig - P80")
        update_order_list()

    # Function to remove item from order list
    def remove_from_order():
        if order_list:
            order_list.pop()
            update_order_list()

    # Function to update the order list display
    def update_order_list():
        canvas.delete("order_text")
        y_offset = 210
        for item in order_list:
            canvas.create_text(690.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1), tags="order_text")
            y_offset += 30

    # Function to handle order button click
    def place_order():
        if order_list:
            window.destroy()  # Close the current canteen interface
            payment_interface(order_list)  # Open the payment interface with the order list
        else:
            messagebox.showerror("Error", "No items in the order list.")

    # Buttons for displaying food images
    button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
    button_13 = Button(image=button_image_13, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_27), relief="flat")
    button_13.place(x=225.0, y=200.0, width=92.0, height=53.0)

    button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
    button_14 = Button(image=button_image_14, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_28), relief="flat")
    button_14.place(x=225.0, y=260.0, width=93.0, height=53.0)

    button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
    button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_29), relief="flat")
    button_15.place(x=225.0, y=320.0, width=92.0, height=53.0)

    button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
    button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_30), relief="flat")
    button_16.place(x=225.0, y=380.0, width=92.0, height=53.0)

    button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
    button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_31), relief="flat")
    button_17.place(x=225.0, y=442.0, width=92.0, height=53.0)

    button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
    button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_32), relief="flat")
    button_18.place(x=225.0, y=504.0, width=92.0, height=53.0)

    # Add to order button
    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(image=button_image_10, borderwidth=0, highlightthickness=0, command=add_to_order, relief="flat")
    button_10.place(x=331.0, y=539.0, width=169.0, height=33.0)

    # Remove from order button
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(image=button_image_11, borderwidth=0, highlightthickness=0, command=remove_from_order, relief="flat")
    button_11.place(x=506.0, y=539.0, width=166.0, height=33.0)

    # Place order button
    button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
    button_12 = Button(image=button_image_12, borderwidth=0, highlightthickness=0, command=place_order, relief="flat")
    button_12.place(x=682.0, y=540.0, width=302.0, height=33.0)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

    window.resizable(False, False)
    window.mainloop()

#-------------------------------Vardas Burger Interface-------------------------------#
def vardasburger_canteen_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Menu rectangles
    menu_rectangles = [
        (15.0, 200.0, 217.0, 253.0),
        (15.0, 260.0, 217.0, 313.0),
        (15.0, 320.0, 217.0, 373.0),
        (15.0, 380.0, 217.0, 433.0),
        (15.0, 442.0, 217.0, 495.0),
        (15.0, 504.0, 217.0, 557.0)
    ]

    for rect in menu_rectangles:
        canvas.create_rectangle(*rect, fill="#D9D9D9", outline="")

    # Menu items structure: (x, y, text)
    menu_items = [
        (20.0, 217.0, "Quarter Pounder..................P55"),
        (21.0, 277.0, "Campus Crush....................P75"),
        (20.0, 337.0, "Premium.............................P85"),
        (20.0, 398.0, "Double Premium.................P155"),
        (20.0, 460.0, "DB QuarterPounder w F&D...P125"),
        (20.0, 523.0, "Campus Crush w F&D.........P110")
    ]

    # Create menu texts with explicit text parameter
    for x, y, text in menu_items:
        canvas.create_text(
            x,
            y,
            text=text,  # Explicit text parameter added here
            anchor="nw",
            fill="#000000",
            font=("Inter", 13 * -1)
        )

    rect_id = canvas.create_rectangle(
        330, 146, 672, 531, fill="#D9D9D9", outline=""
    )

    # Menu title
    canvas.create_rectangle(15.0, 142.0, 317.0, 194.0, fill="#E6B528", outline="")
    canvas.create_text(122.0, 142.0, anchor="nw", text="Menu", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen ", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    # Display area
    canvas.create_rectangle(682.0, 193.36483764648438, 984.0, 531.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(682.0, 140.0, 984.0, 193.36483001708984, fill="#E6B528", outline="")
    canvas.create_text(760.0, 140.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 36 * -1))

    # Load images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(111.0, 53.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(501.0, 338.0, image=image_image_2)

    image_image_33 = PhotoImage(file=relative_to_assets("Quarter Pounder.png"))
    image_image_34 = PhotoImage(file=relative_to_assets("Campus Crush.png"))
    image_image_35 = PhotoImage(file=relative_to_assets("Small Premium Burger.png"))
    image_image_36 = PhotoImage(file=relative_to_assets("Premium Burger.png"))
    image_image_37 = PhotoImage(file=relative_to_assets("Double Quarter Pounder.png"))
    image_image_38 = PhotoImage(file=relative_to_assets("Campus Crush with Drinks.png"))

    # Function to display food images
    def display_food(image):
        canvas.itemconfig(image_2, image=image)
 
    # Function to add item to order list
    order_list = []

    def add_to_order():
        # Get the currently displayed food item
        current_image = canvas.itemcget(image_2, "image")
        if current_image == str(image_image_33):
            order_list.append("Quarter Pounder - 55")
        elif current_image == str(image_image_34):
            order_list.append("Campus Crush - P75")
        elif current_image == str(image_image_35):
            order_list.append("Premium - P85")
        elif current_image == str(image_image_36):
            order_list.append("Double Premium - P155")
        elif current_image == str(image_image_37):
            order_list.append("DB Quarter Pounder w F&D - P125")
        elif current_image == str(image_image_38):
            order_list.append("Campus Crush w F&D - P110")
        update_order_list()

    # Function to remove item from order list
    def remove_from_order():
        if order_list:
            order_list.pop()
            update_order_list()

    # Function to update the order list display
    def update_order_list():
        canvas.delete("order_text")
        y_offset = 210
        for item in order_list:
            canvas.create_text(690.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1), tags="order_text")
            y_offset += 30

    # Function to handle order button click
    def place_order():
        if order_list:
            window.destroy()  # Close the current canteen interface
            payment_interface(order_list)  # Open the payment interface with the order list
        else:
            messagebox.showerror("Error", "No items in the order list.")

    # Buttons for displaying food images
    button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
    button_13 = Button(image=button_image_13, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_33), relief="flat")
    button_13.place(x=225.0, y=200.0, width=92.0, height=53.0)

    button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
    button_14 = Button(image=button_image_14, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_34), relief="flat")
    button_14.place(x=225.0, y=260.0, width=93.0, height=53.0)

    button_image_15 = PhotoImage(file=relative_to_assets("button_15.png"))
    button_15 = Button(image=button_image_15, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_35), relief="flat")
    button_15.place(x=225.0, y=320.0, width=92.0, height=53.0)

    button_image_16 = PhotoImage(file=relative_to_assets("button_16.png"))
    button_16 = Button(image=button_image_16, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_36), relief="flat")
    button_16.place(x=225.0, y=380.0, width=92.0, height=53.0)

    button_image_17 = PhotoImage(file=relative_to_assets("button_17.png"))
    button_17 = Button(image=button_image_17, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_37), relief="flat")
    button_17.place(x=225.0, y=442.0, width=92.0, height=53.0)

    button_image_18 = PhotoImage(file=relative_to_assets("button_18.png"))
    button_18 = Button(image=button_image_18, borderwidth=0, highlightthickness=0, command=lambda: display_food(image_image_38), relief="flat")
    button_18.place(x=225.0, y=504.0, width=92.0, height=53.0)

    # Add to order button
    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(image=button_image_10, borderwidth=0, highlightthickness=0, command=add_to_order, relief="flat")
    button_10.place(x=331.0, y=539.0, width=169.0, height=33.0)

    # Remove from order button
    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(image=button_image_11, borderwidth=0, highlightthickness=0, command=remove_from_order, relief="flat")
    button_11.place(x=506.0, y=539.0, width=166.0, height=33.0)

    # Place order button
    button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
    button_12 = Button(image=button_image_12, borderwidth=0, highlightthickness=0, command=place_order, relief="flat")
    button_12.place(x=682.0, y=540.0, width=302.0, height=33.0)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

    window.resizable(False, False)
    window.mainloop()

#----------------------Payment Interface----------------------#
def payment_interface(order_list):
    global window, entry_6, entry_7, entry_8

    window = Tk()
    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Background and header
    canvas.create_rectangle(0.0, 75.0, 450.0, 650.0, fill="#f4cccc", outline="")
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(132.0, 9.0, anchor="nw", text="Cardinal Canteen", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(111.0, 53.0, image=image_image_1)

    # Order List
    canvas.create_text(89.0, 138.0, anchor="nw", text="Order List", fill="#000000", font=("InknutAntiqua Regular", 24 * -1))

    image_image_39 = PhotoImage(file=relative_to_assets("Cart.png"))
    canvas.create_image(44.0, 177.0, image=image_image_39)

    # Display order items
    y_offset = 180
    total_cost = 0
    for item in order_list:
        canvas.create_text(100.0, y_offset, anchor="nw", text=item, fill="#000000", font=("Inter", 13 * -1))
        y_offset += 30
        # Extract price from the item string (assuming the price is the last part of the string)
        price = int(item.split("P")[-1])
        total_cost += price

    # Display total cost
    canvas.create_text(45.0, 510.0, anchor="nw", text=f"Order Fee: P{total_cost}", fill="#000000", font=("InknutAntiqua Regular", 18 * -1))

    # G-Cash Number Entry
    canvas.create_text(557.0, 180.0, anchor="nw", text="G-Cash Number:", fill="#000000", font=("InknutAntiqua Regular", 12 * -1))
    entry_6 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_6.place(x=557.0, y=200.0, width=255.0, height=51.0)

    # Input Payment Entry
    canvas.create_text(557.0, 260.0, anchor="nw", text="Input Payment:", fill="#000000", font=("InknutAntiqua Regular", 12 * -1))
    entry_7 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_7.place(x=557.0, y=280.0, width=255.0, height=51.0)

    #Input Pickup Time
    canvas.create_text(557.0, 340.0, anchor="nw", text="Input Pickup Time:", fill="#000000", font=("InknutAntiqua Regular", 12 * -1))
    entry_8 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_8.place(x=557.0, y=360.0, width=255.0, height=51.0)

    # Pay Button
    button_image_20 = PhotoImage(file=relative_to_assets("button_20.png"))
    button_20 = Button(
        image=button_image_20,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: process_payment(total_cost, order_list),
        relief="flat"
    )
    button_20.place(x=557.0, y=475.0, width=255.0, height=53.0)

    button_image_hover_20 = PhotoImage(file=relative_to_assets("button_hover_20.png"))

    def button_20_hover(e):
        button_20.config(image=button_image_hover_20)

    def button_20_leave(e):
        button_20.config(image=button_image_20)

    button_20.bind('<Enter>', button_20_hover)
    button_20.bind('<Leave>', button_20_leave)

    button_image_19 = PhotoImage(file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.destroy(), customer_interface()],  # Go back to customer interface
        relief="flat"
    )
    button_19.place(x=882.0, y=15.0, width=95.0, height=41.0)

    button_image_hover_19 = PhotoImage(file=relative_to_assets("button_hover_19.png"))

    def button_19_hover(e):
        button_19.config(image=button_image_hover_19)

    def button_19_leave(e):
        button_19.config(image=button_image_19)

    button_19.bind('<Enter>', button_19_hover)
    button_19.bind('<Leave>', button_19_leave)

#Button for Order and Payment History Interface
    button_image_21 = PhotoImage(
        file=relative_to_assets("button_21.png"))
    button_21 = Button(
        image=button_image_21,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_21 clicked"),
        relief="flat"
    )
    button_21.place(
        x=674.0,
        y=15.0,
        width=190.0,
        height=45.0
    )

    button_image_hover_21 = PhotoImage(
        file=relative_to_assets("button_hover_21.png"))

    def button_21_hover(e):
        button_21.config(
            image=button_image_hover_21
        )
    def button_21_leave(e):
        button_21.config(
            image=button_image_21
        )

    button_21.bind('<Enter>', button_21_hover)
    button_21.bind('<Leave>', button_21_leave)

    window.resizable(False, False)
    window.mainloop()

def process_payment(total_cost, order_list):
    gcash_number = entry_6.get()
    payment_amount = entry_7.get()
    pickup_time = entry_8.get()

    if not gcash_number or not payment_amount or not pickup_time:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    try:
        payment_amount = float(payment_amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid payment amount!")
        return

    if payment_amount < total_cost:
        messagebox.showerror("Error", "Insufficient payment!")
        return

    # Calculate change
    change = payment_amount - total_cost

    # Generate a random Order ID
    order_id = f"MAPUA_{random.randint(1000, 9999)}"

    # Get the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the receipt content
    receipt_content = f"""
    Order ID: {order_id}
    Time Created: {current_time}
    Order List:
    """

    # Add each item in the order list to the receipt
    for item in order_list:
        receipt_content += f"    - {item}\n"

    receipt_content += f"""
    Payment Amount: P{payment_amount}
    Change: P{change}
    Pickup Time: {pickup_time}
    """

    # Define the path to save the receipt
    documents_path = r"C:\Users\Rupert Jay Laureano\Documents\build"
    receipt_path = os.path.join(documents_path, f"receipt_{order_id}.txt")

    # Write the receipt to the file
    with open(receipt_path, "w") as receipt_file:
        receipt_file.write(receipt_content)

        # Show success message
        messagebox.showinfo("Success", f"Payment successful! Thank you for your order.\n\nOrder ID: {order_id}")
        window.destroy()  # Close the payment interface
#------------------------Order and Payment History Interface------------------------#
def order_payment_history_interface():
    global window
    window = Tk()

    window.geometry("1000x580")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=580,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Header
    canvas.create_rectangle(0.0, 0.0, 1000.0, 129.0, fill="#AB2328", outline="")
    canvas.create_rectangle(0.0, 82.0, 1000.0, 99.0, fill="#E6B528", outline="")
    canvas.create_text(162.0, 10.0, anchor="nw", text="Cardinal Canteen", fill="#E6B528", font=("InknutAntiqua Regular", 36 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(111.0, 53.0, image=image_image_1)

    # Title
    canvas.create_rectangle(23.0, 151.0, 983.0, 181.0, fill="#FAEECA", outline="")
    canvas.create_text(32.0, 149.0, anchor="nw", text="ORDER AND PAYMENT HISTORY", fill="#000000", font=("InknutAntiqua Bold", 18 * -1))

# Start the application
create_database()
registration_interface()
