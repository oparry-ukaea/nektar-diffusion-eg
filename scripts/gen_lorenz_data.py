"""To generate Nektar boundary conditions based on Lorenz timeseries data, run write_BC_files.py with mode="lorenz" (the default).
   Running this script directly will output the raw data to a CSV file.
"""

import os.path
import numpy as np

from common.timesteps import gen_timesteps

scripts_dir = os.path.dirname(os.path.realpath(__file__))

# Coefficients for scheme 2: Carpenter - Kennedy
A_coeffs = [0.0, -0.4801594388478, -1.404247195, -2.016477077503, -1.056444269767 ]
B_coeffs = [0.1028639988105, 0.7408540575767, 0.7426530946684, 0.4694937902358, 0.1881733382888]

ICs            = dict(x=np.double(0.0), y=np.double(1.0), z=np.double(0.0))
coeffs         = dict(A=A_coeffs, B=B_coeffs)
default_params = dict(ICs=ICs, coeffs=coeffs, sigma=10.0, rho=28.0, beta=8.0/3.0)

#==================================================================================================
def EvaluateLorenzDerivs(x, y, z, params):
    xDot = params["sigma"] * (y - x)
    yDot = x * (params["rho"] - z) - y
    zDot = x * y - params["beta"] * z
    return xDot, yDot, zDot
#==================================================================================================

#==================================================================================================
def IterateLorenz(x, y, z, dt, params):
    A_coeffs = params["coeffs"]["A"]
    B_coeffs = params["coeffs"]["B"]

    xS = yS = zS = np.double(0.0)
    for Ai,Bi in zip(A_coeffs, B_coeffs):
        xDot, yDot, zDot = EvaluateLorenzDerivs(x, y, z,params)
        xS = Ai * xS + dt * xDot
        yS = Ai * yS + dt * yDot
        zS = Ai * zS + dt * zDot
        x += Bi * xS
        y += Bi * yS
        z += Bi * zS
    return x, y, z    
#==================================================================================================

#==================================================================================================
def write_data(data):
    fpath = os.path.join(scripts_dir,"lorenz.csv")
    names = ["x","y","z"]
    dtype = dict(names = names, formats=[np.double,np.double,np.double])
    arr = np.array(data, dtype=dtype)
    np.savetxt(fpath, arr, delimiter=',', fmt=['%.6e' , '%.6e', '%.6e'], header=",".join(names), comments='')
    print(f"Data written to {fpath}")
#==================================================================================================

#==================================================================================================
def gen_timesteps_and_data(dt_mode,params=default_params):
    dts = gen_timesteps(dt_mode)
    return gen_data(dts,params=params)
#==================================================================================================

#==================================================================================================
def gen_data(dts,params=default_params):
    # Extract initial conditions, timestep, A and B coefficients from params
    ICs   = params["ICs"]
    ix,iy,iz = ICs["x"],ICs["y"],ICs["z"]

    data = []
    for dt in dts:
        ix,iy,iz = IterateLorenz(ix,iy,iz,dt,params)
        data.append((ix,iy,iz))
    return data
#==================================================================================================

#==================================================================================================
def gen_data_from_times(times,params=default_params):
    print("Generating Lorenz timeseries")
    dts = []
    for ii in range(1,len(times)):
        dts.append(times[ii]-times[ii-1])
    return gen_data(dts,params=params)
#==================================================================================================

#==================================================================================================
def main(dt_mode='dirk3',params=default_params):
    """Output data to a CSV file"""
    data = gen_timesteps_and_data(dt_mode,params=params)
    write_data(data)
#==================================================================================================

if __name__=="__main__":
    main()