import math
import os
import os.path
import csv

root_dir = os.path.dirname(os.path.realpath(__file__))

# Dirk3 Lambda value from https://doc.nektar.info/developerguide/5.0.2/developer-guidese22.html
dt_params_global = dict(orig=dict(dt=0.001, nit=100000),dirk3=dict(step=0.001,Nstep=10000,_lambda=0.4358665215))
k = 40000 # Thermal conductivity in W/m^2/K
#==================================================================================================
def get_BCs(mode='lorenz', **mode_opts):
    times = get_times()
    temps = get_temps(times, mode=mode, **mode_opts)
    return zip(times,temps)
#==================================================================================================

#==================================================================================================
def get_temps(times, mode='lorenz', **mode_opts):
    if mode=='lorenz':
        T = read_lorenz_data(npoints=len(times))
    elif mode=='sin':
        Omega = mode_opts.get('Omega',2.0)
        T = [math.sin(Omega*time) for time in times]
    else:
        exit(f"write_file: '{mode}' is not a valid mode")
    return T
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
def get_times(dt_mode='dirk3'):
    dts = gen_timesteps(dt_params_global, dt_mode=dt_mode)
    # Prepend t=0
    times = [0]
    # Sum dts, excluding final one
    for ii in range(len(dts)-1):
        times.append(times[ii]+dts[ii])
    return times
#==================================================================================================

#==================================================================================================
def read_lorenz_data(npoints,nstride=1,r=28.0):
    data_fpath = os.path.join(root_dir,"data","lorenz.csv")
    data = []
    with open(data_fpath) as fh:
        _ = fh.readline() # skip header
        for ii in range(npoints):
            line = fh.readline()
            if ii % nstride == 0:
                flux = 1+2*float(line.split(",")[2])/r
                data.append(flux/k)
    return data
#==================================================================================================

#==================================================================================================
def write_file(fpath,time, T):

    header_vals = ["x","T"]
    with open(fpath, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(header_vals)
        writer.writerow([0,T])
        writer.writerow([1,T])
#==================================================================================================


#==================================================================================================
def main(mode="lorenz"):

    template_dir = os.path.join(root_dir,"runs","templates",f"file-based_{mode}")
    mode_opts = {}
    
    for time, T in get_BCs(mode=mode, **mode_opts):
        fname = "BCVals_{:5.2E}.csv".format(time)
        fpath = os.path.join(template_dir,fname)
        write_file(fpath,time,T)
#==================================================================================================

main()