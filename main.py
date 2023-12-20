from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import Tk, ttk
import tkinter as tk
import re

def limpiar_treeview(tree):
    # Eliminar todos los elementos del Treeview
    for item in tree.get_children():
        tree.delete(item)


def cargar_libros(tree):

    

    conn = conexion()
    cursor = conn.cursor()

    sql = """
        SELECT l.id, l.titulo, a.autor, e.editorial, l.anio, c.categoria, l.comentario
        FROM libros AS l 
        INNER JOIN autores AS a ON a.id = l.autor 
        INNER JOIN editoriales AS e ON e.id = l.editorial
        INNER JOIN categorias AS c ON c.id = l.categoria
    """

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)
    except:
        pass


def conexion():
    conn = sqlite3.connect("base_librero.db")
    return conn

def crear_tabla_libros():
    conn = conexion()
    cursor = conn.cursor()
    sql = """CREATE TABLE libros
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             titulo varchar(255) NOT NULL,
             autor integer,
             editorial integer,
             anio integer,
             categoria integer,
             comentario varchar(255))
    """
    cursor.execute(sql)
    conn.commit()

def crear_tabla_categorias():   
    conn = conexion()
    cursor = conn.cursor() 
    sql1 = """CREATE TABLE categorias
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             categoria varchar(255) NOT NULL)
    """
    cursor.execute(sql1)
    conn.commit()

def agregar_generos_literarios():
    conn = conexion()
    cursor = conn.cursor()

    generos = ["Novela", "Poesía", "Drama", "Ensayo", "Ciencia ficción", "Fantasía", "Misterio", "Terror", "Aventura"]

    cursor.execute("SELECT categoria FROM categorias")
    categorias_existentes = cursor.fetchall()
    categorias_existentes = [cat[0] for cat in categorias_existentes]
        
    for genero in generos:
        if genero not in categorias_existentes:
            sql = "INSERT INTO categorias (categoria) VALUES (?)"
            cursor.execute(sql, (genero,))
    
    conn.commit()

def agregar_editoriales():
    conn = conexion()
    cursor = conn.cursor()

    editoriales = ["Planeta", "Sudamericana", "Siglo XXI Editores", "Paidós", "Interzona", "Emece", "El Ateneo", "Galerna", "Adriana Hidalgo", "Ediciones Continente"]

    cursor.execute("SELECT editorial FROM editoriales")
    editoriales_existentes = cursor.fetchall()
    editoriales_existentes = [edito[0] for edito in editoriales_existentes]
        
    for editorial in editoriales:
        if editorial not in editoriales_existentes:
            sql = "INSERT INTO editoriales (editorial) VALUES (?)"
            cursor.execute(sql, (editorial,))
    
    conn.commit()


def crear_tabla_autores():
    conn = conexion()
    cursor = conn.cursor()
    sql = """CREATE TABLE autores
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             autor varchar(50))
    """
    cursor.execute(sql)
    conn.commit()

def crear_tabla_editorial():
    conn = conexion()
    cursor = conn.cursor()
    sql = """CREATE TABLE editoriales
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             editorial varchar(50))
    """
    cursor.execute(sql)
    conn.commit()

def agregar_autores():
    conn = conexion()
    cursor = conn.cursor()

    autores = ["Jorge Luis Borges", "Julio Cortázar", "Adolfo Bioy Casares", "Ernesto Sabato", "Marta Lynch", "Leopoldo Marechal"]

    cursor.execute("SELECT autor FROM autores")
    autores_existentes = cursor.fetchall()
    autores_existentes = [aut[0] for aut in autores_existentes]
        
    for autor in autores:
        if autor not in autores_existentes:
            sql = "INSERT INTO autores (autor) VALUES (?)"
            cursor.execute(sql, (autor,))
    
    conn.commit()


try:
    conexion()
    crear_tabla_libros()    
except:
    print("Hay un error en la creación de la tabla de libros o la misma ya fue creada anteriormente")


############GENEROS############
try:
    conexion()
    crear_tabla_categorias()    
except:
    print("Hay un error en la creación de la tabla de categorias o la misma ya fue creada anteriormente")

try:
    conexion()
    agregar_generos_literarios()    
except:
    print("Hay un error en el agregado de los géneros literarios o los mismos ya fueron creados anteriormente")
