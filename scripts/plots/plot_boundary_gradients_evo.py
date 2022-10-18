from utils import get_plot_path, get_run_root, read_all_nektar_srcs
from matplotlib import pyplot as plt
import numpy as np

#--------------------------------------------------------------------------------------------------
def plot_boundary_gradients_evo(run_dir, output_fname='boundary_gradients_evo.png', varname='T',save=False):
    data_srcs =  read_all_nektar_srcs(run_dir,compute_gradients=True)
    params = data_srcs[0].get_session().GetParameters()
    Nsrcs = len(data_srcs)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.set_xlabel("t")
    ax.set_ylabel("$-\partial T/\partial x\|_{x}$")
    ax.set_yscale('log')
    ax.set_ylim(2e-5,2e-4)
    t  = np.empty((Nsrcs))
    TL = np.empty((Nsrcs))
    TR = np.empty((Nsrcs))

    grad_suffix = "_x"
    for ichk in range(Nsrcs):
        t[ichk] = params["TIMESTEP"]*params["IO_CHECKSTEPS"]*(ichk+1)
        Tprof   = data_srcs[ichk].get(varname+grad_suffix)
        TL[ichk] = Tprof[0]
        TR[ichk] = Tprof[-1]

    filter =  np.logical_and(TL != 0, TR != 0)

    # Plot boundary gradients
    ax.plot(t[filter],-1*TL[filter],color='blue',label='x=0')
    ax.plot(t[filter],-1*TR[filter],color='red', label='x=1')
    ax.legend()
    
    if save:
        plt.savefig(get_plot_path(output_fname))
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    template = 'file-based_lorenz'
    save     = False

    plot_boundary_gradients_evo(get_run_root(template), varname='T', save=save)
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()