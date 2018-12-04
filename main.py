import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy.core.defchararray as np_f


def main():
    data_dir = raw_input("Enter data directory path:  ")
    resistor = raw_input("Enter resistor value:  ")
    y_axis_max = raw_input("Enter y-axis max:  ")
    for path, subdirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(data_dir, file)
            file_name = file.split('.')[0]
            is_csv = True if file.split('.')[1] == 'csv' else False
            if is_csv:
                create_graph(file_path, resistor, y_axis_max)


def create_graph(file_path, resistor, y_axis_max):
    fig, ax = plt.subplots()

    file_name = os.path.basename(file_path).split('.')[0]
    data = np.genfromtxt(file_path, delimiter=',', dtype=str, skip_header=7)
    is_wet_test = True if data.shape[1] == 5 else False  #4 columns is for dry test, while 5 columns is for wet test
    if is_wet_test:
        data = data[:,2:] #remove first two columns (time string can't be converted to float
        data = np_f.replace(data, '"', '')  #the csv files have double quotes for some reason - these need to be removed
        data = data.astype(np.float) #convert remaining data to flaot
        sp_height = data[:,0]
        ls_volts = data[:,1]
        ps_volts = data[:,2]
        sp_height_rel = sp_height[0] - sp_height
        ls_ohms = ls_volts / ((ps_volts - ls_volts) / float(resistor))

        ax.set_xlim([0, sp_height_rel.max()])
        ax.set_ylim([0, float(y_axis_max)])
        ax.plot(sp_height_rel, ls_ohms, linewidth=0.1)
        ax.set_xlabel('Height (mm)', fontsize=7)
        ax.set_ylabel('LS Resistance (ohms)', fontsize=7)

        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(0, end, 10))

    else:  #dry test
        data = data[:, 1:]
        data = np_f.replace(data, '"', '')  # the csv files have double quotes for some reason - these need to be removed
        data = data.astype(np.float)  # convert remaining data to flaot
        ls_time = data[:, 0]
        ls_volts = data[:, 1]
        ps_volts = data[:, 2]
        ls_ohms = ls_volts / ((ps_volts - ls_volts) / float(resistor))

        ax.set_xlim([0, ls_time.max()])
        ax.set_ylim([0, float(y_axis_max)])
        ax.plot(ls_time, ls_ohms, linewidth=0.1)
        ax.set_xlabel('Time (sec)', fontsize=7)
        ax.set_ylabel('LS Resistance (ohms)', fontsize=7)

        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(0, end, 1))

    ax.tick_params(labelsize=5)
    ax.set_title(file_name, fontsize=7)
    ax.grid(linewidth=0.1)

    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(0, end, 50))

    #fig.savefig("test.png")
    #plt.show()
    make_pdf(file_path)

def make_pdf(file_path):
    pp = PdfPages(file_path.replace('.csv','.pdf'))
    pp.savefig()
    pp.close()


if __name__ == "__main__":

    #create_graph(r'C:\Data\Dry Test\MS 1_a.csv', '319.8', '300')
    #create_graph(r'C:\Data\CA2018-2882 Post IR 7.4.1 Dry Test Raw Data\MS 1_a.csv', '319.8')

    main()





