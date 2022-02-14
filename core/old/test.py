import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

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
    Fp = 22      # thrust parameter (N/%pedal)
    m = 940      # vehicle mass (kg)
    # calculate derivative of the velocity
    dv_dt = (1.0/(m+load)) * (Fp*u - 0.5*rho*Cd*A*v**2)
    return dv_dt

tf = 300                 # final time for simulation
nsteps = 301               # number of time steps
delta_t = tf/(nsteps-1)   # how long is each time step?
ts = np.linspace(0,tf,nsteps) # linearly spaced time vector

# simulate step test operation
step = np.zeros(nsteps) # u = valve % open
# passenger(s) + cargo load
load = 200.0 # kg
# velocity initial condition
v0 = 0.0
# set point
vs = np.zeros(nsteps)
ubias = 0.0
Kc = 1.04 * 3
tauI = 40
sum_int = 0.0
es = np.zeros(nsteps)
sps = np.zeros(nsteps)
sp = 25

plt.figure(1,figsize=(5,4))
if animate:
    plt.ion()
    plt.show()

# simulate with ODEINT
for i in range(nsteps-1):
    if i == 50:
        sp = 0
    if i == 100:
        sp = 15
    if i == 150:
        sp = 20
    if i == 200:
        sp = 10
    sps[i+1] = sp
    error = sp - v0
    es[i+1] = error
    sum_int = sum_int + error * delta_t
    u = ubias + Kc*error + Kc/tauI * sum_int
    # clip inputs to -50% to 100%
    if u >= 100.0:
        u = 100.0
    if u <= -25.0:
        u = -25.0
    step[i+1] = u
    v = odeint(vehicle,v0,[0,delta_t],args=(u,load))
    if v[-1] < 0:
        v[-1] = 0
    v0 = v[-1]   # take the last value
    vs[i+1] = v0 # store the velocity for plotting

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