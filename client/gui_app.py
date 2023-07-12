import tkinter as tk
from tkinter import ttk, messagebox
from model.cliente_dao import Cliente, crear_tablas, borrar_tablas, guadar_cliente, listar, editar,listar_busqueda, eliminar
from model.cliente_dao import Usuario, crear_tabla_usuarios, guadar_usuario, listar_usuarios, listar_busqueda_usuarios
import customtkinter 
from PIL import ImageTk, Image
color='black'
color_2='white'
color_3='#3f3f3f'
bandera_busqueda = False

class Frame_login(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)
        self.login()

    def login(self):
        self.img = customtkinter.CTkImage(light_image=Image.open('img/10.png'), dark_image=Image.open('img/10.png'))
        self.background = customtkinter.CTkLabel(self, text='', image=self.img)
        self.background.place(relx=0.5, rely=0.5, anchor='center')
        self.bind("<Configure>", self.on_resize)

        # Creando marco personalizado
        self.frame = customtkinter.CTkFrame(self, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        for i in range(6):
            self.frame.rowconfigure(i, weight=1)
        for i in range(1):
            self.frame.columnconfigure(i, weight=1)

        l2 = customtkinter.CTkLabel(self.frame, text="REPUESTOS DORTA DE TÁRIBA", font=('Century Gothic', 20))
        l2.grid(row=0, column=0, padx=20, pady=20)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='USUARIO')
        self.entry1.grid(row=1, column=0, padx=20, pady=5)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='CONTRASEÑA', show="*")
        self.entry2.grid(row=2, column=0, padx=20, pady=10)

        l3 = customtkinter.CTkLabel(master=self.frame, text="ERROR", font=('Century Gothic', 12))

        self.nivel_acceso = tk.StringVar(value="")

        def verificar_credenciales():
            self.usuario = Usuario(
                self.entry1.get(),
                self.entry2.get(),
                self.nivel_acceso.get(),
            )
            datos_usuario = listar_busqueda_usuarios(self.usuario)

            try:
                if self.usuario.contraseña == datos_usuario[0][2]:
                    self.bienvenida()
            except Exception as e:
                # Manejar la excepción de acuerdo a tus necesidades
                print("Ocurrió un error:", str(e))
                l3.grid(row=3, column=0, padx=20, pady=0)

        # Creando botón personalizado
        img2 = customtkinter.CTkImage(Image.open("img/3.png").resize((20, 20), Image.ANTIALIAS))

        button1 = customtkinter.CTkButton(master=self.frame, image=img2, width=220, text="Entrar", command=verificar_credenciales, corner_radius=6, font=('Century Gothic',15))
        button1.grid(row=4, column=0, padx=20, pady=(10, 0))
        
        button2 = customtkinter.CTkButton(master=self.frame, text="Salir", width=220, height=30, compound="left",font=('Century Gothic', 15))
        button2.grid(row=5, column=0, padx=20, pady=(10, 20))  
        
    def bienvenida(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        app = Frame_bienvenida(root = self.root)

    def registrarse(self):
        self.destroy()
        app = Frame_registrar_usuario(root = self.root)

    def on_resize(self, event):
        self.img.configure(size=(self.winfo_width()+2, self.winfo_height()+2))


class Frame_bienvenida(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.menu_de_opciones = Frame_menu(self.root)
        self.pack(side='top', fill='both', expand=True)
        self.bienvenida()

    def bienvenida(self):
        self.img = customtkinter.CTkImage(light_image=Image.open('img/4.png'), dark_image=Image.open('img/4.png'))
        self.background = customtkinter.CTkLabel(self, text='', image=self.img)
        self.background.place(relx=0.5, rely=0.5, anchor='center')
        self.bind("<Configure>", self.on_resize)

        for i in range(4):
            self.rowconfigure(i, weight=1)
        for i in range(4):
            self.columnconfigure(i, weight=1)


        self.label_bienvenida = customtkinter.CTkLabel(self, text='Bienvenido', font=('Arial', 12, 'bold'))
        self.label_bienvenida.grid(row=1, column=1, padx=10, pady=10, sticky='e')

       
        img3 = customtkinter.CTkImage(Image.open("img/2.png").resize((20, 20), Image.ANTIALIAS))

        button3 = customtkinter.CTkButton(master=self, image=img3, text="", width=30, height=30, compound="left",
                                          fg_color='white', text_color='black', hover_color='#AFAFAF')
        button3.place(relx=0.5, rely=0.5, anchor="center")

    def on_resize(self, event):
        self.img.configure(size=(self.winfo_width()+2, self.winfo_height()+2))

class Frame_registrar_cliente(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.menu_de_opciones = Frame_menu(root)
        self.pack(side='top', fill='both', expand=True)
        self.tabla_datos()
        #self.barra_menu()

    def barra_menu(self):
        self.barra_registro = tk.Menu()
        self.root.config(menu=self.barra_registro)

        self.menu_inicio = tk.Menu(self.barra_registro, tearoff = 0)
        self.barra_registro.add_cascade(label ='Inicio', menu = self.menu_inicio)

        self.menu_inicio.add_command(label='Crear Registro en DB', command=crear_tablas)
        self.menu_inicio.add_command(label='Eliminar Registro en DB', command=borrar_tablas)
        self.menu_inicio.add_command(label='Salir', command = self.root.destroy)

        self.barra_registro.add_cascade(label='Consultas')
        self.barra_registro.add_cascade(label='Configuracion')
        self.barra_registro.add_cascade(label='Ayuda')


    def tabla_datos(self):
        self.limpiar_pantalla()

        self.tabla = customtkinter.CTkTabview(self)
        self.tabla.pack(fill='both', expand=True)
        self.tabla.add("Cliente")
        self.tabla.add("Contacto")

        for i in range(3):
            self.tabla.tab("Cliente").rowconfigure(i, weight=1)
        for i in range(6):
            self.tabla.tab("Cliente").columnconfigure(i, weight=1)

        for i in range(2):
            self.tabla.tab("Contacto").rowconfigure(i, weight=1)
        for i in range(6):
            self.tabla.tab("Contacto").columnconfigure(i, weight=1)
        #####################1
        #linea 1
        #nombre 
        self.label_nombre = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Nombre: ', font = ('Arial', 12, 'bold'))
        self.label_nombre.grid(row=0, column=0, sticky='e')

        self.nombre = tk.StringVar()
        self.entry_nombre= customtkinter.CTkEntry(self.tabla.tab("Cliente"), textvariable = self.nombre, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, sticky='ew')

        #apellido 
        self.label_apellido = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Apellido: ', font = ('Arial', 12, 'bold'))
        self.label_apellido.grid(row=0, column=2, sticky='e')

        self.apellido = tk.StringVar()
        self.entry_apellido= customtkinter.CTkEntry(self.tabla.tab("Cliente"), textvariable = self.apellido, font=('Arial', 12))
        self.entry_apellido.grid(row=0, column=3, sticky='ew')

        #direccion 
        self.label_direccion = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Dirección: ', font = ('Arial', 12, 'bold'))
        self.label_direccion.grid(row=0, column=4, sticky='e')

        self.direccion = tk.StringVar()
        self.entry_direccion= customtkinter.CTkEntry(self.tabla.tab("Cliente"), textvariable = self.direccion, font=('Arial', 12))
        self.entry_direccion.grid(row=0, column=5, sticky='ew')

        #linea 2
        #telefono 
        self.label_telefono = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Teléfono: ', font = ('Arial', 12, 'bold'))
        self.label_telefono.grid(row=1, column=0, sticky='e')

        self.telefono = tk.StringVar()
        self.entry_telefono= customtkinter.CTkEntry(self.tabla.tab("Cliente"), textvariable = self.telefono, font=('Arial', 12))
        self.entry_telefono.grid(row=1, column=1, sticky='ew')

        #correo_electronico 
        self.label_correo_electronico = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Correo: ', font = ('Arial', 12, 'bold'))
        self.label_correo_electronico.grid(row=1, column=2, sticky='e')

        self.correo_electronico = tk.StringVar()
        self.entry_correo_electronico= customtkinter.CTkEntry(self.tabla.tab("Cliente"), textvariable = self.correo_electronico, font=('Arial', 12))
        self.entry_correo_electronico.grid(row=1, column=3, sticky='ew')

        #fecha_registro
        self.label_fecha_registro = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Fecha registro: ', font = ('Arial', 12, 'bold'))
        self.label_fecha_registro.grid(row=1, column=4, sticky='e')

        self.frame_fecha_registro = customtkinter.CTkFrame(self.tabla.tab("Cliente"), fg_color='transparent')
        self.frame_fecha_registro.grid(row=1, column=5, sticky='ew')

        self.frame_fecha_registro.columnconfigure(0, weight=1)
        self.frame_fecha_registro.columnconfigure(1, weight=1)
        self.frame_fecha_registro.columnconfigure(2, weight=2)

        self.fecha_registro = tk.StringVar()

        self.entry_fecha_registro_day = customtkinter.CTkEntry(self.frame_fecha_registro, placeholder_text='DD', width=30, font=('Arial', 12))
        self.entry_fecha_registro_day.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.entry_fecha_registro_month = customtkinter.CTkEntry(self.frame_fecha_registro, placeholder_text='MM', width=30, font=('Arial', 12))
        self.entry_fecha_registro_month.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.entry_fecha_registro_year = customtkinter.CTkEntry(self.frame_fecha_registro, placeholder_text='YYYY', width=70, font=('Arial', 12))
        self.entry_fecha_registro_year.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        #linea 3
        #informacion_adicional 
        self.label_informacion_adicional = customtkinter.CTkLabel(self.tabla.tab("Cliente"), text = 'Información: ', font = ('Arial', 12, 'bold'))
        self.label_informacion_adicional.grid(row=2, column=1, sticky='e')

        self.entry_informacion_adicional= customtkinter.CTkEntry(self.tabla.tab("Cliente"), font=('Arial', 12))
        self.entry_informacion_adicional.grid(row=2, column=2, columnspan=3, sticky='ew')

        #####################2
        #linea1
        #fecha_contacto
        self.label_fecha_contacto = customtkinter.CTkLabel(self.tabla.tab("Contacto"), text = 'Fecha contacto: ', font = ('Arial', 12, 'bold'))
        self.label_fecha_contacto.grid(row=0, column=0, sticky='e')

        self.frame_fecha_contacto = customtkinter.CTkFrame(self.tabla.tab("Contacto"), fg_color='transparent')
        self.frame_fecha_contacto.grid(row=0, column=1, sticky='ew')

        self.frame_fecha_contacto.columnconfigure(0, weight=1)
        self.frame_fecha_contacto.columnconfigure(1, weight=1)
        self.frame_fecha_contacto.columnconfigure(2, weight=2)

        self.fecha_contacto = tk.StringVar()

        self.entry_fecha_contacto_day = customtkinter.CTkEntry(self.frame_fecha_contacto, placeholder_text='DD', width=30, font=('Arial', 12))
        self.entry_fecha_contacto_day.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.entry_fecha_contacto_month = customtkinter.CTkEntry(self.frame_fecha_contacto, placeholder_text='MM', width=30, font=('Arial', 12))
        self.entry_fecha_contacto_month.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.entry_fecha_contacto_year = customtkinter.CTkEntry(self.frame_fecha_contacto, placeholder_text='YYYY', width=70, font=('Arial', 12))
        self.entry_fecha_contacto_year.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        #tipo contacto
        self.label_tipo_contacto = customtkinter.CTkLabel(self.tabla.tab("Contacto"), text = 'Tipo contacto: ', font = ('Arial', 12, 'bold'))
        self.label_tipo_contacto.grid(row=0, column=2, sticky='e')

        self.entry_tipo_contacto= customtkinter.CTkEntry(self.tabla.tab("Contacto"), font=('Arial', 12))
        self.entry_tipo_contacto.grid(row=0, column=3, sticky='ew')

        #descripcion_contacto 
        self.label_descripcion_contacto = customtkinter.CTkLabel(self.tabla.tab("Contacto"), text = 'Descripcion: ', font = ('Arial', 12, 'bold'))
        self.label_descripcion_contacto.grid(row=0, column=4, sticky='e')

        self.entry_descripcion_contacto= customtkinter.CTkEntry(self.tabla.tab("Contacto"), font=('Arial', 12))
        self.entry_descripcion_contacto.grid(row=0, column=5, sticky='ew')

        #linea 2
        #seguimiento_requerido
        self.label_seguimiento_requerido = customtkinter.CTkLabel(self.tabla.tab("Contacto"), text = 'Seguimiento requerido: ', font = ('Arial', 12, 'bold'))
        self.label_seguimiento_requerido.grid(row=1, column=0, sticky='e')

        self.seguimiento_requerido = tk.StringVar(value="No")
        self.entry_seguimiento_requerido = customtkinter.CTkSwitch(self.tabla.tab("Contacto"), textvariable = self.seguimiento_requerido, font=('Arial', 12, 'bold'), command=self.seguimiento_requerido_evento)
        self.entry_seguimiento_requerido.grid(row=1, column=1, padx=10, sticky='ew')

        #observaciones_adicionales 
        self.label_observaciones_adicionales = customtkinter.CTkLabel(self.tabla.tab("Contacto"), text = 'Información: ', font = ('Arial', 12, 'bold'))
        self.label_observaciones_adicionales.grid(row=1, column=2, sticky='e')

        self.entry_observaciones_adicionales= customtkinter.CTkEntry(self.tabla.tab("Contacto"), font=('Arial', 12))
        self.entry_observaciones_adicionales.grid(row=1, column=3, columnspan=2, sticky='ew')

        # Botones Guardar
        self.boton_guardar = customtkinter.CTkButton(self, text="Guardar", command = self.guardar_cliente, width=20, font=('Arial', 12, 'bold'))
        self.boton_guardar.pack(padx=10, pady=10)

    def seguimiento_requerido_evento(self):
        self.seguimiento_requerido.set('Si' if self.entry_seguimiento_requerido.get() == 1 else 'No')

    def guardar_cliente(self):
        global bandera_busqueda
        self.fecha_registro.set(self.entry_fecha_registro_day.get() + '-' + self.entry_fecha_registro_month.get() + '-' + self.entry_fecha_registro_year.get())
        print(self.fecha_registro.get())
        self.cliente = Cliente(
            self.nombre.get(),
            self.apellido.get(),
            self.direccion.get(),
            self.telefono.get(),
            self.correo_electronico.get(),
            self.fecha_registro.get(),
            self.entry_informacion_adicional.get()
            )

        guadar_cliente(self.cliente)
        self.login()

    def login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(menu=False)
        app = Frame_login(root = self.root)

    def limpiar_pantalla(self):
        for i in list(self.children.values()):
            i.destroy()

        for i in range(20):
            self.rowconfigure(i, weight=0)
        for i in range(20):
            self.columnconfigure(i, weight=0)

#CODIGO BASURA NO BORRAR
class Frame_registro(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)

        self.registro_clientes()

        self.menu_de_opciones = Frame_menu(root)
        self.menu_de_opciones.lift()
        
    def registro_clientes(self):
        self.limpiar_pantalla()

        for i in range(7):
            self.rowconfigure(i, weight=1)
        for i in range(3):
            self.columnconfigure(i, weight=1)

        self.campos_cliente()
        self.deshabilitar_campos()
        self.tabla_cliente()
        self.barra_menu()

    def barra_menu(self):
        self.barra_registro = tk.Menu()
        self.root.config(menu=self.barra_registro)

        self.menu_inicio = tk.Menu(self.barra_registro, tearoff = 0)
        self.barra_registro.add_cascade(label ='Inicio', menu = self.menu_inicio)

        self.menu_inicio.add_command(label='Crear Registro en DB', command=crear_tablas)
        self.menu_inicio.add_command(label='Eliminar Registro en DB', command=borrar_tablas)
        self.menu_inicio.add_command(label='Salir', command = self.root.destroy)

        self.barra_registro.add_cascade(label='Consultas')
        self.barra_registro.add_cascade(label='Configuracion')
        self.barra_registro.add_cascade(label='Ayuda')

    def campos_cliente(self):
        # Labels de cada campo
        self.label_nombre = tk.Label(self, text = 'Nombre: ')
        self.label_nombre.config(font = ('Arial', 12, 'bold'))
        self.label_nombre.grid(row = 0, column = 0, padx = 10, pady = 10, sticky='e')

        self.label_direccion = tk.Label(self, text='direccion: ')
        self.label_direccion.config(font=('Arial', 12, 'bold'))
        self.label_direccion.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.label_telefono = tk.Label(self, text='telefono: ')
        self.label_telefono.config(font=('Arial', 12, 'bold'))
        self.label_telefono.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        # Entrys de cada campo
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable = self.mi_nombre)
        self.entry_nombre.config(width=50, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan = 2, sticky='w')

        self.mi_direccion = tk.StringVar()
        self.entry_direccion = tk.Entry(self, textvariable=self.mi_direccion)
        self.entry_direccion.config(
            width=50, font=('Arial', 12))
        self.entry_direccion.grid(
            row=1, column=1, padx=10, pady=10, columnspan = 2, sticky='w')

        self.mi_telefono = tk.StringVar()
        self.entry_telefono = tk.Entry(self, textvariable=self.mi_telefono)
        self.entry_telefono.config(
            width=50, font=('Arial', 12))
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=10, columnspan = 2, sticky='w')



        # Botones Nuevo
        self.boton_nuevo = tk.Button(self, text="Nuevo", command = self.nuevo_cliente)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'),
                                fg='#DAD5D6', bg='#158645', 
                                cursor='hand2', activebackground='#35BD6F')
        self.boton_nuevo.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        # Botones Guardar
        self.boton_guardar = tk.Button(self, text="Guardar", command = self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'),
                                  fg='#DAD5D6', bg='#1658A2',
                                  cursor='hand2', activebackground='#3586DF')
        self.boton_guardar.grid(row=3, column=1, padx=10, pady=10)

        # Botones Cancelar
        self.boton_cancelar = tk.Button(
            self, text="Cancelar", command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'),
                                   fg='#DAD5D6', bg='#BD152E',
                                   cursor='hand2', activebackground='#E15370')
        self.boton_cancelar.grid(row=3, column=2, padx=10, pady=10, sticky='w')

    def habilitar_campos_buscar(self):
        self.mi_nombre.set('')

        self.entry_nombre.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def habilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_direccion.set('')
        self.mi_telefono.set('')

        self.entry_nombre.config(state='normal')
        self.entry_direccion.config(state='normal')
        self.entry_telefono.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def deshabilitar_campos(self):
        self.id_cliente = None
        
        self.mi_nombre.set('')
        self.mi_direccion.set('')
        self.mi_telefono.set('')

        self.entry_nombre.config(state='disabled')
        self.entry_direccion.config(state='disabled')
        self.entry_telefono.config(state='disabled')

        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')
    
    def guardar_datos(self):
        global bandera_busqueda
        self.cliente = Cliente(
                self.mi_nombre.get(),
                self.mi_direccion.get(),
                self.mi_telefono.get(),
            )

        if bandera_busqueda == True:

            self.tabla_cliente()
            bandera_busqueda = False
        else:

            if self.id_cliente == None:
                guadar(self.cliente)

            else:
                editar(self.cliente, self.id_cliente)

            self.tabla_cliente()

        #Desabilira campos
        self.deshabilitar_campos()

    def tabla_cliente(self):
        #Nuevo widget para la tabla
        frame_tabla = tk.Frame(self, bg='black')
        frame_tabla.grid(row=4, column=0, columnspan=3,padx=20, sticky='we')

        frame_tabla.rowconfigure(0, weight=1)
        for i in range(3):
            frame_tabla.columnconfigure(i, weight=1)

        #Recuperar la lista 
        global bandera_busqueda
        if bandera_busqueda == True:
             self.lista_clientes = listar_busqueda(self.cliente)
        else:
            self.lista_clientes = listar()
        self.lista_clientes.reverse()

        self.tabla  = ttk.Treeview(frame_tabla, 
        column = ('Nombre', 'Direccion', 'Telefono'))
        self.tabla.grid(row=0, column=0, columnspan=3, sticky = 'ew')

        # Scrollbar para la tabla si excede 10 registros
        self.scroll = ttk.Scrollbar(frame_tabla,
        orient = 'vertical', command = self.tabla.yview)
        self.tabla.configure(yscrollcommand = self.scroll.set)
        self.scroll.grid(row = 0, column = 2, sticky = 'nse')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='DIRECCION')
        self.tabla.heading('#3', text='TELEFONO')

        # Iterar la lista
        for p in self.lista_clientes:
            self.tabla.insert('',0, text=p[0], 
            values = (p[1], p[2], p[3]))

        # Botones Editar
        self.boton_editar = tk.Button(self, text="Editar", command = self.editar_datos)
        self.boton_editar.config(width=20, font=('Arial', 12, 'bold'),
                                fg='#DAD5D6', bg='#158645',
                                cursor='hand2', activebackground='#35BD6F')
        self.boton_editar.grid(row=5, column=0, padx=10, pady=10, sticky='e')

        # Botones Buscar
        self.boton_buscar = tk.Button(self, text="Buscar", command = self.buscar_datos)
        self.boton_buscar.config(width = 20, font= ('Arial', 12, 'bold'), fg = 'white', bg='#67B26F', cursor='hand2', activebackground= '#3a6186')
        self.boton_buscar.grid(row = 5, column = 1, padx = 10, pady = 10)

        # Botones Eliminar
        self.boton_eliminar = tk.Button(self, text="Eliminar", command = self.eliminar_datos)
        self.boton_eliminar.config(width=20, font=('Arial', 12, 'bold'),
                                   fg='#DAD5D6', bg='#BD152E',
                                   cursor='hand2', activebackground='#E15370')
        self.boton_eliminar.grid(row=5, column=2, padx=10, pady=10, sticky='w')

        #Boton Atras
        self.boton_atras = tk.Button(self, text="Atras", command = self.login)
        self.boton_atras.config(width=20, font=('Arial', 12, 'bold'),
                                   fg='#DAD5D6', bg='#BD152E',
                                   cursor='hand2', activebackground='#E15370')
        self.boton_atras.grid(row=6, column=1, padx=10, pady=10)

    def login(self):
        self.destroy()
        self.barra_registro.destroy()
        app = Frame_login(root = self.root)

    def nuevo_cliente(self):
        self.habilitar_campos()
    
    def editar_datos(self):
        try:
            self.id_cliente = self.tabla.item(self.tabla.selection())['text']
            self.nombre_cliente = self.tabla.item(
                self.tabla.selection())['values'][0]
            self.direccion_cliente = self.tabla.item(
                self.tabla.selection())['values'][1]
            self.telefono_cliente = self.tabla.item(
                self.tabla.selection())['values'][2]
            
            self.habilitar_campos()

            self.entry_nombre.insert(0, self.nombre_cliente)
            self.entry_direccion.insert(0, self.direccion_cliente)
            self.entry_telefono.insert(0, self.telefono_cliente)
            
        except:
            titulo = 'Edición de datos'
            mensaje = 'No ha seleccionado nigun registro'
            messagebox.showerror(titulo, mensaje)

    def buscar_datos(self):
        global bandera_busqueda
        try:
            self.nombre_cliente = ''
            self.direccion_cliente = ''
            self.telefono_cliente = ''
            
            self.habilitar_campos_buscar()

            self.entry_nombre.insert(0, self.nombre_cliente)
            self.entry_direccion.insert(0, self.direccion_cliente)
            self.entry_telefono.insert(0, self.telefono_cliente)

            bandera_busqueda = True

        except:
            titulo = 'Edición de datos'
            mensaje = 'Mensaje de error'
            messagebox.showerror(titulo, mensaje)

    def eliminar_datos(self):
        try:
            self.id_cliente = self.tabla.item(self.tabla.selection())['text']
            eliminar(self.id_cliente)

            self.tabla_cliente()
            self.id_cliente = None
        except:
            titulo = 'Eliminar un Registro'
            mensaje = 'No ha seleccionado nigun registro'
            messagebox.showerror(titulo, mensaje)

    def limpiar_pantalla(self):
        for i in list(self.children.values()):
            i.destroy()

        for i in range(6):
            self.rowconfigure(i, weight=0)
        for i in range(3):
            self.columnconfigure(i, weight=0)

