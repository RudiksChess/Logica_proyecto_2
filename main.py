"""
Proyecto 2 - Lógica Matemática - Universidad del Valle de Guatemala
Fecha: Agosto de de 2022
Autor: Equipo Random
"""
import Code.DB as DB

DATABASE = DB.DB("NEO4J_SERVER_LOCAL_OR_CLOUD", "USER", "PASSWORD")
DATABASE.base()

ans = True
while ans:
    print("""
        |-----------------------------------CLUB DE AJEDREZ -----------------------------------|
        |______________________________SISTEMA DE RECOMENDACIONES______________________________|
        Seleccionar una opción: 
        1. Entrar al sistema de recomendaciones.
        2. Configuraciones (solo administradores).
        3. Salir. 
        """)
    ans = int(input("Opción:"))
    if ans == 1:
        print("""----------------------RESPONDER------------------------------
        ¿Para qué modalidad quiere una recomendación? 
        1. Blitz 
        2. Rápidas.
        """)
        modalidad = int(input("Respuesta:"))

        if modalidad == 1:
            print("""¿Nivel de blitz? Considere: 
                 1. Principiante [0-1400]
                 2. Intermedio [1400-1600]
                 3. Avanzado [1600-infinito]
                 """)
            blitz = int(input("NIVEL_BLITZ: "))
            nivel_blitz = ["principiante", "intermedio", "avanzado"]

            print("De acuerdo a los miembros del club, las aperturas en orden descendente que debería jugar son:")
            print(DATABASE.match(nivel_blitz[blitz-1], "NIVEL_BLITZ", "APERTURA", "Apertura"))
            print("De acuerdo a los miembros del club, las defensas en orden descendente que debería jugar son:")
            print(DATABASE.match(nivel_blitz[blitz-1], "NIVEL_BLITZ", "DEFENSA", "Defensa"))


        elif modalidad == 2:
            print("""¿Nivel de rápidas? Considere: 
                         1. Principiante [0-1400]
                         2. Intermedio [1400-1600]
                         3. Avanzado [1600-infinito]
                         """)
            rapidas = int(input("NIVEL_RÁPIDAS: "))

            nivel_rapidas = ["principiante", "intermedio", "avanzado"]

            print("De acuerdo a los miembros del club, las aperturas en orden descendente que debería jugar son:")
            print(DATABASE.match(nivel_rapidas[rapidas - 1], "NIVEL_RAPIDAS", "APERTURA", "Apertura"))
            print("De acuerdo a los miembros del club, las defensas en orden descendente que debería jugar son:")
            print(DATABASE.match(nivel_rapidas[rapidas - 1], "NIVEL_RAPIDAS", "DEFENSA", "Defensa"))

    elif ans == 2:
        print(""" ------------- CONFIGURACIONES --------------
      Seleccionar una opción: 
      1. Agregar a un usuario.
      2. Borrar a un usuario. 
      """)
        configuraciones = int(input("Opción"))
        if configuraciones == 1:
            print("----Datos del usuario-----")
            id_usuario = str(input("ID_USUARIO:"))
            nivel_blitz = str(input("NIVEL_BLITZ:"))
            nivel_rapidas = str(input("NIVEL_RAPIDAS:"))
            parte_favorita = str(input("PARTE_FAVORITA:"))
            plataforma = str(input("PLATAFORMA:"))
            apertura = str(input("APERTURA:"))
            defensa = str(input("DEFENSA:"))
            DATABASE.crear_user(id_usuario.lower(),nivel_blitz.lower(),nivel_rapidas.lower(),parte_favorita.lower(),plataforma.lower(),apertura.lower(),defensa.lower())
            print("Usuario creado.")
        elif configuraciones == 2:
            ID = str(input("¿Cuál es el ID del usuario?"))
            DATABASE.borrar_user(ID)
            print("Usuario borrado.")

    else:
        print("Programa cerrado. Base de datos borrada.")
        DATABASE.borrar_DB()
        DATABASE.close()
        ans=False
