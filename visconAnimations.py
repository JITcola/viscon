#tkinterless combined both functions
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import cm
import matplotlib.pylab as pl
from mpl_toolkits import mplot3d
import numpy as np
#frames are saved into python folder, also gives html thing to click through frames
#can also add save as gif functionality 

#solutions
#pole_list = [(-1.0, 0.0), (-0.987729789565432, 0.000617330877333616), (-0.939341655091005, 0.00313110406064478), (-0.830507342443404, 0.00934202540200167),
#(-0.620668822927015, 0.0247871567192033),  (-0.411171421887903, 0.0506787652729613), (-0.274330984357952, 0.0849298515150158),  (-0.193030382290651, 0.126768853979979),
#(-0.145271656681636, 0.173648817797028), (-0.114645541270073, 0.226371773417126), (-0.0931257416093585, 0.288464672926832),  (-0.0773600312913075, 0.364063122829046),
#(-0.0658471224792382, 0.457481421348396), (-0.0579148211683786, 0.57092538995081),  (-0.0530134646702375, 0.703924794396626), (-0.0506373109266826, 0.844760979860435),
#(-0.0500084726262976, 0.946879855975817),  (-0.0499390419213899, 0.991226295519007), (-0.0499377718370024, 1.00124611412781)]
             
#static poles
#static_pole_list = [(0,0),(-0.3594531922483898, -0.02405539865420558), (-0.4708651352879495, -0.02111214394471321), (-0.5573779725615259, -0.014872714076942985),
#(-0.6231275759288948, 0.007390754541543879), (-0.5054342977255696, 0.010088670601496907),(-0.36349633145565674, 0.0363904865598826), (-0.25551053223271547, 0.0709151940754952),
#(-0.18768955460189496, 0.1126219302845108), (-0.1485661688716431, 0.15949509952492663), (-0.1262502798372135, 0.21226788430484553),(-0.1153001429287574, 0.2744864815709789),
#(-0.11481691623914135, 0.3499089801944293), (-0.12631167622465236, 0.44308332091751085), (-0.15452628732576817, 0.5562719977260787),(-0.2063932149609995, 0.6895555514828402),
#(-0.251833702802448, 0.851110052760733), (-0.444838693784351, 0.9285279123662147), (-0.5810939406694652, 0.9690161428947379)]

#stepsizes 
#stepsize_list = [0.1, 0.1, 0.1, 0.1, 0.05808407977353812, 0.024885081657016302, 0.011732647200711172, 0.007560752119438813, 0.007266043481429952, 0.00913221831352027,
#0.013106238089690334, 0.020020976397995313, 0.03107759464489642, 0.048858206313710066, 0.07702568230981807, 0.1, 0.1, 0.1, 0.09125047969823508]

#color values
#colorvals = sorted(stepsize_list)

#list for polygonalcurve
#inputlist = [[(-2, 2), (2, 2), (5, -1), (5, -3)], [(-2, 2), (1, -1), (3, 1), (4, 3)], [(-4, -3), ( -3, -1), (-2, -1), (-1, -3)]]

def animation_2d_original(pole_list, static_pole_list, xlabel, ylabel):
    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    x_val = [x[0] for x in pole_list]
    y_val = [x[1] for x in pole_list]
    x_val_static = [x[0] for x in static_pole_list]
    y_val_static = [x[1] for x in static_pole_list]
    scatterplot = ax.scatter(x_val, y_val)
    staticplot = ax.scatter(x_val_static, y_val_static)

    def animate_2d_1(i, x_val, y_val):
        scatterplot.set_offsets((x_val[i], y_val[i]))
        ax.scatter(x_val[i], y_val[i], color = 'm')
        return scatterplot,

    def animate_2d_2(i, x_val_static, y_val_static):
        staticplot.set_offsets((x_val_static[i], y_val_static[i]))
        ax.scatter(x_val_static[i], y_val_static[i], color = 'g')
        return staticplot,

    animate = animation.FuncAnimation(fig, animate_2d_1, fargs = (x_val, y_val), repeat = True, interval = 200,  blit = False)
    animate2 = animation.FuncAnimation(fig, animate_2d_2, fargs = (x_val_static, y_val_static), repeat = True, interval = 200,  blit = False)
    plt.show()

