import os
import time
#import numpy as np
import mysql.connector
from scipy.integrate import odeint

def db_connect(host, user, password, db):
    mydb = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = db
    )
    return mydb

mydb = db_connect(os.environ.get('DB_HOST'), os.environ.get('MYSQL_USER'), os.environ.get('MYSQL_PASSWORD'), os.environ.get('MYSQL_DATABASE'))
mycursor = mydb.cursor()

def vehicle(v,t,u,load):
    # inputs
    #  v    = vehicle velocity (m/s)
    #  t    = time (sec)
    #  u    = gas pedal position (-50% to 100%)
    #  load = passenger load + cargo (kg)
    Cd = 0.44    # drag coefficient https://www.carinf.com/en/c380425176.html
    rho = 1.225  # air density (kg/m^3)
    A = 2.8    # cross-sectional area (m^2)
    Fp = 20      # thrust parameter (N/%pedal)
    m = 940      # vehicle mass (kg)
    # calculate derivative of the velocity
    dv_dt = (1.0/(m+load)) * (Fp*u - 0.5*rho*Cd*A*v**2)
    return dv_dt

delta_t = 0.1  # how long is each time step?

# simulate step test operation
# passenger(s) + cargo load
load = 100.0 # kg
# velocity initial condition
v0 = 0.0
# set point
# for storing the results
ubias = 0.0
Kc = 1.04 * 2.5
tauI = 45.0
sum_int = 0.0
sp_kmh = 0
i = 0
sp = 25.0
last_update = 0

starttime = time.time()
while(True):
    if(last_update == 0 or time.time() - last_update > 1):
        mycursor.execute("SELECT speed FROM speed ORDER BY Id DESC LIMIT 1;")
        result = mycursor.fetchall()
        if mycursor.rowcount > 0:
            for x in result:
                sp_kmh = x[0]
                sp = sp_kmh/3.6
        else:
            sp = 0
        last_update = 0
    
    error = sp - v0
    sum_int = sum_int + error * delta_t
    u = ubias + Kc*error + Kc/tauI * sum_int

    # clip inputs to -50% to 100%
    if u >= 100.0:
        u = 100.0
        sum_int = sum_int - error * delta_t
    if u <= -50.0:
        u = -50.0
        sum_int = sum_int - error * delta_t
    
    v = odeint(vehicle,v0,[0,delta_t],args=(u,load))
    v0 = float(v[-1])
    if v0 < 0:
        v0 = 0.0
        
    if sp == 0 and v0 == 0:
        u = 0
    if(last_update == 0 or time.time() - last_update > 1):
        vals = (str(int(time.time() - starttime)), str(v0*3.6), str(sp_kmh), str(u))
        sql = """INSERT INTO data (timestamp, cur_speed, set_speed, throttle) VALUES (%s, %s, %s, %s);"""
        mycursor.execute(sql, vals)
        mydb.commit()
        last_update = time.time()
    time.sleep(delta_t - ((time.time() - starttime) % delta_t))

mycursor.close()    
mydb.close()