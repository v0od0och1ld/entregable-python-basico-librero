from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import Tk, ttk



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


try:
    conexion()
    crear_tabla_libros()    
except:
    print("Hay un error en la creación de la tabla de libros o la misma ya fue creada anteriormente")
try:
    conexion()
    agregar_generos_literarios()    
except:
    print("Hay un error en el agregado de los géneros literarios o los mismos ya fueron creados anteriormente")

try:
    conexion()
    agregar_editoriales()    
except:
    print("Hay un error en el agregado de las editoriales o las mismos ya fueron creados anteriormente")

try:
    conexion()
    crear_tabla_categorias()    
except:
    print("Hay un error en la creación de la tabla de categorias o la misma ya fue creada anteriormente")
try:
    conexion()
    crear_tabla_autores()    
except:
    print("Hay un error en la creación de la tabla de autores o la misma ya fue creada anteriormente")    
try:
    conexion()
    crear_tabla_editorial()    
except:
    print("Hay un error en la creación de la tabla de editoriales o la misma ya fue creada anteriormente")

def nuevo_libro():
    pass

def modificar_libro():
    pass

def eliminar_libro():
    pass



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

    return resultado
    
    
    
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

    return resultado
    
    
    
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


root = Tk()
root.title("Librero")

menubar = Menu(root) #Menu

menu_archivo = Menu(menubar, tearoff=0) #tearoff es para subniveles de menu

#Libros
submenu_libros = Menu(menu_archivo, tearoff=0)
submenu_libros.add_command(label="Nuevo", command=nuevo_libro)
submenu_libros.add_command(label="Modificar", command=modificar_libro)
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
        



root.mainloop()