class Frame_registrar_usuario(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.menu_de_opciones = Frame_menu(self.root)
        self.pack(side='top', fill='both', expand=True)
        self.registrar_usuario()
        self.tabla_usuarios()

    def registrar_usuario(self):
        for i in range(9):
            self.rowconfigure(i, weight=1)
        for i in range(3):
            self.columnconfigure(i, weight=1)
        self.label_usuario = customtkinter.CTkLabel(self, text = 'Usuario: ', font = ('Arial', 12, 'bold'))
        self.label_usuario.grid(row = 0, column = 0, padx = 10, pady = 10, sticky='e')

        self.label_contraseña = customtkinter.CTkLabel(self, text='Contraseña: ', font=('Arial', 12, 'bold'))
        self.label_contraseña.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.label_acceso = customtkinter.CTkLabel(self, text = 'Nivel de acceso: ', font = ('Arial', 12, 'bold'))
        self.label_acceso.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 10, sticky='n')

        self.usuario_nombre = tk.StringVar()
        self.entry_usuario = customtkinter.CTkEntry(self, font=('Arial', 12), textvariable = self.usuario_nombre)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.usuario_contraseña = tk.StringVar()
        self.entry_contraseña = customtkinter.CTkEntry(self, font=('Arial', 12), textvariable=self.usuario_contraseña)
        self.entry_contraseña.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        #niveles de acceso con un boton estilo radio
        self.nivel_acceso = tk.StringVar()
        self.nivel_acceso_check1 = customtkinter.CTkRadioButton(self, text="bajo", font=('Arial', 12, 'bold'), variable=self.nivel_acceso, value="bajo")
        self.nivel_acceso_check1.grid(row=3, column=0, padx=10, pady=10)

        self.nivel_acceso_check2 = customtkinter.CTkRadioButton(self, text="medio", font=('Arial', 12, 'bold'), variable=self.nivel_acceso, value="medio")
        self.nivel_acceso_check2.grid(row=3, column=1, padx=10, pady=10)

        self.nivel_acceso_check3 = customtkinter.CTkRadioButton(self, text="alto", font=('Arial', 12, 'bold'), variable=self.nivel_acceso, value="alto")
        self.nivel_acceso_check3.grid(row=3, column=2, padx=10, pady=10)

        self.boton_atras = customtkinter.CTkButton(self, text="Atras", font=('Arial', 12, 'bold'), command = self.login)
        self.boton_atras.grid(row=6, column=1, padx=10, pady=10)

        self.boton_registrar_usuario = customtkinter.CTkButton(self, text="Registrar", font=('Arial', 12, 'bold'), command = self.registrar_usuario_nuevo)
        self.boton_registrar_usuario.grid(row=7, column=1, padx=10, pady=10)

        self.crear_tabla_boton = customtkinter.CTkButton(self, text="Crear tabla", font=('Arial', 12, 'bold'), command = crear_tabla_usuarios)
        self.crear_tabla_boton.grid(row=8, column=1, padx=10, pady=10)

    def registrar_usuario_nuevo(self):
        self.usuario = Usuario(
            self.usuario_nombre.get(),
            self.usuario_contraseña.get(),
            self.nivel_acceso.get(),
        )

        guadar_usuario(self.usuario)
        self.tabla_usuarios()

    def login(self):
        self.destroy()
        app = Frame_login(root = self.root)

    def tabla_usuarios(self):
        #Nuevo widget para la tabla
        frame_tabla = tk.Frame(self, bg='black')
        frame_tabla.grid(row=5, column=0, columnspan=3,padx=20, sticky='we')

        frame_tabla.rowconfigure(0, weight=1)
        for i in range(3):
            frame_tabla.columnconfigure(i, weight=1)

        #Recuperar la lista
        self.lista_usuarios = listar_usuarios()
        self.lista_usuarios.reverse()

        self.tabla  = ttk.Treeview(frame_tabla, 
        column = ('Usuario', 'Contraseña', 'Tipo'))
        self.tabla.grid(row=0, column=0, columnspan=3, sticky = 'ew')

        # Scrollbar para la tabla si excede 10 registros
        self.scroll = ttk.Scrollbar(frame_tabla,
        orient = 'vertical', command = self.tabla.yview)
        self.tabla.configure(yscrollcommand = self.scroll.set)
        self.scroll.grid(row = 0, column = 2, sticky = 'nse')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='USUARIO')
        self.tabla.heading('#2', text='Contraseña')
        self.tabla.heading('#3', text='TIPO')

        # Iterar la lista
        for p in self.lista_usuarios:
            self.tabla.insert('',0, text=p[0], 
            values = (p[1], p[2], p[3]))

