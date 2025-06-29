from pathlib import Path
from tkinter import Tk, Canvas, Entry, PhotoImage, messagebox, Button, filedialog, simpledialog
import tkinter as tk
import random, sys, os
import socket

# Adjusted imports for client
backend_path = Path(__file__).resolve().parent / '..' / 'backend' / 'client'
sys.path.append(str(backend_path))

import client   

DEFAULT_FONT = ("Montserrat", 16)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"source")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Initialize main window
window = Tk()
window.geometry("788x443")
window.configure(bg="#FFFFFF")

# Frames for login and main UI
login_frame = tk.Frame(window, bg="#FFFFFF", width=788, height=443)
main_frame = tk.Frame(window, bg="#FFFFFF", width=788, height=443)

def show_frame(frame):
    frame.pack(fill='both', expand=True)
    frame.tkraise()

# Create login canvas and widgets
canvas_login = Canvas(login_frame, bg="#FFFFFF", height=443, width=788, bd=0, highlightthickness=0, relief="ridge")
canvas_login.place(x=0, y=0)

image_log_in = PhotoImage(file=relative_to_assets("log_in.png"))
log_in = canvas_login.create_image(394.0, 221.0, image=image_log_in)

image_frame = PhotoImage(file=relative_to_assets("frame.png"))
frame = canvas_login.create_image(577.0, 216.0, image=image_frame)

canvas_login.create_text(455, 130, anchor="nw", text="Server IP:", fill="#FFFFFF", font=("Montserrat bold", 12))

entry_1 = Entry(login_frame, bd=0, bg="#576886", fg="white", highlightthickness=0, font=("Montserrat", 12))
entry_1.place(x=455, y=160, width=200, height=20)
canvas_login.create_line(455, 185, 700, 185, fill='white', width=1)

canvas_login.create_text(455, 210, anchor="nw", text="Port:", fill="#FFFFFF", font=("Montserrat bold", 12))

entry_2 = Entry(login_frame, bd=0, bg="#576886", fg="white", highlightthickness=0, font=("Montserrat", 12))
entry_2.place(x=455, y=240, width=200, height=20)
canvas_login.create_line(455, 265, 700, 265, fill='white', width=1)

def round_rectangle(canvas, x1, y1, x2, y2, radius=50, **kwargs):
    radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)
    points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2, y1 + radius,
              x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius,
              y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def check_connection():
    global client_instance
    if client_instance and client_instance.is_connected():
        return True
    else:
        messagebox.showwarning("Warning", "Lost connection to the server. Returning to login screen.")
        main_frame.pack_forget()
        show_login_frame()
        return False

def on_button_enter(event):
    canvas_login.itemconfig(button_bg, fill="#062866")

def on_button_leave(event):
    canvas_login.itemconfig(button_bg, fill="#193D7E")

def fetch_and_display_files():
    if check_connection():
        try:
            file_list = client_instance.list_files()
            if file_list:
                global uploaded_files
                uploaded_files = file_list
                display_uploaded_files()
            # else:
            #     messagebox.showinfo("Info", "No files found on the server.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve files: {e}")

client_instance = None
def on_button_click(event):
    global client_instance

    if entry_1.get() and entry_2.get():
        ip = entry_1.get()
        port = int(entry_2.get())

        client_instance = client.Client(ip, port)

        if client_instance.is_connected():
            try:
                check = client_instance.client_socket.recv(client_instance.MSG_SIZE).decode().strip()
                if check.startswith("OK@\nConnection set."):
                    print("Log in successfully!")
                    login_frame.pack_forget()
                    show_frame(main_frame)
                    messagebox.showinfo("Notification", "Login successfully!")

                    # Fetch and display files
                    fetch_and_display_files()
                    return
                else:
                    messagebox.showerror("Error", "Connection failed! Server did not send proper confirmation.")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {e}")
        else:
            messagebox.showerror("Error", "Connection failed. Please check your IP and port.")
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

    client_instance.client_socket.close()
    client_instance.CONNECTED = False
    main_frame.pack_forget()
    show_frame(login_frame)


