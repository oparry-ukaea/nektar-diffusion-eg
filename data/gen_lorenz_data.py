import os.path
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))

# Coefficients for scheme 2: Carpenter - Kennedy
A_coeffs = [0.0, -0.4801594388478, -1.404247195, -2.016477077503, -1.056444269767 ]
B_coeffs = [0.1028639988105, 0.7408540575767, 0.7426530946684, 0.4694937902358, 0.1881733382888]

ICs      = dict(x=np.double(0.0), y=np.double(1.0), z=np.double(0.0))
coeffs   = dict(A=A_coeffs, B=B_coeffs)
params   = dict(ICs=ICs, coeffs=coeffs, dt=0.001, sigma=10.0, rho=28.0, beta=8.0/3.0, nit=100000)

#==================================================================================================
def EvaluateLorenzDerivs(x, y, z, params):
    xDot = params["sigma"] * (y - x)
    yDot = x * (params["rho"] - z) - y
    zDot = x * y - params["beta"] * z
    return xDot, yDot, zDot
#==================================================================================================

#==================================================================================================
def IterateLorenz(x,y,z, params):
    dt    = params["dt"]
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
    fpath = os.path.join(script_dir,"lorenz.csv")
    names = ["x","y","z"]
    dtype = dict(names = names, formats=[np.double,np.double,np.double])
    arr = np.array(data, dtype=dtype)
    np.savetxt(fpath, arr, delimiter=',', fmt=['%.6e' , '%.6e', '%.6e'], header=",".join(names), comments='')
#==================================================================================================

#==================================================================================================
def main():
    print("Lorenz model time series generator.")
    
    # Extract initial conditions, timestep, A and B coefficients from params
    ICs   = params["ICs"]
    ix,iy,iz = ICs["x"],ICs["y"],ICs["z"]

    data = []
    for it in range(params["nit"]):
        ix,iy,iz = IterateLorenz(ix,iy,iz,params)
        data.append((ix,iy,iz))
    write_data(data)
#==================================================================================================

main()