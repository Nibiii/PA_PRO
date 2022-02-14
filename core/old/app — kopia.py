import os
import time
import random
import mysql.connector

def db_connect(host, user, password, db):
    mydb = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = db
    )
    return mydb

mydb = db_connect("127.0.0.1", "webapp", "example", "db")
mycursor = mydb.cursor()

while(True):
    start = time.perf_counter()
    mycursor.execute("SELECT speed FROM speed ORDER BY Id DESC LIMIT 1;")
    result = mycursor.fetchall()
    if mycursor.rowcount > 0:
        speed = result[0]
    else:
        speed = random.randrange(0,300)
    cur_speed = random.randrange(0,300)
    mycursor.execute("INSERT INTO data (timestamp, cur_speed, set_speed) VALUES ({}, {}, {});".format(time.time(), cur_speed, speed))
    mydb.commit()
    stop = time.perf_counter()
    print(stop-start)
    time.sleep(1 - (stop-start))
    stop2 = time.perf_counter()
    print(stop2-start)

mycursor.close()    
mydb.close()