############GENEROS##############
###########AUTORES###############
try:
    conexion()
    crear_tabla_autores()    
except:
    print("Hay un error en la creación de la tabla de autores o la misma ya fue creada anteriormente")    

try:
    conexion()
    agregar_autores()    
except:
    print("Hay un error en el agregado de autores o los mismos ya fueron creados anteriormente")

###########AUTORES################
###########EDITORIAL##############
try:
    conexion()
    crear_tabla_editorial()    
except:
    print("Hay un error en la creación de la tabla de editoriales o la misma ya fue creada anteriormente")

try:
    conexion()
    agregar_editoriales()    
except:
    print("Hay un error en el agregado de las editoriales o las mismos ya fueron creados anteriormente")



###########EDITORIAL##############





##################                 ################     
################## CRUD CATEGORIA  ################
##################                 ################
def buscar_categoria(nombre_categoria):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM categorias WHERE categoria = ?"

    cursor.execute(sql, (nombre_categoria,))
    resultado = cursor.fetchone()

    return resultado

def buscar_categorias():
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM categorias order by categoria asc"

    cursor.execute(sql)
    resultado = cursor.fetchall()

    categorias_formateadas = [f"{categoria[0]} {categoria[1]}" for categoria in resultado] #CAMBIAR

    return categorias_formateadas
    
    
    
# Graba en la bd la nueva categoria
def guardar_categoria(nombre_categoria):
    conn = conexion()
    cursor = conn.cursor()
    sql = "INSERT INTO categorias (categoria) VALUES(?)"
    try:
        cursor.execute(sql, (nombre_categoria,))
        print(f"Categoría guardada: {nombre_categoria}")
    except:
        print(f"Error al guardar la Categoría {nombre_categoria}")
    conn.commit()


def guardar_mod_categoria(nombre, categoriamod):
    conn = conexion()
    cursor = conn.cursor()
    sql = "UPDATE categorias SET categoria = ? WHERE categoria = ?"
    try:       
        cursor.execute(sql, (categoriamod, nombre))
        conn.commit()
        
        return 1        
    except:
        conn.close()  


# ventana para agregar una nueva categoria
def nueva_categoria():    
    def guardar_categoriain():
        categoria = entry_categoria.get()

        #Valida los caracteres ingresados
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(categoria)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados

        resultado = buscar_categoria(categoria)
        if resultado:            
            label_aviso.config(text="Categoría Existente", fg="red")
            showerror("Error", "Categoría Existente") 
            top.after(0, lambda: top.focus_force())           
        else:            
            guardar_categoria(categoria)
            label_aviso.config(text=f"Categoría '{categoria}' Guardada", fg="green")
            showinfo("Guardado", "Categoría guardada") 
            top.after(0, lambda: top.focus_force())           
            entry_categoria.delete(0, 'end') 

    top = Toplevel()
    top.title("Nueva Categoría")
    top.geometry("300x150")
    

    label_categoria = Label(top, text="Ingrese nueva Categoría:")
    label_categoria.pack()

    entry_categoria = Entry(top)
    entry_categoria.pack()

    btn_guardar = Button(top, text="Guardar", command=guardar_categoriain)
    btn_guardar.pack()
    label_aviso = Label(top)  
    label_aviso.pack()  

#Ventana para modificar categorias
def modificar_categoria():
    nombre = None
    def guardar_modcategoriain(nombre):
        categoriamod = entry_nombre.get()  

        #Valida los caracteres ingresados
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(categoriamod)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados



        resultado = guardar_mod_categoria(nombre, categoriamod)
        if resultado:            
            label_aviso.config(text="Modificación exitosa", fg="Green")
            showinfo("Modificar", "Categoría modificada") 
            top.after(1000, lambda: top.destroy())
            top.after(1000, lambda: root.focus_force())     
        else:            
            label_aviso.config(text=f"Error al modificar la categoría", fg="red")            
            showerror("Error", "Error al modificar la categoría")
            top.after(0, lambda: top.focus_force())
            

    #funcion para pasar texto al combobox
    def seleccionar_item(event):
        nonlocal nombre
        valor_seleccionado = combo.get()
        #nombre = valor_seleccionado.split(' ')[1]
        partes = valor_seleccionado.split(' ', 1)
        if len(partes) > 1:
            nombre = partes[1]
            entry_nombre.delete(0, 'end')
            entry_nombre.insert(0, nombre)
            

    top = Toplevel()
    top.title("Modificar Categoría")
    top.geometry("300x150")

    ####Combobox 
    categorias = buscar_categorias()        
    combo = ttk.Combobox(top, values=categorias)
    combo.pack()
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox
   
    entry_nombre = ttk.Entry(top)
    entry_nombre.pack(pady=10)
    
    btn_guardar = Button(top, text="Guardar modificación", command=lambda: guardar_modcategoriain(nombre))
    btn_guardar.pack()
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes


