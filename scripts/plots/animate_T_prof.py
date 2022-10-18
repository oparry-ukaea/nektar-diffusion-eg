import matplotlib.animation as mpl_animation
from matplotlib import pyplot as plt
from utils import calc_analytic, get_plot_path, get_plot_style, get_run_root, read_all_nektar_srcs

#--------------------------------------------------------------------------------------------------
def _animate_1D_profile_comp(run_dir, output_fname="diffusion_eg_Tprof_evo.mp4", mode='comp', nmax=8, save=False, varname='T', **animate_kwargs):
    data_srcs =  read_all_nektar_srcs(run_dir)

    fig, ax = plt.subplots()

    # Get x-vals and params from the first source
    first_src = data_srcs[0]
    x = first_src.get('x')
    params = first_src.get_session().GetParameters()

    if mode=='comp':
        mi = -3e5
        ra = 6e5
    else:
        mi = 0
        #ra=1.2e-4  # D
        ra = 0.01 # N
    ax.set_ylim(mi,mi+ra)
    
    ax.set_xlabel("x")
    ax.set_ylabel(varname)

    nek_line, = ax.plot(x, x/100, **(get_plot_style("points",markevery=20)))
    if mode=='comp':
        an_line, = ax.plot(x, calc_analytic(x,0,params, nmax=nmax), **(get_plot_style("line")))
    def _animate(ii):
        t = params["TIMESTEP"]*params["IO_CHECKSTEPS"]*(ii+1)
        nek_line.set_ydata(data_srcs[ii].get(varname))
        if mode=='comp':
            an_line.set_ydata(calc_analytic(x,t,params, nmax=nmax))
        ax.set_title("t = {:.2f}".format(t))
        return nek_line,

    animate_kwargs = dict(interval=100, blit=False)
    ani = mpl_animation.FuncAnimation(fig, _animate, frames=len(data_srcs), **animate_kwargs )

    if save:
        FFwriter = mpl_animation.FFMpegWriter()
        ani.save(get_plot_path(output_fname), writer = FFwriter)
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    template       = 'file-based_lorenz'
    mode           = 'nektar'
    output_fname   = f"diffusion_eg_{mode}_Tprof_evo.mp4"
    save           = False

    _animate_1D_profile_comp(get_run_root(template), output_fname=output_fname, mode=mode, nmax=8, save=save)
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()