class Frame_menu(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root, fg_color='transparent')
        self.root = root
        self.pack(side='left', fill='both', expand=False)
        self.lift()

        self.menu_crear()
        self.menu_frame.grid_remove()

    def menu_crear(self):
        # Crear el disparador del menú
        self.trigger_label = customtkinter.CTkButton(self, text="Menú", font=("Arial", 12, "bold"))
        self.trigger_label.grid(row=0, column=0, sticky='w')
        self.trigger_label.bind("<Button-1>", lambda event: self.toggle_menu())

        # Crear el menú usando button
        self.menu_frame = customtkinter.CTkFrame(self)
        self.menu_frame.grid(row=1, column=0, sticky='w')

        self.opcion_1 = customtkinter.CTkButton(self.menu_frame, text='Añadir Cliente', font=('Arial', 12, 'bold'), command = self.registrar_cliente)
        self.opcion_1.grid(row=0, column=0, padx=10, pady=10)

        self.opcion_4 = customtkinter.CTkButton(self.menu_frame, text='Registrar Usuario', font=('Arial', 12, 'bold'), command = self.registrarse)
        self.opcion_4.grid(row=3, column=0, padx=10, pady=10)

        self.opcion_5 = customtkinter.CTkButton(self.menu_frame, text='Salir', font=('Arial', 12, 'bold'), command = self.login)
        self.opcion_5.grid(row=4, column=0, padx=10, pady=10)

        self.opcion_6 = customtkinter.CTkButton(self.menu_frame, text='Color', font=('Arial', 12, 'bold'), command = self.cambiar_color)
        #self.opcion_6.grid(row=5, column=0, padx=10, pady=10)

    def toggle_menu(self):
        if self.menu_frame.winfo_viewable():
            self.menu_frame.grid_remove()
        else:
            self.menu_frame.grid()

    def registrar_cliente(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        app = Frame_registrar_cliente(root = self.root)

    def registrarse(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(menu=False)
        app = Frame_registrar_usuario(root = self.root)

    def login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(menu=False)
        app = Frame_login(root = self.root)

    def cambiar_color(self):
        global color, color_2, color_3, bg
        if color == 'black':
            color = 'white'
            color_2 = 'black'
            color_3 = 'white'
            bg='img/bg2.png'
        else:
            color = 'black'
            color_2 = 'white'
            color_3 = '#3f3f3f'
            bg='img/bg1.png'

        style = ttk.Style()
        style.theme_use("clam")  # Usar el tema "clam" para obtener un fondo oscuro

        style.configure("Treeview", background=color_3, foreground=color_2, fieldbackground=color_3)
        style.configure("Treeview.Heading", background=color_3, foreground=color_2)
        style.map("Treeview", background=[("selected", color_2)], foreground=[("selected", color_3)])

        self.login()
