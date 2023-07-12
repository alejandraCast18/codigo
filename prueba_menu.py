import tkinter as tk

class Frame_menu(tk.Frame):
    def __init__(self, root, menu_options):
        super().__init__(root, bg='black')
        self.root = root
        self.menu_options = menu_options
        self.pack(fill='both', expand=True)

        self.menu_crear(menu_options = menu_options)
        self.menu_frame.grid_remove()

    def menu_crear(self, menu_options):
        # Crear el disparador del menú
        self.menu_options = menu_options
        self.trigger_label = tk.Button(self, text="Menú", padx=10, pady=5, bg="#158645", fg="#DAD5D6", cursor="hand2", activebackground="#35BD6F", font=("Arial", 12, "bold"))
        self.trigger_label.grid(row=0, column=0)
        self.trigger_label.bind("<Button-1>", lambda event: self.toggle_menu())
        # Crear el menú usando labels
        self.menu_frame = tk.Frame(self)

        for index, option in enumerate(self.menu_options):
            label = tk.Button(self.menu_frame, text=option, padx=10, pady=5, width=20, bg="#158645", fg="#DAD5D6", cursor="hand2", activebackground="#35BD6F", font=("Arial", 12, "bold"))
            label.grid(row=index, column=0, padx=10, pady=10)

            # Asignar una función al hacer clic en cada label
            label.bind("<Button-1>", lambda event, option=option: self.handle_click(option))

    def handle_click(self, option):
        print(f"Seleccionaste la opción {option}")

    def toggle_menu(self):
        if self.menu_frame.winfo_viewable():
            self.menu_frame.grid_remove()
        else:
            self.menu_frame.grid()

root = tk.Tk()

menu_options = ["Opción 1", "Opción 2", "Opción 3", "Opción 4"]

menu_de_opciones = Frame_menu(root = root, menu_options = menu_options)




# Ocultar el menú por defecto


root.mainloop()
