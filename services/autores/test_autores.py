from conexion import *
import pytest   

class Test_autores:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5087/autores"
        idAutor = "A001"
        nombre = "Jose Gustabo Posada"
        email = "jose@gmail.com"
        idPais = "CO"
        sql = f"INSERT INTO autores (idAutor,nombre,email,idPais) VALUES ('{idAutor}','{nombre}','{email}','{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    

    def test_lista_autores(self):
        esperado = "autores"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idAutor":"A002","nombre":"Prueba","email":"prueba@example.com","idPais":"PE"},"Autor agregado con exito"),  
         ({"idAutor":"A001","nombre":"Jose Gustabo Posada","email":"jose@gmail.com","idPais":"CO"},"Id de autor ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        idAutor = nuevo_entrada["idAutor"]
        nombre = nuevo_entrada["nombre"]
        email = nuevo_entrada["email"]
        idPais = nuevo_entrada["idPais"]
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"], 
        [("A001","Autor encontrado"),
         ("A009","Id no encontrado")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        idAutor = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{idAutor}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
    
    #Para cuando el pais existe y se modifica con éxito
    def test_modifica1(self):
        idAutor = "A001"
        nombre = "Jose Gustabo Posada Modificado"
        email = "josegustavomodificado@márquez.com"
        idPais = "CO"
        nuevo = {"idAutor":idAutor,"nombre":nombre,"email":email,"idPais":idPais}
        esperado = "Autor modificado con exito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{idAutor}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]

        sql = f"SELECT * FROM autores WHERE idAutor='{idAutor}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and email==datos[2] and idPais==datos[3]

    # Para cuando el país no existe y se intenta modificar
    def test_modifica2(self):
        idAutor = "A009"
        nombre = "Autor de Prueba Modificado"
        email = "prueba.modificada@gmail.com"
        idPais = "VD"
        nuevo = {"idAutor":idAutor,"nombre":nombre,"email":email,"idPais":idPais}
        esperado = "Autor no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{idAutor}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
        
    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("A001","Autor eliminado con exito!"),
         ("A009","Autor no existe")]
    )
    def test_elimina(self,id_entrada,esperado_entrada):
        idAutor = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{idAutor}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado == calculado.json()["mensaje"]
        sql = f"SELECT * FROM autores WHERE idAutor='{idAutor}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        mi_db.commit()
        assert len(datos)==0

    def teardown_class(self):
        # Limpia la base de datos
        sql = f"DELETE FROM autores WHERE idAutor='A001'"
        mi_cursor.execute(sql)
        mi_db.commit()