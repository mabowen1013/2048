import tkinter as tk
import customtkinter as ctk

root = ctk.CTk()
root.geometry("500x500")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

cell_size=100
grid_size=4

for row in range(grid_size):
    for col in range(grid_size):
        frame = ctk.CTkFrame(master=root,width=cell_size,height=cell_size)
        frame.grid(row=row,column=col,padx=10,pady=10)

root.mainloop()