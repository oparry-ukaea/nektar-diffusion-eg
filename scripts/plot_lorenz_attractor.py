import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

from gen_lorenz_data import default_params, gen_timesteps_and_data

#--------------------------------------------------------------------------------------------------
def get_lorenz_data_as_lists(dt_mode,params=default_params):
    data = gen_timesteps_and_data(dt_mode,params=params)
    x=[]
    y=[]
    z=[]
    for t in data:
        x.append(t[0])
        y.append(t[1])
        z.append(t[2])
    return x,y,z
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def plot_lorenz_attractor(dt_mode='dirk3', params=default_params):
    x,y,z = get_lorenz_data_as_lists(dt_mode,params=params)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot(x, y, z)

    plt.show(block=True)
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    plot_lorenz_attractor(dt_mode='uniform')