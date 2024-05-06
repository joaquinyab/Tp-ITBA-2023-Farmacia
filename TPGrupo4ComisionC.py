from funcionesGrupo4ComisionC import *


usuario_actual = []     #ACA SE ALMACENAN LOS DATOS DEL USUARIO ACTUAL (NOMBRE,CLAVE,ROL)
                        ## LA CLAVE DEL usuario: admin es Admin2023 (para empezar a trabajar)
                        

if inicio_sesion(usuario_actual) == True:       #EL USUARIO ENTRA A LA FUNCION INICIAR SESION,
    menu_principal(usuario_actual)              # si el usuario que ingresa es correcto, entra al menu principal y empieza a trabajar


############################################################################################################
################### EN ESTE ARCHIVO  SE TIENE QUE EJECUTAR EL PROGRAMA #####################################
############################################################################################################