def borrar_categoria(nombre):
    conn = conexion()
    cursor = conn.cursor()
    sql = "DELETE FROM categorias WHERE categoria = ?"
        
    try:       
        cursor.execute(sql, (nombre,))
        conn.commit()
        conn.close()        
        return 1        
    except:
        conn.close()  

def eliminar_categoria():
    nombre = None
    def eliminar_categoriain(nombre):
        #categoriamod = entry_nombre.get()        
        resultado = borrar_categoria(nombre)
        if resultado:            
            label_aviso.config(text="Borrado exitosa", fg="Green")  
            showinfo("Borrado", "Borrado Exitoso")
            top.after(1000, lambda: top.destroy())
            top.after(1000, lambda: root.focus_force())     
        else:            
            label_aviso.config(text=f"Error al borrar la categoría", fg="red") 
            showerror("Error", "Error al borrar la categoría")
            top.after(0, lambda: top.focus_force())            
            

    #funcion para pasar la variable del combobox
    def seleccionar_item(event):
        nonlocal nombre
        valor_seleccionado = combo.get()
        #nombre = valor_seleccionado.split(' ')[1]     
        partes = valor_seleccionado.split(' ', 1)
        if len(partes) > 1:
            nombre = partes[1]

    top = Toplevel()
    top.title("Borrar Categoría")
    top.geometry("300x150")
    
    ####Combobox 
    categorias = buscar_categorias()        
    combo = ttk.Combobox(top, values=categorias)
    combo.pack(pady=10)
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox   
    
    btn_borrar = Button(top, text="Borrar", command=lambda: eliminar_categoriain(nombre))
    btn_borrar.pack(pady=10)
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes

##################                 ################     
################## CRUD CATEGORIA  ################
##################                 ################

##################                 ################     
################## CRUD EDITORIAL  ################
##################                 ################
def buscar_editorial(nombre_editorial):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM editoriales WHERE editorial = ?"

    cursor.execute(sql, (nombre_editorial,))
    resultado = cursor.fetchone()

    return resultado

def buscar_editoriales():
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM editoriales order by editorial asc"

    cursor.execute(sql)
    resultado = cursor.fetchall()

    editoriales_formateadas = [f"{editorial[0]} {editorial[1]}" for editorial in resultado] #CAMBIAR

    return editoriales_formateadas
    
    
    
# Graba en la bd la nueva editorial
def guardar_editorial(nombre_editorial):
    conn = conexion()
    cursor = conn.cursor()
    sql = "INSERT INTO editoriales (editorial) VALUES(?)"
    try:
        cursor.execute(sql, (nombre_editorial,))
        print(f"Categoría guardada: {nombre_editorial}")
    except:
        print(f"Error al guardar la editorial {nombre_editorial}")
    conn.commit()


def guardar_mod_editorial(nombre, editorialmod):
    conn = conexion()
    cursor = conn.cursor()
    sql = "UPDATE editoriales SET editorial = ? WHERE editorial = ?"
    try:       
        cursor.execute(sql, (editorialmod, nombre))
        conn.commit()
        
        return 1        
    except:
        conn.close()  


