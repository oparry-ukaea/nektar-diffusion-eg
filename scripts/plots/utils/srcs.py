from NekPlot.data import get_source
from .plotting import get_plot_style

#--------------------------------------------------------------------------------------------------
def read_all_nektar_srcs(run_dir, chk_start=0,chk_end=99,chk_stride=1,compute_gradients=False):
    data_srcs = []
    for chk_num in range(chk_start,chk_end+chk_stride,chk_stride):
        nek_src = get_source("nektar", run_dir, chk_num=chk_num, label=f"Checkpoint {chk_num}")
        if compute_gradients:
            nek_src.add_gradients()
        nek_src.set_plot_kws(get_plot_style("points"))
        data_srcs.append(nek_src)
    return data_srcs
#--------------------------------------------------------------------------------------------------