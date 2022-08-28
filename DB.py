"""
Proyecto 2 - Lógica Matemática - Universidad del Valle de Guatemala
Fecha: Agosto de de 2022
Autor: Equipo Random
"""

from neo4j import GraphDatabase, WRITE_ACCESS
from Code.DB_Nodos import Nodos


def crear_relacion(usuario, categoria, relacion, nodo):
    """
        Método que crea una relación ÚNICA en formato string.
        :param usuario: usuario
        :param categoria: categoria
        :param relacion: relacion
        :param nodo: nombre del nodo al que se quiere relacionar el usuario.
        :return: una relacion en string
        """
    query = f"MATCH ({usuario}:User {{nombre:\"{usuario}\"}}), ({nodo}:{categoria} {{nombre:\"{nodo}\"}}) " \
            f"CREATE ({usuario})-[:{relacion}]->({nodo}) "
    return query


class DB:
    def __init__(self, uri, user, password):
        """

        :param uri: nombre del servidor local de Neo4J
        :param user: El usuario del servidor (neo4j)
        :param password: la contraseña del servidor local.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def base(self):
        """
        Inicializa la base de datos
        """
        session = self.driver.session(default_access_mode=WRITE_ACCESS)
        noditos = Nodos().creador_nodos()
        relaciones = Nodos().relacions_DB_total()
        session.run(noditos)
        for usuario in relaciones:
            for relacion in usuario:
                session.run(relacion)
        session.close()

    def match(self, nodo_nivel_usuario, relacion_modalidad_nivel, relacion_apertura_o_defensa, apertura_defensa_nodo):
        """
        Método para crear las relaciones de losnodos.
        :param nodo_nivel_usuario: NIVEL_BLITZ, NIVEL_RAPIDAS
        :param relacion_modalidad_nivel: modalidad favorita del usuario.
        :param relacion_apertura_o_defensa: apertura o defensa del usuario.
        :param apertura_defensa_nodo: apertura o defnesa del usuario.
        :return: un string con las relaciones.
        """
        session = self.driver.session(default_access_mode=WRITE_ACCESS)
        query = f"MATCH ({nodo_nivel_usuario}:Nivel {{nombre:\"{nodo_nivel_usuario}\"}})<-[:{relacion_modalidad_nivel}]-(User)-[r:{relacion_apertura_o_defensa}]->({apertura_defensa_nodo}) RETURN {apertura_defensa_nodo}.nombre, count(r) AS num ORDER BY num desc "
        result = session.run(query)
        vacio = []
        for element in result:
            vacio.append(element[f"{apertura_defensa_nodo}.nombre"])
        session.close()
        listafinal = ','.join(str(elemento) for elemento in vacio)
        listafinal = listafinal.split(",")
        return listafinal

    def queries_user_nuevo(self, USER, NIVEL_BLITZ, NIVEL_RAPIDAS, PARTE_FAVORITA, PLATAFORMA, APERTURA, DEFENSA):
        """

        :param USER: Usuario
        :param NIVEL_BLITZ: Nivel de blitz
        :param NIVEL_RAPIDAS: Nivel de rápidas
        :param PARTE_FAVORITA: Parte favorita
        :param PLATAFORMA: Plataforma favorita
        :param APERTURA: Apertura favorita
        :param DEFENSA: Defensa favorita
        :return: Una cada con las instrucciones a crear
        """
        query_nodo_user: str = f"CREATE ({USER.lower()}:User {{nombre:\"{USER.lower()}\"}})"
        categorias = ["Nivel", "Plataforma", "Apertura", "Defensa", "Favorito"]
        relacions = ["NIVEL_BLITZ", "NIVEL_RAPIDAS", "PARTE_FAVORITA", "PLATAFORMA", "APERTURA", "DEFENSA"]
        query_relacion_nivel_blitz: str = crear_relacion(USER, categorias[0], relacions[0], NIVEL_BLITZ)
        query_relacion_nivel_rapidas: str = crear_relacion(USER, categorias[0], relacions[1], NIVEL_RAPIDAS)
        query_relacion_parte_favorita: str = crear_relacion(USER, categorias[4], relacions[2], PARTE_FAVORITA)
        query_relacion_plataforma: str = crear_relacion(USER, categorias[1], relacions[3], PLATAFORMA)
        query_relacion_apertura: str = crear_relacion(USER, categorias[2], relacions[4], APERTURA)
        query_relacion_defensa: str = crear_relacion(USER, categorias[3], relacions[5], DEFENSA)
        return query_nodo_user, query_relacion_nivel_blitz, query_relacion_nivel_rapidas, query_relacion_parte_favorita, query_relacion_plataforma, query_relacion_apertura, query_relacion_defensa

    def crear_user(self, USER, NIVEL_BLITZ, NIVEL_RAPIDAS, PARTE_FAVORITA, PLATAFORMA, APERTURA, DEFENSA):
        """
        Crea las relaciones de un nuevo usuario en la base de datos.
        :param USER: Usuario
        :param NIVEL_BLITZ: Nivel de blitz
        :param NIVEL_RAPIDAS: Nivel de rápidas
        :param PARTE_FAVORITA: Parte favorita
        :param PLATAFORMA: Plataforma favorita
        :param APERTURA: Apertura favorita
        :param DEFENSA: Defensa favorita
        """
        query_nodo_user, query_relacion_nivel_blitz, query_relacion_nivel_rapidas, query_relacion_parte_favorita, query_relacion_plataforma, query_relacion_apertura, query_relacion_defensa = self.queries_user_nuevo(
            USER, NIVEL_BLITZ, NIVEL_RAPIDAS, PARTE_FAVORITA, PLATAFORMA, APERTURA, DEFENSA)

        session = self.driver.session(default_access_mode=WRITE_ACCESS)
        session.run(query_relacion_apertura)
        session.run(query_nodo_user)
        session.run(query_relacion_nivel_blitz)
        session.run(query_relacion_nivel_rapidas)
        session.run(query_relacion_parte_favorita)
        session.run(query_relacion_plataforma)
        session.run(query_relacion_apertura)
        session.run(query_relacion_defensa)
        session.close()

    def borrar_user(self, user):
        """
        Borra un usuario insertando su ID.
        :param user: id del usuario.
        """
        session = self.driver.session(default_access_mode=WRITE_ACCESS)
        query = f"MATCH (n {{nombre: '{user}'}}) DETACH DELETE n"
        session.run(query)
        session.close()

    def borrar_DB(self):
        """
        Borra la base de datos.
        """
        session = self.driver.session(default_access_mode=WRITE_ACCESS)
        query = "MATCH (n) DETACH DELETE n"
        session.run(query)
        session.close()

    def close(self):
        """
        Cierra el driver.
        """
        self.driver.close()