# ventana para agregar una nueva editorial
def nueva_editorial():    
    def guardar_editorialin():
        editorial = entry_editorial.get()
        
        #Valida los caracteres ingresados
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(editorial)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados


        resultado = buscar_editorial(editorial)
        if resultado:            
            label_aviso.config(text="Editorial Existente", fg="red")
            showerror("Error", "Editorial Existente") 
            top.after(0, lambda: top.focus_force())           
        else:            
            guardar_editorial(editorial)
            label_aviso.config(text=f"Editorial '{editorial}' Guardada", fg="green")
            showinfo("Guardado", "Editorial guardada") 
            top.after(0, lambda: top.focus_force())           
            entry_editorial.delete(0, 'end') 

    top = Toplevel()
    top.title("Nueva Editorial")
    top.geometry("300x150")
    

    label_editorial = Label(top, text="Ingrese nueva Editorial:")
    label_editorial.pack()

    entry_editorial = Entry(top)
    entry_editorial.pack()

    btn_guardar = Button(top, text="Guardar", command=guardar_editorialin)
    btn_guardar.pack()
    label_aviso = Label(top)  
    label_aviso.pack()  

#Ventana para modificar editorial
def modificar_editorial():
    nombre = None
    def guardar_modeditorialin(nombre):
        editorialmod = entry_nombre.get()
        #Valida los carácteres ingresados
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(editorialmod)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return        
        #Valida los carácteres ingresados
        resultado = guardar_mod_editorial(nombre, editorialmod)
        if resultado:            
            label_aviso.config(text="Modificación exitosa", fg="Green")
            showinfo("Modificar", "Editorial modificada") 
            top.after(1000, lambda: top.destroy())
            top.after(1000, lambda: root.focus_force())     
        else:            
            label_aviso.config(text=f"Error al modificar la Editorial", fg="red")            
            showerror("Error", "Error al modificar la Editorial")
            top.after(0, lambda: top.focus_force())
            

    #funcion para pasar texto al combobox
    def seleccionar_item(event):
        nonlocal nombre
        valor_seleccionado = combo.get()
        #nombre = valor_seleccionado.split(' ')[1]
        partes = valor_seleccionado.split(' ', 1)
        if len(partes) > 1:
            nombre = partes[1]
            entry_nombre.delete(0, 'end')
            entry_nombre.insert(0, nombre)   

    top = Toplevel()
    top.title("Modificar Categoría")
    top.geometry("300x150")
    
    ####Combobox 
    editoriales = buscar_editoriales()        
    combo = ttk.Combobox(top, values=editoriales)
    combo.pack()
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox
   
    entry_nombre = ttk.Entry(top)
    entry_nombre.pack(pady=10)
    
    btn_guardar = Button(top, text="Guardar modificación", command=lambda: guardar_modeditorialin(nombre))
    btn_guardar.pack()
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes


def borrar_editorial(nombre):
    conn = conexion()
    cursor = conn.cursor()
    sql = "DELETE FROM editoriales WHERE editorial = ?"
        
    try:       
        cursor.execute(sql, (nombre,))
        conn.commit()
        conn.close()        
        return 1        
    except:
        conn.close()  

def eliminar_editorial():
    nombre = None
    def eliminar_editorialin(nombre):
        #categoriamod = entry_nombre.get()        
        resultado = borrar_editorial(nombre)
        if resultado:            
            label_aviso.config(text="Borrado exitosa", fg="Green")  
            showinfo("Borrado", "Borrado Exitoso")
            top.after(1000, lambda: top.destroy())
            top.after(1000, lambda: root.focus_force())     
        else:            
            label_aviso.config(text=f"Error al borrar la editorial", fg="red") 
            showerror("Error", "Error al borrar la editorial")
            top.after(0, lambda: top.focus_force())            
            

    #funcion para pasar la variable del combobox
    def seleccionar_item(event):
        nonlocal nombre
        valor_seleccionado = combo.get()
        #nombre = valor_seleccionado.split(' ')[1]       
        partes = valor_seleccionado.split(' ', 1)   
        if len(partes) > 1:
            nombre = partes[1]

    top = Toplevel()
    top.title("Borrar Editorial")
    top.geometry("300x150")
    
    ####Combobox 
    editoriales = buscar_editoriales()        
    combo = ttk.Combobox(top, values=editoriales)
    combo.pack(pady=10)
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox   
    
    btn_borrar = Button(top, text="Borrar", command=lambda: eliminar_editorialin(nombre))
    btn_borrar.pack(pady=10)
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes

##################                  ################     
################## CRUD EDITORIAL   ################
##################                  ################

##################                 ################     
################## CRUD AUTOR      ################
##################                 ################
def buscar_autor(nombre_autor):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM autores WHERE autor = ?"

    cursor.execute(sql, (nombre_autor,))
    resultado = cursor.fetchone()

    return resultado

