import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  
# Themes: blue (default), dark-blue, green
app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1000x1000")

def button_function():
    print("button pressed")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, 
                                 text="CTkButton",
                                 command=button_function)

button.place(relx=0.1, rely=0.3, anchor=tkinter.CENTER)





app.mainloop()