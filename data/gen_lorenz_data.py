import os.path
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))

# Coefficients for scheme 2: Carpenter - Kennedy
A_coeffs = [0.0, -0.4801594388478, -1.404247195, -2.016477077503, -1.056444269767 ]
B_coeffs = [0.1028639988105, 0.7408540575767, 0.7426530946684, 0.4694937902358, 0.1881733382888]

ICs           = dict(x=np.double(0.0), y=np.double(1.0), z=np.double(0.0))
coeffs        = dict(A=A_coeffs, B=B_coeffs)
# Dirk3 Lambda value from https://doc.nektar.info/developerguide/5.0.2/developer-guidese22.html
all_dt_params = dict(orig=dict(dt=0.001, nit=100000),dirk3=dict(step=0.001,Nstep=1000,_lambda=0.4358665215))
global_params = dict(ICs=ICs, coeffs=coeffs, sigma=10.0, rho=28.0, beta=8.0/3.0, dt=all_dt_params)

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
    fpath = os.path.join(script_dir,"lorenz.csv")
    names = ["x","y","z"]
    dtype = dict(names = names, formats=[np.double,np.double,np.double])
    arr = np.array(data, dtype=dtype)
    np.savetxt(fpath, arr, delimiter=',', fmt=['%.6e' , '%.6e', '%.6e'], header=",".join(names), comments='')
    print(f"Data written to {fpath}")
#==================================================================================================

#==================================================================================================
def gen_timesteps(all_dt_params,dt_mode='fixed'):
    dt_params = all_dt_params[dt_mode]
    if dt_mode=="orig":
        dts = [dt_params["dt"]]*dt_params["nit"]
    elif dt_mode=="dirk3":
        substep_ratios= [dt_params["_lambda"], (1-dt_params["_lambda"])/2, (1-dt_params["_lambda"])/2]
        dts = []
        for ii in range(dt_params["Nstep"]):
            dts.extend([r*dt_params["step"] for r in substep_ratios])
    return dts
#==================================================================================================


#==================================================================================================
def main(dt_mode='dirk3',params=global_params):
    # Extract initial conditions, timestep, A and B coefficients from params
    ICs   = params["ICs"]
    ix,iy,iz = ICs["x"],ICs["y"],ICs["z"]

    data = []
    dts = gen_timesteps(params["dt"], dt_mode)
    for dt in dts:
        ix,iy,iz = IterateLorenz(ix,iy,iz,dt,params)
        data.append((ix,iy,iz))
    write_data(data)
#==================================================================================================

main()