def buscar_autores():
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM autores order by autor asc"

    cursor.execute(sql)
    resultado = cursor.fetchall()

    autores_formateados = [f"{autor[0]} {autor[1]}" for autor in resultado] #CAMBIAR
    

    return autores_formateados #CAMBIAR EN LOS OTROS CRUD
    
    
    
# Graba en la bd el nuevo autor
def guardar_autor(nombre_autor):
    conn = conexion()
    cursor = conn.cursor()
    sql = "INSERT INTO autores (autor) VALUES(?)"
    try:
        cursor.execute(sql, (nombre_autor,))
        print(f"Autor guardado: {nombre_autor}")
    except:
        print(f"Error al guardar el autor {nombre_autor}")
    conn.commit()


def guardar_mod_autor(nombre, autormod):
    conn = conexion()
    cursor = conn.cursor()
    sql = "UPDATE autores SET autor = ? WHERE autor = ?"
    try:       
        cursor.execute(sql, (autormod, nombre))
        conn.commit()
        
        return 1        
    except:
        conn.close()  


# ventana para agregar un nuevo autor
def nuevo_autor():    
    def guardar_autorin():
        autor = entry_autor.get()

        #Valida los caracteres ingresados
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(autor)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados

        resultado = buscar_autor(autor)
        if resultado:            
            label_aviso.config(text="Autor Existente", fg="red")
            showerror("Error", "Autor Existente") 
            top.after(0, lambda: top.focus_force())           
        else:            
            guardar_autor(autor)
            label_aviso.config(text=f"Autor '{autor}' Guardada", fg="green")
            showinfo("Guardado", "Autor guardado") 
            top.after(0, lambda: top.focus_force())           
            entry_autor.delete(0, 'end') 

    top = Toplevel()
    top.title("Nuevo autor")
    top.geometry("300x150")
    

    label_autor = Label(top, text="Ingrese nuevo Autor:")
    label_autor.pack()

    entry_autor = Entry(top)
    entry_autor.pack()

    btn_guardar = Button(top, text="Guardar", command=guardar_autorin)
    btn_guardar.pack()
    label_aviso = Label(top)  
    label_aviso.pack()  

#Ventana para modificar autores
def modificar_autor():
    nombre = None
    def guardar_modautorin(nombre):
        autormod = entry_nombre.get()  

        #Valida los caracteres ingresados
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(autormod)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados

        resultado = guardar_mod_autor(nombre, autormod)
        if resultado:            
            label_aviso.config(text="Modificación exitosa", fg="Green")
            showinfo("Modificar", "Autor modificado") 
            top.after(1000, lambda: top.destroy())
            top.after(1000, lambda: root.focus_force())     
        else:            
            label_aviso.config(text=f"Error al modificar autor", fg="red")            
            showerror("Error", "Error al modificar autor")
            top.after(0, lambda: top.focus_force())
            

    #funcion para pasar texto al combobox
    #def seleccionar_item(event):
    #    nonlocal nombre
    #    valor_seleccionado = combo.get()
    #    nombre = valor_seleccionado.split(' ')[1]
    #    entry_nombre.delete(0, 'end')
    #    entry_nombre.insert(0, nombre)    
    def seleccionar_item(event):
        nonlocal nombre
        valor_seleccionado = combo.get()
        partes = valor_seleccionado.split(' ', 1)
        if len(partes) > 1:
            nombre = partes[1]
            entry_nombre.delete(0, 'end')
            entry_nombre.insert(0, nombre)
            
    top = Toplevel()
    top.title("Modificar Autor")
    top.geometry("300x150")
    
    ####Combobox 
    autores = buscar_autores()        
    combo = ttk.Combobox(top, values=autores)
    combo.pack()
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox
   
    entry_nombre = ttk.Entry(top)
    entry_nombre.pack(pady=10)
    
    btn_guardar = Button(top, text="Guardar modificación", command=lambda: guardar_modautorin(nombre))
    btn_guardar.pack()
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes


def borrar_autor(nombre):
    conn = conexion()
    cursor = conn.cursor()
    sql = "DELETE FROM autores WHERE autor = ?"
        
    try:       
        cursor.execute(sql, (nombre,))
        conn.commit()
        conn.close()        
        return 1        
    except:
        conn.close()  

