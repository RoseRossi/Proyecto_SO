import psycopg2
from flask import Flask, request
import time
app = Flask(__name__)

#connect to postgres
# la conexión se puso en un bucle while para que la aplicacion no crashee por no iniciar la base de datos 
# primero, por lo tanto, el bucle while forza la conexión para que se de primero, una vez conectada, el break
# rompe la iteración y se pasa a la siguiente parte de la codigo

while True:
    try:
        conn = psycopg2.connect(
            host="postgres",
            user="postgres",
            password="postgres",
            dbname="postgres"
        )
        break
    except psycopg2.Error as exc:
        time.sleep(0.3)


# create a cursor object to execute PostgreSQL commands
# crea un cursor objeto para ejecutar comandos PostgreSQL
cursor = conn.cursor()

def get_hit_count():
    retries = 5
    while True:
        try:
            cursor.execute("SELECT count FROM hit_count")
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO hit_count (count) VALUES (1)")
                conn.commit()
                return 1
            else:
                count = result[0]
                cursor.execute("UPDATE hit_count SET count = %s", (count+1,))
                conn.commit()
                return count+1
        except psycopg2.Error as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# Inicio
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Holiis! has visitado este sitio {} veces.\n'.format(count)

# Endpoints

# Metodo GET 
@app.route('/counter', methods = ['GET'])
def get_counter():
    cursor.execute("SELECT * FROM hit_count")
    return 'Counter: {}'.format(cursor.fetchone()[0])

# Metodo DELETE
@app.route('/counter', methods=['DELETE'])
def delete_counter():
    cursor.execute("UPDATE hit_count SET count = 0")
    conn.commit()
    return 'Counter reset to 0'

# Metodo PUT
@app.route('/counter', methods=['PUT'])
def put_counter():
    count = request.args.get("count")
    cursor.execute("UPDATE hit_count SET count = %s", (count,))
    conn.commit()
    return 'Counter set to {}'.format(count)

# Metodo POST
@app.route('/counter', methods=['POST'])
def post_counter():
    count = request.args.get("count")
    cursor.execute("UPDATE hit_count SET count = %s", (count,))
    conn.commit()
    return 'Counter set to {}'.format(count)