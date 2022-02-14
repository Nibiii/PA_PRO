import time
import os
import mysql.connector
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
mydb = None
mycursor = None

def db_connect(host, user, password, db):
    mydb = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = db
    )
    return mydb

def check_if_table_exists():
    mycursor.execute("CREATE TABLE IF NOT EXISTS `data` (`id` INT NOT NULL AUTO_INCREMENT, `timestamp` INT(20) NOT NULL, `cur_speed` FLOAT(20) NOT NULL, `set_speed` INT(20) NOT NULL, `throttle` FLOAT(20) NOT NULL, PRIMARY KEY (`id`));")
    mycursor.execute("CREATE TABLE IF NOT EXISTS `speed` (`id` INT NOT NULL AUTO_INCREMENT, `speed` FLOAT(20) NOT NULL, PRIMARY KEY (`id`));")
    mydb.commit()
    
@app.route('/get')
@cross_origin()
def send_data():
    new_list = []
    mycursor.execute("SELECT timestamp, cur_speed, set_speed, throttle FROM data ORDER BY id ASC;")
    result = mycursor.fetchall()
    if mycursor.rowcount > 0:
        for x in result:
            new_list.append({"timestamp": x[0], "current_speed": x[1], "set_speed": x[2], "throttle": x[3]})
    mydb.commit()
    return jsonify(new_list)

@app.route('/set')
@cross_origin()
def get_data():
    speed = request.args.get('speed')
    mycursor.execute("INSERT INTO speed (speed) VALUES ({});".format(speed))
    mydb.commit()
    return "SUCCESS"

if __name__ == '__main__':
    mydb = db_connect(os.environ.get('DB_HOST'), os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_DATABASE'))
    mycursor = mydb.cursor()
    check_if_table_exists()
    app.run(host="0.0.0.0", port=5001)
