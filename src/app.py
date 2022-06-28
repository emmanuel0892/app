from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
from validaciones import validar_vehiculos

app = Flask(__name__)


conexion = MySQL(app)
#-------------------------------------------------------------------------------------------------------------
# Listar Vehiculo
@app.route('/vehiculos', methods=['GET'])
def listar_vehiculos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM vehiculos;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        vehiculos = []
        for i in datos:
            if i[6] == 1:
                text = "si"
            elif i[6] == 0:
                text = "no"
            vehiculo = {'id_patente':i[0],"chasis":i[1],"año":i[2],"marca":i[3],"modelo":i[4],"color":i[5],"TieneSeguro": text}
            vehiculos.append(vehiculo)
        return jsonify({'vehiculo': vehiculos, 'respuesta': "Lista de vehiculos"})
    except Exception as ex:
        return jsonify({'respuesta': "Error"})
#-------------------------------------------------------------------------------------------------------------
# Registar Vehiculo
@app.route('/vehiculos', methods=['POST'])
def registar_vehiculo():
    try:
        if (request.json['id_patente'] != "" and request.json['chasis'] > 0   and 
            request.json['año'] != ""        and request.json['marca'] != ""  and 
            request.json['modelo'] != ""     and request.json['color'] != ""  and 
            request.json['TieneSeguro'] >= 0 and  request.json['TieneSeguro'] <= 2):   

            cursor = conexion.connection.cursor()
            sql = """INSERT INTO vehiculos (id_patente,chasis,año,marca,modelo,color,TieneSeguro) 
            VALUES ('{0}',{1},'{2}','{3}','{4}','{5}',{6});""".format(request.json['id_patente'],
                                                                    request.json['chasis'],
                                                                    request.json['año'],
                                                                    request.json['marca'],
                                                                    request.json['modelo'],
                                                                    request.json['color'],
                                                                    request.json['TieneSeguro'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'respuesta' : "Vehiculo Registrado"})
        else:
            return jsonify({'respuesta':"No se aceptan campos vacios o con formatos distintos!!!"})
    except Exception as ex:
        return jsonify({'respuesta': "Error"})
#-------------------------------------------------------------------------------------------------------------
# Eliminar Vehiculo
@app.route('/vehiculos/<id_patente>', methods=['DELETE'])
def eliminar_vehiculo(id_patente):
    try:
        validacion = validar_vehiculos(id_patente)
        if validacion == True:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM vehiculos WHERE id_patente = '{0}';".format(id_patente)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'respuesta' : "Vehiculo Eliminado"})
        else:
            return jsonify({'respuesta' : "El vehiculo no existe"})
    except Exception as ex:
        return jsonify({'respuesta': "Error"})
#-------------------------------------------------------------------------------------------------------------
# Actualizar Vehiculo
@app.route('/vehiculos/<id_patente>', methods=['PUT'])
def actualizar_vehiculo(id_patente):
    try:
        validacion = validar_vehiculos(id_patente)
        if validacion == True:
            cursor = conexion.connection.cursor()
            sql = """UPDATE vehiculos SET chasis = {0}, año = '{1}', marca = '{2}', modelo = '{3}', color = '{4}', TieneSeguro = {5} 
            WHERE id_patente = '{6}';""".format(request.json['chasis'],
                                                    request.json['año'],
                                                    request.json['marca'],
                                                    request.json['modelo'],
                                                    request.json['color'],
                                                    request.json['TieneSeguro'],
                                                    id_patente)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'respuesta' : "Vehiculo Actualizado"})
        else:
            return jsonify({'respuesta' : "El vehiculo no existe"})
    except Exception as ex:
        return jsonify({'respuesta': "Error"})
#-------------------------------------------------------------------------------------------------------------
# Manejo de Error
def Error404(error):
    return "<h1>Página no encontrada!!!</h1>",404

if __name__=='__main__':
    app.config.from_object(config['configuracion'])
    app.register_error_handler(404, Error404)
    app.run()