def eliminar_autor():
    nombre = None
    def eliminar_autorin(nombre):
        #categoriamod = entry_nombre.get()        
        resultado = borrar_autor(nombre)
        if resultado:            
            label_aviso.config(text="Borrado exitosa", fg="Green")  
            showinfo("Borrado", "Borrado Exitoso")
            top.after(1000, lambda: top.destroy())
            top.after(1000, lambda: root.focus_force())     
        else:            
            label_aviso.config(text=f"Error al borrar autor", fg="red") 
            showerror("Error", "Error al borrar autor")
            top.after(0, lambda: top.focus_force())            
            

    #funcion para pasar la variable del combobox
    def seleccionar_item(event):
        nonlocal nombre
        valor_seleccionado = combo.get()
        #nombre = valor_seleccionado.split(' ')[1]    
        partes = valor_seleccionado.split(' ', 1)
        if len(partes) > 1:
            nombre = partes[1]

    top = Toplevel()
    top.title("Borrar Autor")
    top.geometry("300x150")
    
    ####Combobox 
    autores = buscar_autores()        
    combo = ttk.Combobox(top, values=autores)
    combo.pack(pady=10)
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox   
    
    btn_borrar = Button(top, text="Borrar", command=lambda: eliminar_autorin(nombre))
    btn_borrar.pack(pady=10)
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes

##################                 ################     
################## CRUD AUTOR      ################
##################                 ################

##################                 ################     
################## CRUD LIBRO      ################
##################                 ################
#def nuevo_libro():
#    pass





def buscar_libro(nombre_libro):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM libros WHERE titulo = ?"

    #0 id
    #1 titulo
    #2 autor
    #3 editorial
    #4 anio
    #5 categoria
    #6 comentario

    cursor.execute(sql, (nombre_libro,))
    resultado = cursor.fetchone()

    return resultado

def buscar_libros():
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM libros order by libro asc"

    cursor.execute(sql)
    resultado = cursor.fetchall()

    libros_formateados = [f"{libro[0]} {libro[1]}" for libro in resultado] #CAMBIAR

    return libros_formateados

def obtener_id_autor(autor):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT id FROM autores WHERE autor = ?"
    
    cursor.execute(sql, (autor,))
    resultado = cursor.fetchone()

    return resultado    

def obtener_id_editorial(editorial):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT id FROM editoriales WHERE editorial = ?"
    
    cursor.execute(sql, (editorial,))
    resultado = cursor.fetchone()

    return resultado    

def obtener_id_categoria(categoria):
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT id FROM categorias WHERE categoria = ?"
    
    cursor.execute(sql, (categoria,))
    resultado = cursor.fetchone()

    return resultado    
    
# Graba en la bd el nuevo libro
def guardar_libro(nombre_libro, autor, editorial, anio, genero, comentario):
    indice_espacio_autor = autor.find(' ')
    autor_sin_numero = autor[indice_espacio_autor + 1:]        
    autor_id = obtener_id_autor(autor_sin_numero)

    indice_espacio_editorial = editorial.find(' ')
    editorial_sin_numero = editorial[indice_espacio_editorial + 1:]        
    editorial_id = obtener_id_editorial(editorial_sin_numero)
    
    
    indice_espacio_genero = genero.find(' ')
    genero_sin_numero = genero[indice_espacio_genero + 1:] 
    genero_id = obtener_id_categoria(genero_sin_numero)


    conn = conexion()
    cursor = conn.cursor()

    #sql = "INSERT INTO libros (titulo, autor, editorial, anio, categoria, comentario) VALUES(?, ?, ?, ?, ?, ?)" 

    sql = ("""INSERT INTO libros (titulo, autor, editorial, anio, categoria, comentario) 
                   VALUES ('{}',{}, {}, {},{},'{}')""".format(nombre_libro, autor_id[0], editorial_id[0], anio, genero_id[0], comentario))
                


    try:
        #cursor.execute(sql, (nombre_libro, autor_id[0], editorial_id[0], anio, genero_id[0], comentario))
        cursor.execute(sql)
        conn.commit()

        print(f"Libro guardado: {nombre_libro}")
    except Exception as e:
        print(f"Error al guardar el libro {nombre_libro}: {e}")
        conn.rollback() 
    finally:
        conn.close()  


