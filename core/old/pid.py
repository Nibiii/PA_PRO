import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#uchyb = set - read
#Kp = out/in
Cd = 0.4    # drag coefficient https://www.carinf.com/en/c380425176.html
rho = 1.225  # air density (kg/m^3)
A = 2.6    # cross-sectional area (m^2)
Fp = 20      # thrust parameter (N/%pedal)
m = 940      # vehicle mass (kg)
# calculate derivative of the velocity
throttle = 1
dv_dt = (1.0/(m)) * (Fp*100 - 0.5*rho*Cd*A*2.127659574468085**2)
print(dv_dt)
speed = dv_dt
v = np.cbrt((51000 * throttle) / (rho * Cd * A * 1/2))

v2 = np.sqrt(2*51000*0.4/m)

for i in range(50):
    dv_dt_old = dv_dt
    dv_dt = (1.0/(m)) * (Fp*100 - 0.5*rho*Cd*A*dv_dt_old**2)
    speed+=dv_dt
    print(speed)