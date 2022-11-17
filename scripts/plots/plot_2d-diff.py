from utils import animate_2d_field, get_plot_path, get_run_root, plot_2d_field, read_nektar_src, read_all_nektar_srcs

#--------------------------------------------------------------------------------------------------
def plot_single_chk(run_dir, chk_num, varname='T',save=False):
    output_fname=f"T_scatter_chk{chk_num}"
    src = read_nektar_src(run_dir, chk_num, plot_style='scatter')
    plot_2d_field(src,varname,output_fpath=get_plot_path(output_fname),save=save)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def animate(run_dir, output_fname='tmp.mp4', varname='T',save=False, **other_kwargs):
    srcs = read_all_nektar_srcs(run_dir, plot_style="scatter", **other_kwargs)
    animate_2d_field(srcs,varname,output_fpath=get_plot_path(output_fname),save=save)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    mode     = 'animate'
    #mode     = 'single'
    template = '2d-diff'
    save     = False

    run_dir = get_run_root(template)
    if mode=='animate':
        chk_range=dict(chk_start=19,chk_end=99,chk_stride=10)
        animate(run_dir, output_fname='2d-diff.mp4', varname='T',save=save, **chk_range)
    elif mode=='single':
        chk_num = 100
        plot_single_chk(run_dir, chk_num, varname='T', save=save)
    else:
        exit(f"Mode {mode} not recognised")
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()