def guardar_mod_libro(nombre, libromod):
    conn = conexion()
    cursor = conn.cursor()
    sql = "UPDATE libros SET libro = ? WHERE libro = ?"
    try:       
        cursor.execute(sql, (libromod, nombre))
        conn.commit()
        
        return 1        
    except:
        conn.close()  


# ventana para agregar una nueva categoria
def nuevo_libro():
    def guardar_libroin():
        libro = entry_libro.get()
        autor = combo_autores.get()
        editorial = combo_editoriales.get()
        genero = combo_categorias.get()
        anio = entry_anio.get()
        comentario = text_comentario.get("1.0", "end-1c")



        #Valida los caracteres ingresados en el titulo
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(libro)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados en el titulo
        #Valida los caracteres ingresados en el año

        patron = re.compile("^(1\d{3}|2\d{3})$")  # Expresión regular para años entre 1000 y 2999
        match = patron.match(anio)

        if not match:
            showerror("Error", "El año es incorrecto") 
            top.after(0, lambda: top.focus_force()) 
            return
        
        #Valida los caracteres ingresados en el año
        #Valida los caracteres ingresados en los comentarios
        patron = re.compile("^[a-zA-Z0-9 ]+$")
        match = patron.search(comentario)

        if not match:
            showerror("Error", "Algunos carácteres introducidos no son válidos") 
            top.after(0, lambda: top.focus_force()) 
            return
        #Valida los caracteres ingresados en los comentarios


        resultado = buscar_libro(libro)
        if resultado:            
            label_aviso.config(text="Libro Existente", fg="red")
            showerror("Error", "Libro Existente") 
            top.after(0, lambda: top.focus_force())           
        else:            
            guardar_libro(libro, autor, editorial, anio, genero, comentario)
            label_aviso.config(text=f"Libro '{libro}' Guardado", fg="green")
            showinfo("Guardado", "Libro guardado") 
            top.after(0, lambda: top.focus_force())           
            entry_libro.delete(0, 'end') 
            limpiar_treeview(tree)
            cargar_libros(tree)

    # Verifica la longitud del campo de comentarios
    def limitar_longitud(event):
        comentario = text_comentario.get("1.0", "end-1c")
        if len(comentario) > 255:
            text_comentario.delete("end-1c", "end")  

    top = Toplevel()
    top.title("Nuevo Libro")
    top.geometry("300x400")
    

    label_libro = Label(top, text="Ingrese nuevo Libro:")
    label_libro.pack()

    entry_libro = Entry(top)
    entry_libro.pack()

    ####Combobox autor
    label_autor = Label(top, text="Autor:")
    label_autor.pack()
    autores = buscar_autores()        
    combo_autores = ttk.Combobox(top, values=autores)
    combo_autores.pack()
    ####Combobox autor
    ####Combobox genero
    label_genero = Label(top, text="Genero:")
    label_genero.pack()
    categorias = buscar_categorias()        
    combo_categorias = ttk.Combobox(top, values=categorias)
    combo_categorias.pack()
    ####Combobox genero
    ####Combobox genero
    label_editorial = Label(top, text="Editorial:")
    label_editorial.pack()
    editoriales = buscar_editoriales()        
    combo_editoriales = ttk.Combobox(top, values=editoriales)
    combo_editoriales.pack()
    ####Combobox genero
    ####Entry año
    label_anio = Label(top, text="Año:")
    label_anio.pack()
    
    entry_anio = Entry(top)
    entry_anio.pack()
    ####Entry año
    #### Text comentario ####
    label_comentario = Label(top, text="Comentarios:")
    label_comentario.pack()
    text_comentario = Text(top, height=9, width=30)  
    text_comentario.pack()
    text_comentario.bind("<Key>", limitar_longitud)
    #### Text comentario ####



    btn_guardar = Button(top, text="Guardar", command=guardar_libroin)
    btn_guardar.pack()
    label_aviso = Label(top)  
    label_aviso.pack()  