def animation_2d_static(pole_list, static_pole_list, filename, xlabel, ylabel): #currently throws a list index error but works, check length of input lists 
    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    x_val = [x[0] for x in pole_list]
    y_val = [x[1] for x in pole_list]
    x_val_static = [x[0] for x in static_pole_list]
    y_val_static = [x[1] for x in static_pole_list]
    scatterplot = ax.scatter(x_val, y_val)
    staticplot = ax.scatter(x_val_static, y_val_static)

    def animate_2d_1(i, x_val, y_val, x_val_static, y_val_static):
        scatterplot.set_offsets((x_val[i], y_val[i]))
        ax.scatter(x_val[i], y_val[i], color = 'm')
        staticplot.set_offsets((x_val_static[i], y_val_static[i]))
        ax.scatter(x_val_static[i-1], y_val_static[i], color = 'g')
        return scatterplot,staticplot

    animate = animation.FuncAnimation(fig, animate_2d_1, fargs = (x_val, y_val, x_val_static, y_val_static), repeat = False, interval = 200,  blit = False)
    animate.save(filename+".html")
    
def animation_3d(pole_list, stepsize_list, colorvals, filename, xlabel, ylabel, zlabel, colorbarlabel):
    colorvals = set(colorvals)
    colorvals = list(colorvals) #ugly 
    colorvals.sort() #hacky way to make colormap work for big data
    fig = plt.figure(figsize =(9, 6))
    ax = fig.gca(projection = '3d')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    x_val = [x[0] for x in pole_list]
    y_val = [x[1] for x in pole_list]
    colors = pl.cm.hsv(np.linspace(0, 1, len(colorvals)))
    lines = [[]]
    for i in range(len(x_val)-1):
        colori = colorvals.index(stepsize_list[i])
        lineplot, = ax.plot([x_val[i], x_val[i+1]], [y_val[i], y_val[i+1]], [stepsize_list[i], stepsize_list[i+1]], color=colors[colori])
        lines.append(lines[-1] + [lineplot])
    img = plt.cm.ScalarMappable(cmap="hsv")#dummy image to make colorbar
    img.set_array([])
    cbar = plt.colorbar(img, ticks = [0, 1])
    cbar.ax.set_yticklabels(['smaller', 'larger'])
    cbar.set_label(colorbarlabel)    
    animate = animation.ArtistAnimation(fig, lines, interval = 300)
    plt.show() #this one works but for consistencys sake 
    animate.save(filename+".html")

def plotpolygonalcurve(inputlist, xlabel, ylabel, filename):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    colors = pl.cm.hsv(np.linspace(0, 1, len(inputlist)+1))
    for i in range(len(inputlist)):
        plotlist = inputlist[i]
        x_vals = [x[0] for x in plotlist]
        y_vals = [x[1] for x in plotlist]
        line = ax.plot(x_vals, y_vals, color = colors[i], marker = 'o', label = "solution" + str(i+1))
    ax.legend()
    plt.savefig(filename+'png')
    plt.show()


def main():
    print("Welcome to my visualizer")
    userin = input("Would you like to produce an animated 2d plot, list of 2d frames, a polygonal curve, or a 3d visualization set? 2da/2ds/poly/3d ")
    xlabel = input("What would you like to call your x axis label? " )
    ylabel = input("What would you like to call your y axis label? ")
    if userin == '2da':
        animation_2d_original(pole_list, static_pole_list, xlabel, ylabel)
    elif userin == '2ds':
        filename = input("What would you like to call your file? ")
        animation_2d_static(pole_list, static_pole_list, filename, xlabel, ylabel)
    elif userin == 'poly':
        filename = input("What would you like to call your file? ")
        plotpolygonalcurve(inputlist, xlabel, ylabel, filename)
    elif userin == '3d':
        zlabel = input("What would you like to call your additional z axis label? ")
        colorbarlabel = input("What would you like to call your colorbar? ")
        filename = input("What would you like to call your file? ")
        animation_3d(pole_list,stepsize_list,colorvals, filename, xlabel, ylabel, zlabel, colorbarlabel)
    else:
        print("invalid input!")

#main()
                    
