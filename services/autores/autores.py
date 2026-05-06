""" 
Se tendrá aquí el modelo para la gestión de autores,
es decir todo aquello que tenga que ver con la persistencia
(SQL)
"""
from conexion import *

class Autores:
    def listar(self):
        sql = "SELECT * FROM autores"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    def consultar(self, idAutor):
        sql = f"SELECT * FROM autores WHERE idAutor = %s"
        mi_cursor.execute(sql, (idAutor,))
        resultado = mi_cursor.fetchall()
        return resultado
    def agregar(self,idAutor,nom,email,idPais):
        sql = f"INSERT INTO autores (idAutor,nombre,email,idPais) VALUES (%s,%s,%s,%s)"
        mi_cursor.execute(sql, (idAutor, nom, email, idPais))
        mi_db.commit()
    def modificar(self, idAutor, nom, email, idPais):
        sql = f"UPDATE autores SET nombre=%s, email=%s, idPais=%s WHERE idAutor=%s"
        mi_cursor.execute(sql, (nom, email, idPais, idAutor))
        mi_db.commit()
        return self.consultar(idAutor)
    def eliminar(self, idAutor):
        sql = f"DELETE FROM autores WHERE idAutor = %s"
        mi_cursor.execute(sql, (idAutor,))
        mi_db.commit()
    
mis_autores = Autores()