def eliminar_libro():    
    def eliminar_libro_seleccionado():
        seleccion = tree.focus()
        datos = tree.item(seleccion)
        libro_id = datos['values'][0] 

        


        
        resultado = eliminar_libro_db(libro_id)
        if resultado:        
            tree.delete(seleccion)
            showinfo("Borrado", "Libro Borrado")             
        else:
            showerror("Error", "Error al borrar") 

    top = Toplevel()
    top.title("Eliminar Libro")
    label_info = Label(top, text="Seleccione un libro en el treeview y presione el botón para borrar")
    label_info.pack()
    

    top.geometry("300x150")

    btn_eliminar = Button(top, text="Eliminar Libro", command=eliminar_libro_seleccionado)
    btn_eliminar.pack()

def eliminar_libro_db(libro_id):
    
    conn = conexion()
    cursor = conn.cursor()
    sql = "DELETE FROM libros WHERE id = ?"

    try:
        cursor.execute(sql, (libro_id,))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


    
    ####Combobox 
    categorias = buscar_categorias()        
    combo = ttk.Combobox(top, values=categorias)
    combo.pack(pady=10)
    combo.bind("<<ComboboxSelected>>", seleccionar_item)
    ####Combobox   
    
    btn_borrar = Button(top, text="Borrar", command=lambda: eliminar_categoriain(nombre))
    btn_borrar.pack(pady=10)
    
    #### Label de notificación de mensajes
    label_aviso = Label(top)  
    label_aviso.pack()  
    #### Label de notificación de mensajes

##################                 ################     
################## CRUD LIBRO      ################
##################                 ################


root = Tk()
root.title("Librero")

menubar = Menu(root) #Menu

menu_archivo = Menu(menubar, tearoff=0) #tearoff es para subniveles de menu

#Libros
submenu_libros = Menu(menu_archivo, tearoff=0)
submenu_libros.add_command(label="Nuevo", command=nuevo_libro)
#submenu_libros.add_command(label="Modificar", command=modificar_libro)
submenu_libros.add_command(label="Eliminar", command=eliminar_libro)
menu_archivo.add_cascade(label="Libros", menu=submenu_libros)
#Libros

#Categorias
submenu_categorias = Menu(menu_archivo, tearoff=0)
submenu_categorias.add_command(label="Nueva Categoría", command=nueva_categoria)
submenu_categorias.add_command(label="Modificar Categoría", command=modificar_categoria)
submenu_categorias.add_command(label="Eliminar Categoría", command=eliminar_categoria)
menu_archivo.add_cascade(label="Categorías", menu=submenu_categorias)
#Categorias

#Editoriales
submenu_editoriales = Menu(menu_archivo, tearoff=0)
submenu_editoriales.add_command(label="Nueva Editorial", command=nueva_editorial)
submenu_editoriales.add_command(label="Modificar Editorial", command=modificar_editorial)
submenu_editoriales.add_command(label="Eliminar Editorial", command=eliminar_editorial)
menu_archivo.add_cascade(label="Editoriales", menu=submenu_editoriales)
#Editoriales

#Autores
submenu_autores = Menu(menu_archivo, tearoff=0)
submenu_autores.add_command(label="Nuevo Autor", command=nuevo_autor)
submenu_autores.add_command(label="Modificar Autor", command=modificar_autor)
submenu_autores.add_command(label="Eliminar Autor", command=eliminar_autor)
menu_archivo.add_cascade(label="Autores", menu=submenu_autores)
#Autores

menu_archivo.add_separator()

menu_archivo.add_command(label="Salir", command=root.quit)

menubar.add_cascade(label="Archivo", menu=menu_archivo)

root.config(menu=menubar)

##### ESTE ES EL TREEVIEW

tree = ttk.Treeview(root)
tree["columns"] = ("id","titulo","autor","editorial","anio","categoria","comentario")
#tree.column("#0", width=50, minwidth=50, anchor=W)
#tree.column("col1", width=80, minwidth=80, anchor=W)
#tree.column("col2", width=80, minwidth=80, anchor=W)
tree.heading("id", text="ID")
tree.heading("titulo", text="Título")
tree.heading("autor", text="Autor")
tree.heading("editorial", text="Editorial")
tree.heading("anio", text="Año")
tree.heading("categoria", text="Categoría")
tree.heading("comentario", text="Comentario")
tree.grid(column=0, row=5, columnspan=6)

##### ESTE ES EL TREEVIEW


###### LLENAR EL TREEVIEW
cargar_libros(tree)

###### LLENAR EL TREEVIEW



root.mainloop()
