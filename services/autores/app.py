from conexion import *
from autores import mis_autores

programa = Flask(__name__)
api = Api(programa)

class ListaAutores(Resource):
    def get(self):
        autores = mis_autores.listar()
        return jsonify({"mensaje": "autores","data": autores})
    def post(self):
        nuevo=request.json
        resultado = mis_autores.consultar(nuevo["idAutor"])
        if len(resultado)==0:
            mis_autores.agregar(nuevo["idAutor"],nuevo["nombre"],nuevo["email"],nuevo["idPais"])
            return jsonify({"mensaje":"Autor agregado con exito"})
        else:
            return jsonify({"mensaje":"Id de autor ya existe"})

class Autor(Resource):
    def get(self,idAutor):
        resultado = mis_autores.consultar(idAutor)
        if len(resultado)==0:
            return jsonify({"mensaje":"Id no encontrado"})
        else:
            return jsonify({"mensaje":"Autor encontrado","autor":resultado[0]})
    def put(self,idAutor):
        nuevo=request.json
        resultado = mis_autores.consultar(idAutor)
        if len(resultado)==0:
            return jsonify({"mensaje":"Autor no existe"})
        else:
            mis_autores.modificar(nuevo["idAutor"],nuevo["nombre"],nuevo["email"],nuevo["idPais"])
            return jsonify({"mensaje":"Autor modificado con exito"})
    def delete(self,idAutor):
        resultado = mis_autores.consultar(idAutor)
        if len(resultado)==0:
            return jsonify({"mensaje":"Autor no existe"})
        else:
            mis_autores.eliminar(idAutor)
            return jsonify({"mensaje":"Autor eliminado con exito!"})

api.add_resource(ListaAutores, "/autores")
api.add_resource(Autor,"/autores/<idAutor>")

if __name__=="__main__":
    programa.run(host="0.0.0.0",debug=True,port=5087)