# Log In button
global button_bg
button_bg = round_rectangle(canvas_login, 470, 300, 690, 340, radius=50, fill="#193D7E", outline="")
button_text = canvas_login.create_text(580, 320, text="Log In", fill="white", font=("Montserrat bold", 14))

# Bind events to both the button background and the text
canvas_login.tag_bind(button_bg, "<Enter>", on_button_enter)
canvas_login.tag_bind(button_bg, "<Leave>", on_button_leave)
canvas_login.tag_bind(button_bg, "<Button-1>", on_button_click)
canvas_login.tag_bind(button_text, "<Enter>", on_button_enter)
canvas_login.tag_bind(button_text, "<Leave>", on_button_leave)
canvas_login.tag_bind(button_text, "<Button-1>", on_button_click)

canvas_login.create_text(540.0, 80.0, anchor="nw", text="Login", fill="#FFFFFF", font=("Montserrat bold", 18))
canvas_login.create_text(30.0, 50.0, anchor="nw", text="HELLO!", fill="#FFFFFF", font=("Montserrat bold", 50))
canvas_login.create_text(30.5, 130.0, anchor="nw", text="Welcome to our app", fill="#FFFFFF", font=("Montserrat", 16))

# Create main canvas and widgets
canvas_main = Canvas(main_frame, bg="#FFFFFF", height=443, width=788, bd=0, highlightthickness=0, relief="ridge")
canvas_main.place(x=0, y=0)

image_bg2 = PhotoImage(file=relative_to_assets("bg2.png"))
bg2 = canvas_main.create_image(394.0, 221.0, image=image_bg2)

FILE_TYPE_IMAGES = {
    'pdf': 'pdf.png',
    'txt': 'txt.png',
    'doc': 'docx.png',
    'docx': 'docx.png',
    'xlsx': 'xlsx.png',
    'jpg': 'image.png',
    'png': 'image.png',
    'jpeg': 'image.png',
    'zip': 'zip.png',
    'mp4': 'mp4.png',
    'mp3': 'mp3.png',
    'mov': 'mp4.png',
    'default': 'others.png'
}

# Store uploaded files
uploaded_files = []

def display_uploaded_files():
    # Clear existing file display
    for widget in main_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget != plus:
            widget.destroy()
    
    # Define grid layout parameters
    columns = 4
    x_start = 150
    y_start = 60
    x_spacing = 150
    y_spacing = 150
    
    # Display the list of uploaded files
    for idx, file in enumerate(uploaded_files):
        row = idx // columns
        col = idx % columns
        
        x_position = x_start + col * x_spacing
        y_position = y_start + row * y_spacing
        
        file_extension = file.split('.')[-1].lower()
        image_file = FILE_TYPE_IMAGES.get(file_extension, 'others.png')
        
        image = PhotoImage(file=relative_to_assets(image_file))
        label = tk.Label(main_frame, image=image, bg='#102854', cursor="hand2")
        label.image = image  # Keep a reference to avoid garbage collection
        label.place(x=x_position, y=y_position)
        
        # Show the filename as text
        filename_label = tk.Label(main_frame, text=file, font=("Montserrat", 10), bg="#102854", fg="white")
        filename_label.place(x=x_position + 5, y=y_position + 80)
        
        # Add context menu
        context_menu = tk.Menu(window, tearoff=0)
        context_menu.add_command(label="Download", command=lambda f=file: download_file(f))
        context_menu.add_command(label="Delete", command=lambda f=file: delete_file(f))
        context_menu.add_command(label="Rename", command=lambda f=file: rename_file(f))
        
        def show_context_menu(event, f=file):
            if check_connection():
                context_menu.post(event.x_root, event.y_root)
        
        label.bind("<Button-3>", show_context_menu)
        filename_label.bind("<Button-3>", show_context_menu)

