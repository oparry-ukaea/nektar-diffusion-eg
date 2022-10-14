import math
import os
import os.path
import csv

from common.timesteps import get_times
from gen_lorenz_data import default_params as lorenz_params
from gen_lorenz_data import gen_data_from_times as gen_lorenz_data

scripts_dir = os.path.dirname(os.path.realpath(__file__))

k = 1 # Thermal conductivity in W/m^2/K
#==================================================================================================
def get_BCs(mode='lorenz', dt_mode='dirk3', **mode_opts):
    times = get_times(dt_mode)
    temps = get_temps(times, mode=mode, **mode_opts)
    return zip(times,temps)
#==================================================================================================

#==================================================================================================
def get_temps(times, mode='lorenz', **mode_opts):
    if mode=='lorenz':
        T = [1+2*it[2]/lorenz_params["rho"]/k for it in gen_lorenz_data(times)]
    elif mode=='sin':
        Omega = mode_opts.get('Omega',2.0)
        T = [math.sin(Omega*time) for time in times]
    else:
        exit(f"write_file: '{mode}' is not a valid mode")
    return T
#==================================================================================================

#==================================================================================================
def write_file(fpath, T):
    header_vals = ["x","T"]
    with open(fpath, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(header_vals)
        writer.writerow([0,T])
        writer.writerow([1,T])
#==================================================================================================


#==================================================================================================
def main(mode="lorenz"):
    template_dir = os.path.join(scripts_dir,"..","runs","templates",f"file-based_{mode}")
    print(f"Creating BC files in {template_dir}")

    mode_opts = {}
    dt_mode='dirk3'
    
    for time, T in get_BCs(mode=mode, dt_mode=dt_mode, **mode_opts):
        fname = "BCVals_{:5.2E}.csv".format(time)
        fpath = os.path.join(template_dir,fname)
        write_file(fpath,T)    
    print("Done")
#==================================================================================================

if __name__=="__main__":
    main()