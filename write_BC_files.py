import math
import os
import os.path
import csv

root_dir = os.path.dirname(os.path.realpath(__file__))

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
def get_times(dstep = 5e-3,nsteps = 1000,substeps = [0, 2.18e-3, 3.59e-3]):
    # Generate timestep pattern (for implicit)   
    steps = [ii*dstep for ii in range(nsteps)]    
    times = []
    for step in steps:
        times.extend([step+substep for substep in substeps])
    return times
#==================================================================================================

#==================================================================================================
def read_lorenz_data(npoints,nstride=1,r=28.0):
    data_fpath = os.path.join(root_dir,"data","orig","lorenz.csv")
    data = []
    with open(data_fpath) as fh:
        _ = fh.readline() # skip header
        for ii in range(npoints):
            line = fh.readline()
            if ii % nstride == 0:
                data.append(1+2*float(line.split(",")[2])/r )
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