import argparse
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
def get_BCs(template='lorenz', dt_mode='dirk3', **mode_opts):
    times = get_times(dt_mode)
    temps = get_temps(times, template=template, **mode_opts)
    return zip(times,temps)
#==================================================================================================

#==================================================================================================
def get_temps(times, template='lorenz', **mode_opts):
    if template=='lorenz':
        T = [1+2*it[2]/lorenz_params["rho"]/k for it in gen_lorenz_data(times)]
    elif template=='sin':
        Omega = mode_opts.get('Omega',2.0)
        T = [math.sin(Omega*time) for time in times]
    else:
        exit(f"write_file: '{template}' is not a valid template")
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
def main(template="lorenz", dt_mode='dirk3'):
    template_dir = os.path.join(scripts_dir,"..","runs","templates",f"file-based_{template}")
    print(f"Creating BC files in {template_dir}")

    mode_opts = {}
    
    for time, T in get_BCs(template=template, dt_mode=dt_mode, **mode_opts):
        fname = "BCVals_{:5.2E}.csv".format(time)
        fpath = os.path.join(template_dir,fname)
        write_file(fpath,T)    
    print("Done")
#==================================================================================================

#==================================================================================================
def parseCLargs():
    parser = argparse.ArgumentParser()
    valid_templates = ["lorenz","sin"]
    template_desc =  "Specify which file-based template to populate. Options are: lorenz (default), sin"
    parser.add_argument("-t", "--template", help=template_desc)

    args = parser.parse_args()
    options = {}
    if args.template:
        allowed_prefix = 'file-based_'
        template = args.template[len(allowed_prefix):] if args.template.startswith(allowed_prefix) else args.template
        if template in valid_templates:
            options['template'] = template
        else:
            exit(f"'{template}' is not a valid template; use '"+"' or '".join(valid_templates)+"'")
    return options
#==================================================================================================


if __name__=="__main__":
    options = parseCLargs()
    main(**options)