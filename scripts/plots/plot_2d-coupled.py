from utils import get_plot_path, get_plot_style, get_run_root, read_nektar_src, read_all_nektar_srcs


import matplotlib.animation as mpl_animation
import matplotlib.pyplot as plt
import numpy as np

#--------------------------------------------------------------------------------------------------
def plot_coupled_scatter(data_srcs,varnames,log=False,output_fpath='Coupled_plot.png',save=False):
    fwidth = 15    
    fig,axarr=plt.subplots(nrows=1,ncols=2, figsize=(fwidth, 7.5))

    for ii,ax in enumerate(axarr):
        s = data_srcs[ii]
        ax.set_title(s.label)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        x = s.get('x')
        y = s.get('y')
        f = s.get(varnames[ii])
        scatter = ax.scatter(x, y, c=f, label=s.label, **s.get_plot_kws())
        
        fig.colorbar(scatter, ax=ax)

    if save:
        fig.savefig(output_fpath)
    else:
        plt.show(block=True)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def animate_coupled_scatters(run_dir, file_bases, chk_start=0, chk_end=100, chk_stride=1, varnames=['T','T'], output_fname='Coupled-BCs.mp4', save=False, **src_kwargs):
    print("Reading "+file_bases[0]+" data")
    left_srcs  = read_all_nektar_srcs(run_dir, chk_start=chk_start,chk_end=chk_end,chk_stride=chk_stride,file_base=file_bases[0], **src_kwargs)
    print("Reading "+file_bases[1]+" data")
    right_srcs = read_all_nektar_srcs(run_dir, chk_start=chk_start,chk_end=chk_end,chk_stride=chk_stride,file_base=file_bases[1], **src_kwargs)

    srcs = [left_srcs,right_srcs]

    # Set up subplots
    fwidth = 15
    fig,axarr=plt.subplots(nrows=1,ncols=2, figsize=(fwidth, 7.5))
    artists = []
    for ii,ax in enumerate(axarr):
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        # First frame to set up colorbar
        first_src = srcs[ii][0]
        artist = ax.scatter(first_src.get('x'), first_src.get('y'), c=first_src.get(varnames[ii]))#, **first_src.get_plot_kws())
        artists.append(artist)
        fig.colorbar(artist,ax=ax)

    # Define update func
    def update(ifrm):
        print("Frame {}/{}".format(ifrm+1,len(srcs[0])))
        for ii,ax in enumerate(axarr):
            src = srcs[ii][ifrm]
            f = src.get(varnames[ii])

            # Set colors
            artists[ii].set_array(f)
            ax.set_title(src.label)

        fig.canvas.draw()
        return artists[0],

    # Then setup FuncAnimation.
    ani = mpl_animation.FuncAnimation(fig, update, interval=1, frames=len(srcs[0]), blit=False)

    if save:
        FFwriter = mpl_animation.FFMpegWriter()
        ani.save(get_plot_path(output_fname), writer = FFwriter)
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def plot_single_coupled(run_dir, file_bases, chk_num, varnames=['T','T'], save=False, **src_kwargs):
    output_fname=f"Coupled_scatter_chk{chk_num}"
    srcs = [ read_nektar_src(run_dir, chk_num, plot_style='scatter', file_base=fb, **src_kwargs) for fb in file_bases]
    plot_coupled_scatter(srcs,varnames,output_fpath=get_plot_path(output_fname),save=save)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    file_bases = ['bc-provider_session','diff-solver_session']
    mode     = 'animate'
    run_lbl  = 'cwipi-BCs'
    save     = False

    run_dir = get_run_root(run_lbl)
    if mode=='animate':
        chk_range=dict(chk_start=0,chk_end=100,chk_stride=1)
        animate_coupled_scatters(run_dir, file_bases, save=save, **chk_range)
    elif mode=='single':
        chk_num = 1
        plot_single_coupled(run_dir, file_bases, chk_num, save=save)
    else:
        exit(f"Mode {mode} not recognised")
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()