from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

conexion = MySQL(app)

def validar_vehiculos(id_vehiculo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM vehiculos WHERE id_patente = '{0}';".format(id_vehiculo)

        cursor.execute(sql)
        datos = cursor.fetchall()
        for i in datos:
            if i[0] == id_vehiculo:
                return True
            else:
                return False
    except Exception as ex:
        return jsonify({'respuesta': "Error"})