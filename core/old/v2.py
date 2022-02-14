import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import time

# animate plots?
animate=False # True / False

# define model
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

delta_t = 0.5  # how long is each time step?
ts = [] # linearly spaced time vector

# simulate step test operation
step = [0] # u = valve % open
# passenger(s) + cargo load
load = 200.0 # kg
# velocity initial condition
v0 = 0.0
# set point
# for storing the results
vs = [0]
ubias = 0.0
Kc = 1.0/0.72 * 5.0
tauI = 25.0
sum_int = 0.0
es = [0]
ies = [0]
i = 0
sps = [0]
sp = 25.0
counter = 0
plt.figure(1,figsize=(5,4))
if animate:
    plt.ion()
    plt.show()
    
starttime = time.time()
# simulate with ODEINT
while(True):
    u = step[i]
    if i == 500:
        sp = 0
    if i == 1000:
        sp = 15
    if i == 1500:
        sp = 20
    if i == 2000:
        sp = 10
    
    sps.append(sp)
    error = sp - v0
    es.append(error)
    sum_int = sum_int + error * delta_t
    u = ubias + Kc*error + Kc/tauI * sum_int

    # clip inputs to -50% to 100%
    if u >= 100.0:
        u = 100.0
        sum_int = sum_int - error * delta_t
    if u <= -20.0:
        u = -20.0
        sum_int = sum_int - error * delta_t
    
    ies.append(sum_int)
    step.append(u)
    v = odeint(vehicle,v0,[0,delta_t],args=(u,load))
    v0 = v[-1]
    counter+=delta_t
    ts.append(counter)
    vs.append(v0)
    # plot results
    if animate:
        plt.clf()
        plt.subplot(2,1,1)
        plt.plot(ts[0:i+1],vs[0:i+1],'b-',linewidth=3)
        plt.plot(ts[0:i+1],sps[0:i+1],'k--',linewidth=2)
        plt.ylabel('Velocity (m/s)')
        plt.legend(['Velocity','Set Point'],loc=2)
        plt.subplot(2,1,2)
        plt.plot(ts[0:i+1],step[0:i+1],'r--',linewidth=3)
        plt.ylabel('Gas Pedal')    
        plt.legend(['Gas Pedal (%)'])
        plt.xlabel('Time (sec)')
        plt.pause(0.1)  
    i+=1
    print(time.time())
    time.sleep(delta_t - ((time.time() - starttime) % delta_t))

if not animate:
    # plot results
    plt.subplot(2,1,1)
    plt.plot(ts,vs,'b-',linewidth=3)
    plt.plot(ts,sps,'k--',linewidth=2)
    plt.ylabel('Velocity (m/s)')
    plt.legend(['Velocity','Set Point'],loc=2)
    plt.subplot(2,1,2)
    plt.plot(ts,step,'r--',linewidth=3)
    plt.ylabel('Gas Pedal')    
    plt.legend(['Gas Pedal (%)'])
    plt.xlabel('Time (sec)')
    plt.show()