def upload_file():
    if not check_connection():
        return
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        if file_name not in uploaded_files:
            try:
                client_instance.upload(file_path)
                uploaded_files.append(file_name)
                display_uploaded_files()
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed")
                main_frame.pack_forget()
                show_frame(login_frame)
                client_instance.client_socket.close()
                client_instance.CONNECTED = False
                messagebox.showerror("Error", "Server closed connection!")
        else:
            messagebox.showinfo("Info", "File already exists in the uploaded files list.")

def download_file(filename):
    if not check_connection():
        return
    if filename in uploaded_files:
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename)
        if save_path:
            try:
                client_instance.download(filename, save_path)
                messagebox.showinfo("Success", f"File '{filename}' downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed")
                main_frame.pack_forget()
                show_frame(login_frame)
                client_instance.client_socket.close()
                client_instance.CONNECTED = False
                messagebox.showerror("Error", "Server closed connection!")
    else:
        messagebox.showerror("Error", "File not found in the uploaded files list.")

def delete_file(filename):
    if not check_connection():
        return
    if filename in uploaded_files:
        try:
            client_instance.delete(filename)
            uploaded_files.remove(filename)
            display_uploaded_files()
            messagebox.showinfo("Success", f"File '{filename}' deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed")
            main_frame.pack_forget()
            show_frame(login_frame)
            client_instance.client_socket.close()
            client_instance.CONNECTED = False
            messagebox.showerror("Error", "Server closed connection!")
    else:
        messagebox.showerror("Error", "File not found in the uploaded files list.")

def rename_file(filename):
    if not check_connection():
        return
        
    if filename in uploaded_files:

        file_root, file_ext = os.path.splitext(filename)
        new_name_root = simpledialog.askstring("Rename file", f"Enter the new name for file '{file_root}':")

        if new_name_root:
            new_name = new_name_root.strip() + file_ext
            try:
                success = client_instance.rename(filename, new_name)
                if success:
                    uploaded_files.remove(filename)
                    uploaded_files.append(new_name)
                    display_uploaded_files()
                    messagebox.showinfo("Success", f"File '{filename}' renamed to '{new_name}' successfully.")
                else:
                    messagebox.showerror("Failed", "Rename failed, Please try again!")

            except Exception as e:
                messagebox.showerror("Error", f"Rename failed")
                main_frame.pack_forget()
                show_frame(login_frame)
                client_instance.client_socket.close()
                client_instance.CONNECTED = False
                messagebox.showerror("Error", "Server closed connection!")
    else:
        messagebox.showerror("Error", "File not found in the uploaded files list.")

def disconnected_server():
    global client_instance
    if client_instance and client_instance.is_connected():
        try:
            client_instance.client_socket.close()
            client_instance.CONNECTED = False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to disconnect from server: {e}")
    main_frame.pack_forget()
    show_frame(login_frame)
    messagebox.showinfo("Success", f"Disconnecting from server successfully")

button_image_1 = PhotoImage(file=relative_to_assets("newFile.png"))
newFile = Button(main_frame, image=button_image_1, borderwidth=0, highlightthickness=0, bg="#102854", command=upload_file, relief="flat")
newFile.place(x=633.0, y=362.0, width=125.0, height=60)

button_image_2 = PhotoImage(file=relative_to_assets("home.png"))
home = Button(main_frame, image=button_image_2, borderwidth=0, highlightthickness=0, bg="#304469", command=disconnected_server, relief="flat")
home.place(x=22.0, y=33.0, width=29.0, height=24.0)

button_image_3 = PhotoImage(file=relative_to_assets("plus.png"))
plus = Button(main_frame, image=button_image_3, borderwidth=0, highlightthickness=0, bg="#3c4d71", command=upload_file, relief="flat")
plus.place(x=27.23, y=90.0, width=17.0, height=16.6)

button_image_4 = PhotoImage(file=relative_to_assets("exit.png"))
exit = Button(main_frame, image=button_image_4, borderwidth=0, highlightthickness=0, bg="#717998", command=disconnected_server, relief="flat")
exit.place(x=27.0, y=394.0, width=18.0, height=18.0)


# Show login frame initially
show_frame(login_frame)
window.mainloop()
