import csv


#########################################################################################
########################FUNCIONES PARA VALIDAR FECHA INGRESADA###########################
#########################################################################################


def es_bisiesto(anio):
    if (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0:             #verifica que el anio sea bisisesto
        return True
    return False


def verificar_Fecha(fecha):
    if len(fecha) != 10:
        return False
    
    pos = 0
    posOK = True                            ##verifica que la fecha este en el formato correcto, con las barras donde deben estar y la cantidad de caracteres corretos
    while pos < len(fecha):
        if pos == 2 or pos == 5:
            if fecha[pos] != '/':
                posOK = False
        else: 
            if fecha[pos] < '0' or fecha[pos] > '9':
                posOK = False
        pos += 1
    
    if posOK:
        dia = int(fecha[:2])
        mes = int(fecha[3:5])
        anio = int(fecha[6:])
        
        if mes >= 1 and mes <= 12:              #aca llama a la funcion bisiesto ya que empiezxa a depender si es bisiesto o no el anio la cnatidad de dias de algunos meses
            if mes == 2:
                if es_bisiesto(anio):
                    if dia < 1 or dia > 29:
                        return False
                else:
                    if dia < 1 or dia > 28:
                        return False
            elif mes in [4, 6, 9, 11]:
                if dia < 1 or dia > 30:
                    return False
            else:
                if dia < 1 or dia > 31:
                    return False
        else:
            return False
    
    return True                             #si esta funcion returnea TRUE es porque la fecha ingresada es correcta, si devuelve False NO

    
###################################################################################
###################################FUNCION HACER LA CLAVE 'NORMAL' ################
###################################################################################


def desencriptar(password):
   
    validos = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                 
    ClaveIncriptada = ''                  
   
    for i in password:                      
        encontrado = False              
        nueva_posicion = 0                  
   
        for c in range(len(validos)):          
           
            if i == validos[c]:                        
                nueva_posicion = (c+len(password)) % len(validos)      
           
                encontrado = True                    
             
        if encontrado:                                    
            ClaveIncriptada += validos[nueva_posicion]  
   
        else:                                  
            ClaveIncriptada +=c
           
    return ClaveIncriptada


##################################################################################
###################################FUNCION HACER LA CLAVE 'SEGURA' ###############          ###EL CODIGO DE AMBAS ES BASICAMENTE EL MISMO, PERO EL NOMBRE DISTINTO DE LA FUNCION NOS AYUDA MUCHO A LA HORA DE LLAMARLA EN DIFERENTES FUNCIONES
##################################################################################


def encriptar(password):
   
    validos = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                 
    ClaveIncriptada = ''                  
   
    for i in password:                  #password es la clave que ingreso el usuario(la estamos pasando como parametro)                
        encontrado = False              
        nueva_posicion = 0                  
   
        for c in range(len(validos)):          
           
            if i == validos[c]:                             
                nueva_posicion = (c+len(password)) % len(validos)       #si se pasa de la lista arranca dde atras para adelante   
           
                encontrado = True                    
             
        if encontrado:                                    
            ClaveIncriptada += validos[nueva_posicion]  
   
        else:                                  
            ClaveIncriptada +=c
           
    return ClaveIncriptada


############################################################################## 
###################################FUNCION INICIAR SESION ####################
##############################################################################

                                            
def inicio_sesion(usuario_actual):
    usuarios = []
    claves = []
    rol = []

    try:
        with open('usuarios.csv', 'r',encoding="utf-8") as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                usuarios.append(fila[0])
                claves.append(fila[1])
                rol.append(fila[2])

        autenticado = False                 #autenticado comienza en False, una vez que se autentica cambia  a TRUE y puede ingresar al menu principal a trabajar
    
        while not autenticado:
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            contraseña = input("Ingrese su contraseña: ")
       
            claveIncript = encriptar(contraseña)                #compara con  la clave incriptada
            claveDesencriptada = desencriptar(contraseña) 


            for i in range(len(usuarios)):
                if nombre_usuario == usuarios[i] and claveIncript == claves[i]:     #si el nombre del usuario se encuentra en la lista y en su misma posicion de la lista claves esta la clave que puso incriptada entra.
                    usuario_actual.append(nombre_usuario)
                    usuario_actual.append(contraseña)        
                    usuario_actual.append(rol[i])
                
                    return True                                                             #esta todo perfecto, ingresa al menu principal
           
            if not autenticado:                                                             #pone error ya que autenticado no cambio a TRUE(se mantuvo en False), por lo tanto lanza un error y vuelve al while
                print("Autenticación fallida. Usuario o contraseña incorrectos. Inténtelo de nuevo.")
                
                
    except FileNotFoundError:                                                                #si el archivo no existe, lo crea
        with open('usuarios.csv', "w", newline="", encoding="utf-8") as usuarios_file:
            usuarios_csv = csv.writer(usuarios_file)
            header = ["USUARIO","CONTRASEÑA","ROL"]
            usuarios_csv.writerow(header)

   
#############################################################################  
###################################FUNCION ELIMINAR USUARIO #################
#############################################################################


def eliminar_usuario(usuario_actual): 
    usuarios = []
    clave = []
    rol = []
    clave_administrador = usuario_actual[1]  # Reemplaza con la clave del administrador UNICAMENTE PUEDE INGRESAR A LA FUNCION EL ADMINISTRADOR

    try:
        with open("usuarios.csv", "r", encoding="utf-8") as arch:
            agregar_csv = csv.reader(arch)

            for fila in agregar_csv:                    #se pone cada columna del archivo en una lista distinta
                usuarios.append(fila[0])
                clave.append(fila[1])
                rol.append(fila[2])

            usuarioAEliminar = input('Ingrese usuario a eliminar: ')
            claveAdmin = input('Ingrese la clave del administrador: ')      #debe ser igual a la que esta en este momento en clave_administrador

            while usuarioAEliminar not in usuarios or usuarioAEliminar == usuario_actual[0]:    #SI EL USUARIO NO ESTA EN LA LISTA USUARIOS NO LO ELIMINA YA QUE NO EXISTE
                usuarioAEliminar = input('ERROR AL ELIMINAR, Ingrese usuario a eliminar: ')
                claveAdmin = input('Ingrese la clave del administrador: ')

            if claveAdmin == clave_administrador:  # Verifica la clave del administrador
                usuario_encontrado = False                  
                nuevo_usuario = []
                nueva_clave = []
                nuevo_rol = []

                for i in range(len(usuarios)):
                    if usuarios[i] == usuarioAEliminar:
                        usuario_encontrado = True
                    else:
                        nuevo_usuario.append(usuarios[i])               ## lo que hace esto es agregar todos los usuario excepto el que quiere eliminar
                        nueva_clave.append(clave[i])
                        nuevo_rol.append(rol[i])

                if usuario_encontrado:
                    with open("usuarios.csv", "w", newline="", encoding="utf-8") as arch:
                        editar_csv = csv.writer(arch)

                        for i in range(len(nuevo_usuario)):                                     #agrega uno por uno los usuario que no quiere eliminar excepto el que si
                            editar_csv.writerow([nuevo_usuario[i], nueva_clave[i], nuevo_rol[i]])   

                    print('El usuario', usuarioAEliminar, 'se eliminó correctamente!!!')
                else:
                    print('El usuario no fue encontrado en la lista.')              

            else:                   ### SI LA CLAVE QUE INGRESA EL ADMIN NO ES LA CORRECTA SALE DE LA ACCION PARA QUE LA PERSONA QUE INGRESO COMO ADMIN NO PUEDA ELIMINAR A NADIE
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print('La clave del administrador es incorrecta. No se eliminó ningún usuario, volviendo al menu principal...')
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

            gestion_usuario_Submenu(usuario_actual)

    except FileNotFoundError:                                               #si el archivo no existe, lo crea
        with open('usuarios.csv', "w", newline="", encoding="utf-8") as usuarios_file:
            usuarios_csv = csv.writer(usuarios_file)
            header = ["USUARIO","CONTRASEÑA","ROL"]
            usuarios_csv.writerow(header)
            
            gestion_usuario_Submenu(usuario_actual)

         
######################################################################################
############################FUNCION VERIFICAR CLAVE ##################################
######################################################################################


def verificar_clave_usuario(clave):
    # Verificar la longitud de la clave (al menos 8 caracteres), si es menor directamente returnea false
    if len(clave) < 8:                                  
        print('La clave debe tener al menos 8 caracteres.')
        return False
                            #si la longitud es mayor entra a verificar los demas condiciones
    tiene_mayuscula = False
    tiene_minuscula = False                 #todas las condiciones empiezan en False y van cambiando a medida que se analizan si se cumplen
    tiene_numero = False

                                                                # Verificar caracteres en la clave UNO POR UNO
    for caracter in clave:                      
        if 'A' <= caracter <= 'Z':
            tiene_mayuscula = True
        if 'a' <= caracter <= 'z':
            tiene_minuscula = True
        if '0' <= caracter <= '9':
            tiene_numero = True

    if tiene_mayuscula and tiene_minuscula and tiene_numero:            #SI LA CLAVE CUMPLE TODAS LAS CONDICIONES RETURNEA TRUE, SI FALTA ALGUNA RETURNEA FALSE
        return True
    else:
        print('La clave debe tener al menos una letra mayúscula, una letra minúscula y un número.')
        return False  


#############################################################################
###################################FUNCION AGREGAR USUARIO ##################
############################################################################# 


def agregar_usuario(usuario_actual):
   
    usuariosL = []
    claves = []
    rol = []
    
    try:
        with open("usuarios.csv", "r", encoding="utf-8") as arch:
            agregar_csv = csv.reader(arch)
            for fila in agregar_csv:                    #agrega todas las columnas del archivo en listas distintas
                usuariosL.append(fila[0])
                claves.append(fila[1])
                rol.append(fila[2])

        nombreUsuario = input('Ingrese un nuevo nombre de usuario: ')
        
        while len(nombreUsuario) <= 0:                                  #si el nombre del usuario esta vacio lo pide devuelta
            nombreUsuario = input('Ingrese un nuevo nombre de usuario: ')

        while nombreUsuario in usuariosL:                           #si el nombre del usaurio que queres crear ya esta en el archivo te pide otro nombre ya que ya existe
            nombreUsuario = input('Ya hay un usuario con ese nombre, ingrese un nuevo nombre de usuario: ')

        nuevoUsuario = []  # Inicializa la lista para el nuevo usuario con los 3 parámetros para agregar al archivo
        nuevoUsuario.append(nombreUsuario)


        nuevaClaveUsuario = input('Ingrese la clave del nuevo usuario: ')
        while not verificar_clave_usuario(nuevaClaveUsuario):               #mientras la clave ingresada no cumpla con los requisitos de la clave la pide devuelta
            nuevaClaveUsuario = input('La clave no cumple con los requisitos. Ingrese la clave del nuevo usuario: ')


        claveIncriptada = desencriptar(nuevaClaveUsuario)                       #necesitamos que guarde la clave encriptada, por lo tanto llamamos a la funcion
    
        nuevoUsuario.append(claveIncriptada)

        rolUsuario = input('Ingrese el rol del nuevo usuario: ')
                                                                    #mientras que el rol sea distinto a los permitidos lo pide devuelta
        while len(rolUsuario) <= 0 or (rolUsuario !='administrador' and rolUsuario !='farmaceutico' and rolUsuario != 'vendedor'):
            rolUsuario = input('Ingrese un nuevo rol de usuario: ')
            
        nuevoUsuario.append(rolUsuario)

        print('El usuario',nombreUsuario, 'se creó exitosamente.')

        with open("usuarios.csv", "a", newline="", encoding="utf-8") as arch_escritura:
            escritor = csv.writer(arch_escritura)                                               #agrega el usuario que acaba de crear si es que pone correctamente la info
            escritor.writerow(nuevoUsuario)

        gestion_usuario_Submenu(usuario_actual)
    except FileNotFoundError:                                                        #si el archivo no existe, lo crea
        with open('usuarios.csv', "w", newline="", encoding="utf-8") as usuarios_file:
            usuarios_csv = csv.writer(usuarios_file)
            header = ["USUARIO","CONTRASEÑA","ROL"]
            usuarios_csv.writerow(header)
            


#############################################################################  
###################################FUNCION REALIZAR VENTA ###################
############################################################################# 


def realizarVentaPrincipal(usuario_actual):
    

    ROL = usuario_actual[2]

    def menu_string(texto, opciones):
        dato = input(texto + " (" + str(opciones) + "): ")

        while dato not in opciones:
            dato = input('Ingrese una opción válida (' + str(opciones) + '): ')

        return dato


    def read_csv_file(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = list(reader)        ##  convierte en lista
            lines = lines[1:]           ##saltea encabezado

        if filename == 'stock.csv':     #si el archivo que queremos abrir es el de stock: que almacene su info necesaria
            nombre_producto = []
            cantidad = []
            fecha_caducidad = []
            for row in lines:
                nombre_producto.append(row[0])
                cantidad.append(row[1])
                fecha_caducidad.append(row[2])             
            return nombre_producto, cantidad, fecha_caducidad


        elif filename == 'detalle_producto.csv':    #si el archivo que queremos abrir es el de detalle: que almacene su info necesaria
            nombre_producto = []
            farmaco = []
            proveedor = []
            bajo_receta = []
            precio = []
            for row in lines:
                nombre_producto.append(row[0])
                farmaco.append(row[1])
                proveedor.append(row[2])
                bajo_receta.append(row[3])
                precio.append(row[4])
            return nombre_producto, farmaco, proveedor, bajo_receta, precio


    def write_stock_csv(nombre_producto, cantidad, fecha_caducidad):
        with open('stock.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in range(len(nombre_producto)):
                row = [nombre_producto[i], cantidad[i], fecha_caducidad[i]]
                writer.writerow(row)


    def search_row(match, columna):
        for i in range(len(columna)):
            if columna[i] == match:
                return i


    def search_rows(match, columna):                ###columna ESTO
        idx = []
        for i in range(len(columna)):
            if columna[i] == match:
                idx.append(i)
        return idx


    def OrdenarXFecha(nombre_producto, cantidad, fecha_caducidad):
        n = len(fecha_caducidad)                                #[10/12/2023,12/12/2024,10/10/2023,25/10/2023]
        for i in range(n):                                          
            for j in range(0, n-i-1):                            ###(i+1,len(n))
                fecha1 = fecha_caducidad[j]
                fecha2 = fecha_caducidad[j+1]

                dia1, mes1, anio1 = fecha1[0:2], fecha1[3:5], fecha1[6:]        ##
                dia2, mes2, anio2 = fecha2[0:2], fecha2[3:5], fecha2[6:]        

                dia1, mes1, anio1 = int(dia1), int(mes1), int(anio1)
                dia2, mes2, anio2 = int(dia2), int(mes2), int(anio2)
                                                                        #COMPARAMOS LAS FECHAS PARA OBTENER EL ORDEN
                    
                if (anio1, mes1, dia1) > (anio2, mes2, dia2):   #OTRA FORMA DE HACERLO: if anio1 > anio2 or (anio1 == anio2 and (mes1 > mes2 or (mes1 == mes2 and dia1 > dia2))): POSIBLE ALTERNATIVA
                    fecha_caducidad[j], fecha_caducidad[j+1] = fecha_caducidad[j+1], fecha_caducidad[j]
                    nombre_producto[j], nombre_producto[j+1] = nombre_producto[j+1], nombre_producto[j]
                    cantidad[j], cantidad[j+1] = cantidad[j+1], cantidad[j]


    def update_stock(row):
        NOMBRE = 0
        CANTIDAD = 1            # Constantes para los índices de las columnas en el archivo CSV
        FECHA = 2

        stock = read_csv_file("stock.csv")

        nombre_producto, cantidad, fecha_caducidad = stock              # Desempaquetar las listas en variables separadas

        updated = False                         # updated es  para rastrear si se realizó alguna actualización

        updated_nombre_producto = []
        updated_cantidad = []                        # Listas para almacenar los valores actualizados
        updated_fecha_caducidad = []

        for i in range(len(nombre_producto)):       # Iterar a través de las filas del archivo CSV
            if nombre_producto[i] == row[NOMBRE] and fecha_caducidad[i] == row[FECHA]:
                if row[CANTIDAD] != 0:                                  # Si la cantidad no es cero, actualizar la cantidad
                    new_quantity = int(cantidad[i]) - int(row[CANTIDAD])
                    if new_quantity > 0:                                # Si la cantidad actualizada es mayor que 0, almacenar los valores actualizados                                     
                        updated_nombre_producto.append(nombre_producto[i])
                        updated_cantidad.append(str(new_quantity))
                        updated_fecha_caducidad.append(fecha_caducidad[i])
                    updated = True
            
            else:                                                    # Si la fila no cumple con los criterios de actualización, almacenar los valores existentes
                updated_nombre_producto.append(nombre_producto[i])
                updated_cantidad.append(cantidad[i])
                updated_fecha_caducidad.append(fecha_caducidad[i])

        if updated:                                             # Si se realiza alguna actualización, escribir los valores actualizados de nuevo en el archivo CSV
            with open("stock.csv", "w") as file:
                file.write("NOMBRE_PRODUCTO,CANTIDAD,FECHA_CADUCIDAD\n")
                for i in range(len(updated_nombre_producto)):
                    file.write(updated_nombre_producto[i] + "," + str(updated_cantidad[i]) + "," + updated_fecha_caducidad[i] + "\n")


    def realizar_venta(fecha_hoy, nro_factura):
        ROL = usuario_actual[2]
        CANTIDAD = 1
        FARMACO = 1
        NOMBRE = 0  
        PRECIO = 4

        nombre = input("Nombre del medicamento: ")
        
        while len(nombre)<=0:
            nombre = input("Ingrese nuevamente, Nombre del medicamento: ")
        
        cantidad = None  # Otra opción sería inicializarlo con cualquier valor que no sea un número entero positivo

        while cantidad is None or cantidad <= 0:
            cantidad_input = input("Cantidad: ")

            try:
                cantidad = int(cantidad_input)
                if cantidad <= 0:
                    print("Por favor, ingrese un número entero positivo.")
            except ValueError:
                print("Error: Ingrese un número entero válido.")
            


        nombre_producto_detalle, farmaco, _, bajo_receta, precio = read_csv_file('detalle_producto.csv')
        nombre_producto_stock, cantidad_stock, fecha_caducidad = read_csv_file("stock.csv")

        detalle_idx = search_row(nombre, nombre_producto_detalle)
        if detalle_idx is None:
            print(f'{nombre} not found')                #si no se logra la venta devuelve listas vacias
            return [], [], [], []

        if bajo_receta[detalle_idx] == "SI" and ROL != "farmaceutico":
            print("NO PUEDES VENDER ESTE MEDICAMENTO SIN RECETA")            #si no se logra la venta devuelve listas vacias
            return [], [], [], []

        OrdenarXFecha(nombre_producto_stock, cantidad_stock, fecha_caducidad) 
        partidas_idx = search_rows(nombre, nombre_producto_stock)
        if not partidas_idx:
            print(nombre,'está fuera de stock')                              #si no se logra la venta devuelve listas vacias
            return [], [], [], []

        partidas_farmaco_idx = partidas_idx
        detalles_farmaco = search_rows(farmaco[detalle_idx], farmaco)
        
        for detalle in detalles_farmaco:
            partidas_idx = search_rows(nombre_producto_detalle[detalle], nombre_producto_stock)
            for partida in partidas_idx:
                if nombre_producto_stock[partida] != nombre:
                    partidas_farmaco_idx.append(partida) 

        total = 0
        for partida in partidas_farmaco_idx:
            total += int(cantidad_stock[partida])

        if total < cantidad:
            print("No hay suficiente stock disponible.")             #si no se logra la venta devuelve listas vacias
            return [], [], [], []


        print("Venta exitosa: ")
        factura_idx = []
        factura_precio = []
        factura_cantidad = []
        factura_farmaco = []
        conseguidas = 0
        i = 0
        size = len(partidas_farmaco_idx)

        while conseguidas < cantidad and i < size:
            current = int(cantidad_stock[partidas_farmaco_idx[i]])

            if current > cantidad - conseguidas:
                current = cantidad - conseguidas

            conseguidas += current

            print("Producto: " + nombre_producto_stock[partidas_farmaco_idx[i]] + ", Cantidad: " + str(current))
            cantidad_stock[partidas_farmaco_idx[i]] = str(int(cantidad_stock[partidas_farmaco_idx[i]]) - current)
            row = [nombre_producto_stock[partidas_farmaco_idx[i]], current, fecha_caducidad[partidas_farmaco_idx[i]]]
            update_stock(row)

            factura_idx.append(nombre_producto_stock[partidas_farmaco_idx[i]])
            detalle_i = search_row(nombre_producto_stock[partidas_farmaco_idx[i]], nombre_producto_detalle)
            factura_precio.append(precio[detalle_i])
            factura_cantidad.append(current)
            factura_farmaco.append(farmaco[detalle_i])

            i += 1
            
        if conseguidas > 0:
            with open('ventas.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for i in range(len(factura_idx)):
                    fecha_caducidad_value = ""
                    if i < len(partidas_farmaco_idx):
                        fecha_caducidad_value = fecha_caducidad[partidas_farmaco_idx[i]]
                    writer.writerow([fecha_hoy, factura_idx[i], factura_cantidad[i], fecha_caducidad_value, nro_factura])

        return factura_idx, factura_cantidad, factura_precio, factura_farmaco

    def get_last_invoice_number():          #ESTA FUNCION ANALIZA EL ULTIMO NUMERO DE FACTURA QUE ESTA EN ELA RCHIVO VENTAS PARA PODER SABER CUAL PONER DESPUES
        try:
            with open('ventas.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                lines = list(reader)                    #convierte todo en lista (visto en clase list())
                if len(lines) > 1:
                    last_invoice = 0
                    for row in lines[1:]:               ##SALTEA EL ENCABEZADO (HAY VARIAS FORMAS)
                        
                            invoice_number = int(row[-1])
                            if invoice_number > last_invoice:
                                last_invoice = invoice_number
                       
                    return last_invoice + 1
                else:
                    return 1
        except (FileNotFoundError, IndexError):
            return 1


    def write_to_txt(nombre, cantidad, precio, farmaco, nro_factura, fecha_hoy):
        nombre_archivo = 'factura-' + str(nro_factura - 1) + '.txt'

        unique_products = []
        total_amount = 0

        with open(nombre_archivo, 'a') as f:
            f.write("Fecha: " + str(fecha_hoy) + "\n")
            f.write("Numero de Factura: " + str(nro_factura - 1) + "\n")
            f.write("===================================\n")
            f.write("Farmaco\t\tProduct\t\tCantidad\tPrecio Unitario\tTotal\n")
            f.write("-----------------------------------\n")

            for i in range(len(nombre)):
                key = (farmaco[i], nombre[i], precio[i])

                found = False
                for item in unique_products:
                    if item[0] == key:
                        item[1] += cantidad[i]
                        item[2] += float(precio[i]) * float(cantidad[i])
                        found = True

                if not found:
                    unique_products.append([key, cantidad[i], float(precio[i]) * float(cantidad[i])])

                total_amount += float(precio[i]) * float(cantidad[i])

            for item in unique_products:
                key, cantidad, total = item
                farmaco, nombre, precio = key
                f.write(farmaco + "\t\t" + nombre + "\t\t" + str(cantidad) + "\t\t" + str(precio) + "\t\t" + str(total) + "\n")

            f.write("===================================\n")
            f.write("IMPORTE: " + str(total_amount) + "\n")
            
            
    nro_factura = get_last_invoice_number()
    continuar = True
    fecha_hoy = input("Ingrese la fecha de hoy (dd/mm/yyyy): ")
    while verificar_Fecha(fecha_hoy) == False:
        fecha_hoy = input("Ingrese la fecha de hoy (dd/mm/yyyy): ")
        
    factura_nombre_total = []
    factura_cantidad_total = []
    factura_precio_total = []
    factura_farmaco_total = []

    while continuar:
        factura_nombre, factura_cantidad, factura_precio, factura_farmaco = realizar_venta(fecha_hoy, nro_factura)

        if factura_nombre:
            print(factura_nombre, factura_cantidad, factura_precio, factura_farmaco)
            factura_nombre_total += factura_nombre
            factura_cantidad_total += factura_cantidad
            factura_precio_total += factura_precio
            factura_farmaco_total += factura_farmaco
        else:
            print("No hay suficiente stock disponible.")

        opcion = menu_string("¿Quieres realizar otra venta en esta factura? (SI/NO)", ["SI", "NO"])

        if opcion == "NO":
            continuar = False
            nro_factura = get_last_invoice_number()
            write_to_txt(factura_nombre_total, factura_cantidad_total, factura_precio_total, factura_farmaco_total, nro_factura, fecha_hoy)
            
        

        #realizar_venta(fecha_hoy,nro_factura)
    gestionInventario(usuario_actual)  
        
#############################################################################  
###################################FUNCION SEGUIMIENTO DE CADUCIDAD #########
#############################################################################    
    
 
def seguimiento_caducidad(usuario_actual):
    def calcular_fecha_final(dia, mes, año, dias):      # ejemplo 25/03/2023  #200  #a dia_final se le suma el dia de la fecha de inicio + la cantidad de dias ingresada despues
        dia_final = dia + dias                          #dia=01,mes=02,anio=2023    dias= 100        100-30 = 70
        mes_final = mes                                 #100   01/02/2023
        año_final = año
                                                #ponemos 30 porque es el numero de dias promedio de los meses
        while dia_final > 30:                   #si el numero en dia es mayor a 30 se le resta 30 dias y agrega 1 mes mas  y asi hasta que dias sea menor a 30, es decir sea un mes
            dia_final -= 30                     #por ejemplo si llega 27 ya no sigue entrando al while ni agregando meses
            mes_final += 1
                                                        #          01/02/2023
        while mes_final > 12:               #lo mismo que antes pero ahora con anio y mes, muy probablemente la cantidad de meses sea > 12 dependiendo de la cantidad de dias que pongamos
            mes_final -= 12                             #         por ej quedaria 27/11/2023
            año_final += 1

        return dia_final, mes_final, año_final              # devuelve el dia calculado de la fecha creada final, junto al mes y al anio

    def obtener_fecha_caducidad(stock_data):
        fecha_caducidad = ""
        en_comillas = False
        i = 0                                               

        while i < len(stock_data):
            char = stock_data[i]

            if char == '"':
                en_comillas = not en_comillas
            elif char == ',' and not en_comillas:
                i = len(stock_data)
            else:
                fecha_caducidad += char

            i += 1

        return fecha_caducidad

    def obtener_detalle_producto(detalle_data):
        detalle = []
        item_actual = ""
        comillas = False

        for char in detalle_data:
            if char == ',' and not comillas:
                detalle.append(item_actual)
                item_actual = ""
            elif char == '"':
                comillas = not comillas
            else:
                item_actual += char

        if item_actual:
            detalle.append(item_actual)

        return detalle

    def obtener_nombre_producto(stock_data):
        nombre_producto = ""
        comillas = False
        i = 0

        while i < len(stock_data):
            char = stock_data[i]

            if char == '"':
                comillas = not comillas
            elif char == ',' and not comillas:
                return
            else:
                nombre_producto += char

            i += 1

        return nombre_producto

    def comparar_fechas(fecha1, fecha2):
        dia1, mes1, año1 = dividir_fecha(fecha1)            #por ej 01/12/2023     #01/12/2024
        dia2, mes2, año2 = dividir_fecha(fecha2)            #por ej 25/11/2023     #25/11/2023

        if año1 < año2:
            return -1
        elif año1 > año2:
            return 1                                            #0 1 -1 = 0 ASPIRINA ENTRA?
        elif mes1 < mes2:                                       #1 1 -1 = 1
            return -1
        elif mes1 > mes2:                                       #depende lo que devuelva el producto esta o no vencido entre las fechas que pusimos
            return 1
        elif dia1 < dia2:
            return -1
        elif dia1 > dia2:
            return 1
        else:
            return 0

    def dividir_fecha(fecha):       #01/02/2023
        dia, mes, año = 0, 0, 0
        componente_actual = ""      #
        contador_componente = 0                     #divide la fecha en dias,meses y anios

        for char in fecha:
            if char == '/':
                if contador_componente == 0:
                    dia = int(componente_actual)
                elif contador_componente == 1:
                    mes = int(componente_actual)
                componente_actual = ""
                contador_componente += 1
            else:
                componente_actual += char

        if contador_componente == 2:
            año = int(componente_actual)

        return dia, mes, año

    def encontrar_id_producto(detalle_lines, nombre_producto):
        for i in range(len(detalle_lines)):
            line = detalle_lines[i]
            if nombre_producto in line:
                return i
        return None

    def consultar_productos_a_vencer():
        
        detalle_columna1 = []                   #agrega cada info de columna de cada archivo a su lista correspondiente
        detalle_columna2 = []                   #agrega cada info de columna de cada archivo a su lista correspondiente
        detalle_columna3 = []                   #agrega cada info de columna de cada archivo a su lista correspondiente

        stock_columna1 = []                     #agrega cada info de columna de cada archivo a su lista correspondiente
        stock_columna2 = []                     #agrega cada info de columna de cada archivo a su lista correspondiente
        stock_columna3 = []                     #agrega cada info de columna de cada archivo a su lista correspondiente
       
        with open("detalle_producto.csv", "r", encoding="utf-8") as detalle_file:
            detalle_reader = csv.reader(detalle_file)
            for row in detalle_reader:
                detalle_columna1.append(row[0])
                detalle_columna2.append(row[1])
                detalle_columna3.append(row[2])

        with open("stock.csv", "r", encoding="utf-8") as stock_file:
            stock_reader = csv.reader(stock_file)
            for row in stock_reader:
                stock_columna1.append(row[0])
                stock_columna2.append(row[1])
                stock_columna3.append(row[2])

        print("Seleccione el tipo de consulta:")
        print("1. Entre una fecha y una cantidad de días a partir de esa fecha")
        print("2. Entre dos fechas")
        opcion = input("Elija una opción (1 o 2): ")
        
        while opcion !='1' and opcion !='2':
            opcion = input("ERROR, Elija una opción (1 o 2): ")

        if opcion == "1":
            fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/aaaa): ")
            while verificar_Fecha(fecha_inicio) ==False:                                #verifiva que lafecha que ponga el usuarios cumpla con los requisitos
                fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/aaaa): ")
                
            dias = None  # Otra opción sería inicializarlo con cualquier valor que no sea un número entero positivo

            while dias is None or dias <= 0:
                dias_input = input("Ingrese la cantidad de días a partir de la fecha de inicio: ")

                try:
                    dias = int(dias_input)
                    if dias <= 0:
                        print("Por favor, ingrese un número entero positivo.")
                except ValueError:
                    print("Error: Ingrese un número válido.")    
                
            #dias = int(input("Ingrese la cantidad de días a partir de la fecha de inicio: "))
            
            #while dias < 0:
            #    dias = int(input("ERROR, Ingrese la cantidad de días a partir de la fecha de inicio: "))

            dia, mes, año = dividir_fecha(fecha_inicio)                 
            dia_final, mes_final, año_final = calcular_fecha_final(dia, mes, año, dias)
            fecha_final = str(dia_final) + '/' + str(mes_final) + '/' + str(año_final)      #convierte en fecha final

        elif opcion == "2":
            fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/aaaa): ")
            
            while verificar_Fecha(fecha_inicio) ==False:                            #verifiva que lafecha que ponga el usuarios cumpla con los requisitos
                fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/aaaa): ")

            
            fecha_final = input("Ingrese la fecha final (dd/mm/aaaa): ")
            
            while verificar_Fecha(fecha_final) ==False:                                 #verifiva que lafecha que ponga el usuarios cumpla con los requisitos
                fecha_final = input("ERROR, Ingrese la fecha de inicio (dd/mm/aaaa): ")

        productos_a_vencer = []

        for i in range(len(stock_columna1)):
            fecha_caducidad = stock_columna3[i]

            if comparar_fechas(fecha_inicio, fecha_caducidad) <= 0 <= comparar_fechas(fecha_final, fecha_caducidad):
                nombre_producto = stock_columna1[i]
                id_producto = encontrar_id_producto(detalle_columna1, nombre_producto)
                if id_producto is not None:
                    detalle_data = (detalle_columna1[id_producto], detalle_columna2[id_producto], detalle_columna3[id_producto])
                    nombre_producto = detalle_data[0]
                    proveedor = detalle_data[2]

                    productos_a_vencer.append([nombre_producto, proveedor, fecha_caducidad])

        productos_por_pagina = 20
        pagina_actual = 0

        while pagina_actual < len(productos_a_vencer):                      #si en pantalla hay mas de 20 productos, presionando enter pasa a otra pagina
            print("\nNombre del producto\tProveedor\tFecha de caducidad")
            i = pagina_actual
            while i < pagina_actual + productos_por_pagina and i < len(productos_a_vencer):  # Verifica manualmente el final de la lista
                producto = productos_a_vencer[i]
                print(producto[0],'\t''\t',producto[1],'\t''\t',producto[2])
                i += 1

            if i < len(productos_a_vencer):
                input("Presione ENTER para avanzar a la siguiente página")

            pagina_actual += productos_por_pagina
    consultar_productos_a_vencer()
    gestionInventario(usuario_actual)


#############################################################################  
###################################FUNCION CAMBIAR CLAVE ####################
#############################################################################  


def cambiarClave_usuario(usuarioActual):
    usuarios = []
    claves = []
    rol = []
    try:
        with open("usuarios.csv", "r", encoding="utf-8") as arch:
            agregar_csv = csv.reader(arch)

            for fila in agregar_csv:                #almacena cada columna en una lista distinta
                usuarios.append(fila[0])
                claves.append(fila[1])
                rol.append(fila[2])
                
          
            for i in range(len(usuarios)):
                if usuarios[i] == usuarioActual[0]:                 #solo puede cambiarse la clave a si mismo, (el usuario que esta ahora)
                    claveInput = input('Ingrese nueva clave: ')
                    while not verificar_clave_usuario(claveInput):              #tiene que verificar que este poniendo SU CLAVE
                        claveInput = input('La clave no cumple con los requisitos. Ingrese una nueva clave: ')
                        
                    claveCambiada = desencriptar(claveInput)                #la incripta (con la otra funcion), nos sirve para pensar mejor lo que hace (la funcion encriptar y desencriptar son iguales)
                    claves[i] =claveCambiada
                    print('CLAVE CAMBIADA CON EXITO!!!')
                                  
    except FileNotFoundError:
        with open('usuarios.csv', "w", newline="", encoding="utf-8") as usuarios_file:
            usuarios_csv = csv.writer(usuarios_file)
            header = ["USUARIO","CONTRASEÑA","ROL"]
            usuarios_csv.writerow(header)
        
    with open("usuarios.csv", "w", newline="", encoding="utf-8") as arch:
        editar_csv = csv.writer(arch)

        for i in range(len(usuarios)):
            editar_csv.writerow([usuarios[i], claves[i], rol[i]])
            
    gestion_usuario_Submenu(usuarioActual)
            

############################################################################## 
########################FUNCION AGREGAR STOCK ################################
##############################################################################


def AgregarStock(usuario_actual):
# Definir las listas para almacenar datos
    NombreProductosStock = []
    CantidadStockInteger = []
    CaducidadStock = []
    
    NombreProductoDetalle = []

                                        # Variable para rastrear si se ha leído la primera fila
    header_read = False

                                        # Ruta del archivo stock.csv
    archivo_stock = "stock.csv"
    archivo_detalle = "detalle_producto.csv"
    
                            # Leer el archivo stock.csv y cargar los datos en las listas
    try:
        
        with open(archivo_detalle,"r",encoding="utf-8",newline="") as detalle_file:
            detalle_csv = csv.reader(detalle_file)
        
            for fila in detalle_csv:
                NombreProductoDetalle.append(fila[0])
            

        with open(archivo_stock, "r", encoding="utf-8", newline="") as stock_file:
            stock_csv = csv.reader(stock_file)

            for row in stock_csv:
                if not header_read:
                    header = row  # Almacenar la primera fila (encabezados)
                    header_read = True
                else:
                    NombreProductosStock.append(row[0])
                    cantidad = row[1]
                    try:
                        cantidad_entero = int(cantidad)  # Intentar convertir a entero
                        CantidadStockInteger.append(cantidad_entero)
                    except ValueError:      #SI PONE UN VALOR QUE TIRA ESTE RROR QE LO AGREGUE COMO 0, except se puede usar para cualquiero error, estuvimos investigando y tiene sentido poder usarlo para value error(que vimos en clase tambien)
                        CantidadStockInteger.append(0)  # Si no se puede convertir, usar 0
                    CaducidadStock.append(row[2])

    except FileNotFoundError:
    # Si el archivo stock.csv no existe, crearlo con encabezados
        with open(archivo_stock, "w", newline="", encoding="utf-8") as stock_file:
            stock_csv = csv.writer(stock_file)
            header = ["NOMBRE_PRODUCTOS", "CANTIDAD", "FECHA_CADUCIDAD"]
            stock_csv.writerow(header)


    productoIngresado = input('Ingrese un producto: ')
    while len(productoIngresado) <= 0:                      #si la ifnfo ingresada esta vacia que la pida devuelta
        productoIngresado = input('No puede estar en blanco Ingrese un producto: ')
    
    cantidadIngresado = None  # Otra opción sería inicializarlo con cualquier valor que no sea un número entero positivo

    while cantidadIngresado is None or cantidadIngresado <= 0:
        cantidadIngresado_input = input("Ingrese la cantidad:: ")

        try:
            cantidadIngresado = int(cantidadIngresado_input)
            if cantidadIngresado <= 0:
                print("Por favor, ingrese un número entero positivo.")
        except ValueError:
            print("Error: Ingrese una cantidad válida.") 


    fecha_caducidadIngresado = input('Ingrese la fecha de caducidad en el siguiente formato: dd/mm/aaaa: ')

    if productoIngresado not in NombreProductoDetalle:
                                                         # El producto no se encuentra en stock.csv, solicitar detalles al usuario
        farmacoIngresado = input('Ingresar FARMACO: ')
        
        while len(farmacoIngresado)<=0:                 #si la info ingresada esta vacia que la pida devuelta
            farmacoIngresado = input('Ingresar FARMACO: ')
            
        proveedorIngresado = input('Ingresar PROVEEDOR: ')
        
        while len(proveedorIngresado)<=0:                               #si la ifnfo ingresada esta vacia que la pida devuelta
            proveedorIngresado = input('Ingresar PROVEEDOR: ')
            
        recetaIngresado = input('¿Es bajo receta? (SI o NO): ')
        
        while len(recetaIngresado)<=0 or (recetaIngresado != 'NO' and recetaIngresado !='SI'):      #si la info ingresada esta vacia que la pida devuelta y es distinta a SI O NO la pide devuelta (salteamos la posibilidad de que no poner nada sea igual que NO porque no es eficiente a la hora de analizar el archivo)
           recetaIngresado = input('error, ¿Es bajo receta? (SI o NO): ')



        precioIngresado = None  # Otra opción sería inicializarlo con cualquier valor que no sea un número entero positivo

        while precioIngresado is None or precioIngresado <= 0:
            precioIngresado_input = input('Ingresar PRECIO: ')

            try:
                precioIngresado = float(precioIngresado_input)
                if precioIngresado <= 0:
                    print("Por favor, ingrese un número positivo.")
            except ValueError:
                print("Error: Ingrese un precio válido.") 


        try:
            with open("detalle_producto.csv", "a", newline="", encoding="utf-8") as detalle_file:
                detalle_csv = csv.writer(detalle_file)
                detalle_csv.writerow([productoIngresado, farmacoIngresado, proveedorIngresado, recetaIngresado, precioIngresado])
        except FileNotFoundError:
            print('Error escribiendo en detalle_productos.csv')

            # Agregar los detalles a las listas (para stock.csv)
        NombreProductosStock.append(productoIngresado)
        try:
            cantidad_entero = int(cantidadIngresado)  # Intentar convertir a entero
            CantidadStockInteger.append(cantidad_entero)
        except ValueError:
            CantidadStockInteger.append(0)  # Si no se puede convertir, usar 0
            
        fechaMal = True    
        while fechaMal:                                 #si la fecha esta mal la pide devuelta (llama a la funcion verificar fecha)
                    
            if verificar_Fecha(fecha_caducidadIngresado):
                    fechaMal = False
            else:
                print('Fecha no válida. Inténtelo de nuevo.')
                fecha_caducidadIngresado = input('Ingrese una fecha de caducidad en el siguiente formato: dd/mm/aaaa: ')
                
                    
            if fechaMal == False:  
                CaducidadStock.append(fecha_caducidadIngresado)
        
    else:
            # El producto ya existe en stock.csv, actualizar cantidad si la fecha coincide
        found = False
        for i in range(len(NombreProductosStock)):
            if productoIngresado == NombreProductosStock[i] and fecha_caducidadIngresado == CaducidadStock[i]:
                    try:
                        cantidad_entero = int(cantidadIngresado)  # Intentar convertir a entero
                        CantidadStockInteger[i] += cantidad_entero
                    except ValueError:                       #except se usa para cualquier error, iinvestigamos y tiene todo el sentido del mundo poder usar otros errores para reemplazarlos
                        print('No se modifica la cantidad')
                    found = True

        if not found:
                                                            # El producto existe en stock.csv pero con diferente fecha, agregar como nueva partida
                NombreProductosStock.append(productoIngresado)
                try:
                    cantidad_entero = int(cantidadIngresado)  # Intentar convertir a entero
                    CantidadStockInteger.append(cantidad_entero)
                except ValueError:               #except se usa para cualquier error, iinvestigamos y tiene todo el sentido del mundo poder usar otros errores para reemplazarlos
                    CantidadStockInteger.append(0)  # Si no se puede convertir, usar 0
                    
                fechaMal = True    
                while fechaMal:
                    
                    if verificar_Fecha(fecha_caducidadIngresado):
                        fechaMal = False
                    else:
                        print('Fecha no válida. Inténtelo de nuevo.')
                        fecha_caducidadIngresado = input('Ingrese una fecha en el siguiente formato: dd/mm/aaaa: ')
                    
                if fechaMal == False:  
                    CaducidadStock.append(fecha_caducidadIngresado)
                    
                
        # Actualizar el archivo stock.csv
    try:
            with open(archivo_stock, "w", newline="", encoding="utf-8") as stock_file:
                stock_csv = csv.writer(stock_file)
                stock_csv.writerow(header)  # Escribir la fila de encabezados nuevamente

                for i in range(len(NombreProductosStock)):
                    stock_csv.writerow([NombreProductosStock[i], CantidadStockInteger[i], CaducidadStock[i]])

    except FileNotFoundError:                           
            print('No se pudo relizar la accion')
                
    gestionInventario(usuario_actual)


################################################################################ 
########################SUB MENU GESTION DE INVENTARIO #########################
################################################################################  


def gestionInventario(usuario_actual):
    print('*** GESTION DE INVENTARIO***')
    print('a. Ingresar nuevo stock')
    print('b. Realizar venta')
    print('c. Seguimiento de caducidad')
    print('d. Volver al menú principal')

    ingresar = input('¿Qué desea hacer en el menú de gestión de inventario? ')
    
    while ingresar !='a' and ingresar !='b' and ingresar !='c' and ingresar !='d':
        ingresar = input('ERROR, ¿Qué desea hacer en el menú de gestión de inventario?: ')

    if ingresar == 'a' :
        AgregarStock(usuario_actual)
        
    elif ingresar == 'b':
        realizarVentaPrincipal(usuario_actual)
    
    elif ingresar == 'c':
        seguimiento_caducidad(usuario_actual)
    
    elif ingresar == 'd':
        menu_principal(usuario_actual)
        
    else:
        print('*********************************************')
        print('***** NO TIENE LOS PERMISOS NECESARIOS ******')
        print('*********************************************')
        gestionInventario(usuario_actual)
        
    
################################################################################  
########################SUB MENU GESTION USUARIOS ##############################
################################################################################


def gestion_usuario_Submenu(usuario_actual):
    #while True:
        print('*** GESTION DE USUARIOS ***')
        print('a. Agregar usuario')
        print('b. Eliminar usuario')
        print('c. Cambiar contraseña')
        print('d. Volver al menú principal')

        ingresar = input('¿Qué desea hacer en el menú de gestión de usuarios? ')
        
        while ingresar !='a' and ingresar !='b' and ingresar !='c' and ingresar !='d':
            ingresar = input('ERROR, ¿Qué desea hacer en el menú de gestión de usuarios? ')

        if ingresar == 'a' and usuario_actual[2] == 'administrador':
            agregar_usuario(usuario_actual)
        
        elif ingresar == 'b' and usuario_actual[2] == 'administrador':
            eliminar_usuario(usuario_actual)

        elif ingresar == 'c':
            cambiarClave_usuario(usuario_actual)
            
        elif ingresar == 'd':
            menu_principal(usuario_actual)
            
        else:
            print('                          !!!!!!             !!!!!!!                   !!!!!!!!!                     ')
            print('!!!!!        USTED NO TIENE LOS PERMISOS NECESARIOS PARA REALIZAR LA ACCION                     !!!!!')
            print('                          !!!!!!             !!!!!!!                   !!!!!!!!!                     ')
            gestion_usuario_Submenu(usuario_actual)


################################################################################################
###################################FUNCION INFORMES RANKING IMPORTE/CANTIDAD ###################
################################################################################################


def InformeRanking(usuario_actual):
    anio = input("Ingrese el año (aaaa): ")
    while len(anio) < 4 or len(anio) > 4:
        anio = input("ERROR, Ingrese el año (aaaa): ")

    campo_orden = input("¿Desea ordenar por 'cantidad' o 'importe' de ventas?: ")       # Solicitar al usuario que elija el campo de orden ('cantidad' o 'importe')

    if campo_orden not in ['cantidad', 'importe']:          # Verificar si el campo de orden es válido
        print("Campo de orden no válido. Debe ser 'cantidad' o 'importe'.")
    else:                           # Inicializar listas para almacenar proveedores, cantidades e importes
        proveedores = []
        cantidades = []
        importes = []

        with open('ventas.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            es_primerlinea = True

            for row in reader:
                if es_primerlinea:
                    es_primerlinea = False
                else:
                    fecha, producto, cantidad, fecha_caducidad, numero_factura = row
                    cantidad = int(cantidad)
                    numero_factura = float(numero_factura)

                    anio_venta = fecha[-4:]          # Extraer el año de la fecha de venta
                                                 # Verificar si la venta pertenece al año ingresado por el usuario
                    if anio_venta == anio:
                        proveedor = None
                                                                                         # Abrir el archivo 'detalle_producto.csv' y leer los detalles del producto
                        with open('detalle_producto.csv', 'r', encoding='utf-8') as product_file:
                            product_reader = csv.reader(product_file)
                            esPrimeraLinea = True
                                                                                # Iterar sobre las filas del archivo de detalles de productos
                            for product_row in product_reader:
                                if esPrimeraLinea:
                                    esPrimeraLinea = False
                                else:                                           # Verificar si el producto coincide con el de la venta actual
                                    if product_row[0] == producto:
                                        proveedor = product_row[2]
                                        precio_unitario = float(product_row[4])

                        if proveedor is not None:                           # Verificar que se haya encontrado un proveedor
                            if proveedor in proveedores:
                                index = proveedores.index(proveedor)
                                cantidades[index] += cantidad
                                importes[index] += cantidad * precio_unitario  # Ajuste aquí
                            else:
                                proveedores.append(proveedor)
                                cantidades.append(cantidad)
                                importes.append(cantidad * precio_unitario)

        if not proveedores:                                              # Verificar si se encontraron ventas para el año ingresado
            print("NO SE ENCONTRARON VENTAS PARA EL", anio,"ASEGURESE DE HABERLO ESCRITO BIEN O QUE HAYA VENTAS EN ESE AÑO")
        else:                                                           # Ordenar las listas según el campo especificado por el usuario
            if campo_orden == 'cantidad':
                for i in range(len(cantidades)):
                    for j in range(i + 1, len(cantidades)):
                        if cantidades[i] < cantidades[j]:
                            proveedores[i], proveedores[j] = proveedores[j], proveedores[i]
                            cantidades[i], cantidades[j] = cantidades[j], cantidades[i]
                            importes[i], importes[j] = importes[j], importes[i]
            else:
                for i in range(len(importes)):
                    for j in range(i + 1, len(importes)):
                        if importes[i] < importes[j]:
                            proveedores[i], proveedores[j] = proveedores[j], proveedores[i]
                            cantidades[i], cantidades[j] = cantidades[j], cantidades[i]
                            importes[i], importes[j] = importes[j], importes[i]

            nombre_archivo = "ranking" + campo_orden + "Vtas_" + anio + ".txt"              # Crear un nombre de archivo para el informe

            with open(nombre_archivo, 'w') as output_file:                                   # Crear y escribir el informe en el archivo
                output_file.write("Ranking de Ventas Año\t " + anio + "\nProveedor Cantidad Importe\n" + '-' * 32 + "\n")

                for i in range(len(proveedores)):
                    proveedor = proveedores[i]
                    cantidad = cantidades[i]
                    importe = importes[i]
                    output_file.write(proveedor + " " + str(cantidad) + " " + str(importe) + "\n")

            print("Archivo", nombre_archivo, "generado con éxito.")
                
        informes_submenu(usuario_actual)
        
    
###################################################################################################################
###################################FUNCION INFORMES PROMEDIO ENTRE FECHA DE VENTA Y VENCIMIENTO ###################
###################################################################################################################


def promedioFechaYVencimiento(usuario_actual):
        try:
            fechas_caducidad = []
            fechas_compra = []
        
 
            with open('ventas.csv', 'r', encoding='utf-8') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)

                esPrimeraLinea = True
                for fila in lector_csv:
                    if esPrimeraLinea:
                        esPrimeraLinea = False
                    else:
                                            # Verifica que la fila contenga al menos 4 elementos (columnas).
                        if len(fila) >= 4:
                                            # Extrae las fechas de caducidad y compra como cadenas de texto.
                            fecha_caducidad = fila[3]
                            fecha_compra = fila[0]

                        # Agrega las fechas a las listas correspondientes.
                            fechas_caducidad.append(fecha_caducidad)
                            fechas_compra.append(fecha_compra)

                                # Inicializa variables para llevar un registro del total de días y el contador de registros.
            total_dias = 0
            contador_registros = 0

                                                        # Itera sobre las fechas y calculamos la diferencia en días 
            for i in range(len(fechas_caducidad)):
                fecha_caducidad = fechas_caducidad[i]
                fecha_compra = fechas_compra[i]

                                                # Verificam nuevamente que las fechas tengan el formato esperado.
                if len(fecha_caducidad) == 10 and len(fecha_compra) == 10:
                                                            # Extraemos el día, mes y año de las fechas.
                    dia_caducidad = int(fecha_caducidad[:2])
                    mes_caducidad = int(fecha_caducidad[3:5])
                    anio_caducidad = int(fecha_caducidad[6:10])

                    dia_compra = int(fecha_compra[:2])
                    month_compra = int(fecha_compra[3:5])
                    anio_compra = int(fecha_compra[6:10])

                                                        # Calcula la diferencia en días entre la fecha de caducidad y la fecha de compra.
                    diferencia_dias = 0

                    if anio_caducidad == anio_compra:
                        if mes_caducidad == month_compra:
                            diferencia_dias = dia_caducidad - dia_compra
                        elif mes_caducidad > month_compra:
                            diferencia_dias = (mes_caducidad - month_compra) * 30 + (dia_caducidad - dia_compra)
                    elif anio_caducidad > anio_compra:
                        diferencia_dias = (anio_caducidad - anio_compra) * 365 + (mes_caducidad - month_compra) * 30 + (dia_caducidad - dia_compra)

                                                        #    Acumula la diferencia en días y aumenta el contador de registros.
                    total_dias += diferencia_dias
                    contador_registros += 1

                                            # se calcula el promedio de la cantidad de días de diferencia.
            if contador_registros > 0:
                promedio_dias = total_dias / contador_registros
                print("El promedio de la cantidad de días de diferencia es: ", promedio_dias, "días")
            else:
                print("No se encontraron registros en el archivo CSV o el formato de las fechas no es el esperado.")
          
        except FileNotFoundError:
            print('error, no se encontro el archivo') 
                  
        informes_submenu(usuario_actual)   
        


###################################################################################################################
###################################FUNCION INFORMES PRODUCTOS VENCIDOS ############################################
###################################################################################################################


def informeProductosVencidos(usuario_actual):
    
    # Ruta de los archivos CSV
    archivo_stock = "stock.csv"
    archivo_detalle = "detalle_producto.csv"

                                    # Función para verificar la fecha en formato dd/mm/yyyy
    def verificar_fecha(fecha):                     
        dia, mes, anio = "", "", ""
        contadorBarra = 0

        for char in fecha:
            if char == '/':
                contadorBarra += 1
            else:
                if contadorBarra == 0:
                    dia += char
                elif contadorBarra == 1:
                    mes += char
                elif contadorBarra == 2:
                    anio += char

        if len(dia) > 0 and len(mes) > 0 and len(anio) > 0:
            return int(dia), int(mes), int(anio)
        return None

                                                       
    fecha_actual = input("Ingrese la fecha actual (dd/mm/yyyy): ")

                                                                    # Validar que la fecha tenga el formato correcto
    fecha_actual_parts = verificar_fecha(fecha_actual)

    while not fecha_actual_parts:
        print("Formato de fecha incorrecto. Utilice dd/mm/yyyy")
        fecha_actual = input("Ingrese la fecha actual (dd/mm/yyyy): ")
        fecha_actual_parts = verificar_fecha(fecha_actual)

    dia_actual, mes_actual, anio_actual = fecha_actual_parts

    # Inicializar variables para el reporte
    total_stock_perdido = 0
    farmacos_cantidad_perdida = []  # Lista para almacenar cantidad perdida por fármaco
    importe_max_perdido = 0
    producto_max_importe_perdido = ""

    # Almacenar la primera fila (encabezados) del archivo stock.csv
    with open(archivo_stock, 'r', encoding="utf-8", newline="") as stock_file:
        stock_csv = csv.reader(stock_file)

                                # Utilizar una bandera para determinar si estamos en la primera fila
        primera_fila = True

                                    # Procesar el resto del archivo
        for row in stock_csv:
                                     # Saltar la primera fila
            if primera_fila:
                primera_fila = False
            else:

                nombre = row[0]
                cantidad = int(row[1])
                fecha_caducidad = row[2]
                fecha_caducidad_parts = verificar_fecha(fecha_caducidad)
                
                if fecha_caducidad_parts:
                    dia_cad, mes_cad, anio_cad = fecha_caducidad_parts          #fecha de caducidad por partes
                    
                    if (anio_cad, mes_cad, dia_cad) < (anio_actual, mes_actual, dia_actual):        #aca esta comparando que fecha es 'mas' que la otra
                        cantidad_perdida = cantidad
                        total_stock_perdido += cantidad_perdida

                                                            # Verificar si el fármaco ya está en la lista
                        encontrado = False
                        for farmaco_info in farmacos_cantidad_perdida:
                            if farmaco_info[0] == nombre:
                                farmaco_info[1] += cantidad_perdida
                                encontrado = True
                        
                                                                # Si el fármaco no está en la lista, agregarlo
                        if not encontrado:
                            farmacos_cantidad_perdida.append([nombre, cantidad_perdida])

                                                                    # Calcular la cantidad e importe total perdido
    importe_max_perdido = 0

    try:
        with open(archivo_detalle, 'r', encoding="utf-8", newline="") as detalle_file:
            detalle_csv = csv.reader(detalle_file)

                                                                                        # Utilizar una bandera para determinar si estamos en la primera fila y asi para poder no tomarla en cuenta
            primera_fila = True

                                                                            # Procesar el resto del archivo
            for row in detalle_csv:
                                                                                    # Saltar la primera fila
                if primera_fila:
                    primera_fila = False
                    
                else:

                    nombre_producto = row[0]
                    farmaco = row[1]
                    precio_str = row[4]

                    if precio_str and precio_str != "NO":
                        try:
                            precio = float(precio_str)
                        except ValueError:
                            precio = 0.0

                                                                            # Encontrar la cantidad perdida del fármaco en la lista
                        for farmaco_info in farmacos_cantidad_perdida:
                            if farmaco_info[0] == nombre_producto:
                                cantidad_perdida = farmaco_info[1]
                                farmaco_info[0] = farmaco

                        importe_perdido = cantidad_perdida * precio

                        if importe_perdido > importe_max_perdido:
                            importe_max_perdido = importe_perdido
                            producto_max_importe_perdido = farmaco


    except FileNotFoundError:
        with open(archivo_stock, "w", newline="", encoding="utf-8") as stock_file:
            stock_csv = csv.writer(stock_file)
            header = ["NOMBRE_PRODUCTOS", "CANTIDAD", "FECHA_CADUCIDAD"]
            stock_csv.writerow(header)           

                                                # Mostrar el reporte por pantalla
    print("Total de stock perdido: ", total_stock_perdido)      #cantidad TOTAL de stock que se perdio (vencieron)
    
    max_cantidad_farmaco = ""  # Asegúrate de usar el mismo nombre de variable aquí
    max_cantidad_perdida = 0

    for farmaco_info in farmacos_cantidad_perdida:
        if farmaco_info[1] > max_cantidad_perdida:
            max_cantidad_perdida = farmaco_info[1]
            max_cantidad_farmaco = farmaco_info[0]

    print("Fármaco que perdió más cantidad: ", max_cantidad_farmaco, "Cantidad: ", max_cantidad_perdida)
                                                        # Encontrar el fármaco que perdió más cantidad 

    
    print("Fármaco que perdió más importe: ", producto_max_importe_perdido, "Importe: ", importe_max_perdido)
                                                        # Encontrar el farmaco que perdio mas importe
    informes_submenu(usuario_actual)


#############################################################################  
###################################FUNCION MENU PRINCIPAL ###################
#############################################################################   


def menu_principal(usuario_actual):
    print('Este es el menu principal, que desea hacer? ')
    print('1. Gestion de usuarios')
    print('2. Gesion de inventario')  
    print('3. informes') 
    print('4. Salir') 
   
    queHacer = input('que desea hacer?: ')
    
    
    while  queHacer !='1' and queHacer  !='2' and queHacer !='3' and queHacer !='4':        #si presiona otra opcion, pide ingresar nuevamente
        queHacer = input('ERROR, que desea hacer?: ')
   
    if queHacer == '1':
        gestion_usuario_Submenu(usuario_actual)
        
    elif queHacer == '2' and (usuario_actual[2]=='vendedor' or usuario_actual[2]=='farmaceutico'):   #si quiere hacer gestion de inventario tiene que ser farmaceutico o vendedor
        gestionInventario(usuario_actual)
        
    elif queHacer == '3':
        informes_submenu(usuario_actual)
        
    elif queHacer == '4':
        print('Estas saliendo del programa, estas seguro? ')
        print('1. nuevo inicio de  sesion ')
        print('2. abandonar sistema')
        queHacerSalir = input('que desea hacer?: ')

        while queHacerSalir !='1' and queHacerSalir !='2':
            print('error ingreso incorrecto presione 1 o 2 ')
            queHacerSalir = input('que desea hacer?: ')
            
        if queHacerSalir == '1':
            usuario_actual = []                 #SE REINICIA EL USUARIO ACTUAL DE 0 YA QUE AHORA SE VA AGREGAR OTRO CON OTRA INFO
            
            if inicio_sesion(usuario_actual) == True:
                menu_principal(usuario_actual)
            
            
        elif queHacerSalir == '2':              #si presiona 2 se sale del sistema
            print('********ABANDONASTE EL SISTEMA********')
            
    else:
        print('************************')
        print('NO TIENE LOS PERMISOS NECESARIOS')
        print('************************')
        menu_principal(usuario_actual)

#############################################################################  
###################################FUNCION SUBMENU INFORMES #################
############################################################################# 

 
def informes_submenu(usuario_actual):
    print("***************SUBMENU INFORMES***************")
    print('a. Ranking importe/cantidad')
    print('b. Promedio dias')
    print('c. Informes productos vencidos')
    print('d. volver al menu principal')
    
    queHacerInformes = input('Que desea hacer: ')
    
    
    while queHacerInformes !='a'and queHacerInformes  !='b' and queHacerInformes !='c' and queHacerInformes !='d':
        queHacerInformes = input('ERROR, Que desea hacer: ')                                                    #si presiona otra opcion pide ingresar devuelta
    
    if queHacerInformes == 'a':
        InformeRanking(usuario_actual)
        
    elif queHacerInformes == 'b':
        promedioFechaYVencimiento(usuario_actual)
        
    elif queHacerInformes == 'c':
        informeProductosVencidos(usuario_actual)
       
        
    elif queHacerInformes =='d':
        menu_principal(usuario_actual)