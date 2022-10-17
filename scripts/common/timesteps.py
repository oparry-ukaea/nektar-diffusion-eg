# Default parameters
#   Dirk3 Lambda value from https://doc.nektar.info/developerguide/5.0.2/developer-guidese22.html
dt_params_default = dict(uniform=dict(dt=0.001, N=100000),
                        dirk3=dict(dt_major=0.001,N_major=10000,_lambda=0.4358665215)
                        )

#==================================================================================================
def gen_timesteps(dt_mode,params=None):
    if params is None:
        params = dt_params_default[dt_mode]
    if dt_mode=="uniform":
        dts = [params["dt"]]*params["N"]
    elif dt_mode=="dirk3":
        substep_ratios= [params["_lambda"], (1-params["_lambda"])/2, (1-params["_lambda"])/2]
        dts = []
        for ii in range(params["N_major"]):
            dts.extend([r*params["dt_major"] for r in substep_ratios])
    return dts
#==================================================================================================

#==================================================================================================
def get_times(dt_mode,t_init=0,params=None):
    dts = gen_timesteps(dt_mode, params=params)
    # Prepend t_init
    times = [t_init]
    # Sum dts, excluding final one
    for ii in range(len(dts)-1):
        times.append(times[ii]+dts[ii])
    return times
#==================================================================================================