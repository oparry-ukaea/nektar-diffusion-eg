import math
import os
import os.path
import csv

#==================================================================================================
def write_file(fpath,time,Omega=2.0):
    u = math.sin(Omega*time)
    header_vals = ["x","u"]
    with open(fpath, 'w') as fh:
        writer = csv.writer(fh)
        writer.writerow(header_vals)
        writer.writerow([0,u])
        writer.writerow([1,u])
#==================================================================================================

#==================================================================================================
def get_times(dstep = 1e-3,nsteps = 1000,substeps = [0, 4.36e-4, 7.18e-4]):
    # Generate timestep pattern (for implicit)   
    steps = [ii*dstep for ii in range(nsteps)]    
    times = []
    for step in steps:
        times.extend([step+substep for substep in substeps])
    return times
#==================================================================================================

#==================================================================================================
def main(template="chaotic"):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    for time in get_times():
        fname = "BCVals_{:5.2E}.csv".format(time)
        fpath = os.path.join(root_dir,"runs","templates",template,fname)
        write_file(fpath,time)
#==================================================================================================

main()