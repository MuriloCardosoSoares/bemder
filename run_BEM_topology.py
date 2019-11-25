#%% Import Packages and define simulation

import matplotlib.pyplot as plt
import pandas as pd
import bempp.api
import numpy as np
import bemder.porous as porous
from bemder.room_api import RoomBEM

#% Defining constants
c0 = 343 #Speed ou sound
rho0 = 1.21 #Air density


#% Load mesh
filename = 'topology.msh'
grid = bempp.api.import_grid('Mshs/'+filename)

#Defining frequencies of analysis 
f1= 20
f2 = 150
df = 2
f_range = np.arange(f1,f2+df,df)

#Defining Surface admittance
muh = np.zeros_like(f_range)
zsd1 = porous.delany(5000,0.1,f_range)
zsd2 = porous.delany(10000,0.2,f_range)
zsd3 = porous.delany(15000,0.3,f_range)
mud1 = np.complex128(rho0*c0/np.conj(zsd1))
mud2 = np.complex128(rho0*c0/np.conj(zsd2))
mud3 = np.complex128(rho0*c0/np.conj(zsd3))

mu = {}

mu[1] = mud1
mu[2] = mud2
mu[3] = mud3


points = {}
points[0] = np.array([0.5,1.5,1.2])
#points[1] = np.array([0.6,0.2,-0.15])


r0 = {}
r0[0] =  np.array([-0.5,4,1.2])
#r0[1] = np.array([1.4,-0.7,-0.35])

q = {}
q[0] = 1
#q[1] = 1

#% Defining grid plot properties 
plane = 'xy'
d = 0

grid_size = [0,6,-3,3]

n_grid_pts = 250



space = bempp.api.function_space(grid, "DP", 0)


#%% Solve BEM

s1 = RoomBEM(space,f_range,r0,q,mu,c0)

p,u = s1.bemsolve()

pT = s1.point_evaluate(points,p,u)

#%% Plot Comparison between Bempp and Validation
data = pd.read_csv('Data/topology_cmplx_r1.csv', sep=",", header=None)
data.columns = ["freq","spl","arg"]

err = np.abs((np.array([data.spl]).reshape(len(pT),1) - 20*np.log10(np.abs(pT)/2e-5)).mean(axis=1))

plt.plot(f_range, 20*np.log10(np.abs(pT)/2e-5))
#plt.plot(f_range, np.real(pT))
plt.plot(data.freq,data.spl)
plt.legend(['bempp','validation'])
plt.xlabel('Frequency [Hz]')
plt.ylabel('SPL [dB]')
plt.savefig('topology_r0_r1_cmplx_SPL.png', dpi=500)
plt.show()

plt.plot(f_range, np.angle(pT))
#plt.plot(f_range, np.real(pT))
plt.plot(data.freq,data.arg)
plt.legend(['bempp','validation'])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [rad]')
plt.savefig('topology_r0_r1_cmplx_phase.png', dpi=500)
plt.show()

plt.plot(f_range, err)

plt.legend(['bempp','validation'])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Error [dB]')
plt.savefig('topology_r0_r1_err.png', dpi=500)
plt.show()
