## coded by Trixi (with Manuelas & Alessandros help)
## look at distribution of fines for a given Vin (=for the time given frame) 
##  -- for those ADCs for which coarse is always the same !! --
## as 1d histogram (=> should give a first VERY ROUGH idea about noise ...)


import matplotlib
# Generate images without having a window appear:
# this prevents sending remote data to locale PC for rendering
# matplotlib.use('Agg')  # Must be before importing matplotlib.pyplot or pylab!
# Generate images with having a window appear:
# this sends remote data to locale PC for rendering
matplotlib.use('TkAgg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt  # noqa E402

from plot_base import PlotBase  # noqa E402o
import copy
import os
import numpy as np


class Plot(PlotBase):
    def __init__(self, **kwargs):  # noqa F401
        # overwrite the configured col and row indices
        new_kwargs = copy.deepcopy(kwargs)
        #new_kwargs["frame"] = None
        #new_kwargs["dims_overwritten"] = True

        super().__init__(**new_kwargs)

    def plot_sample(self):
        self.create_dir()

        title = ("Frame={}, Sample: Row={}, Col={}, ADC={}"
                 .format(self._frame, self._row, self._col, self._adc))
        out = os.path.join(self._output_dir,
                           "raw_1dHist_fine_fixedCrs_row{}_col{}_adc{}"
                           .format(self._row, self._col, self._adc))


        fig = plt.figure(figsize=None)

        cmap = matplotlib.pyplot.cm.jet
        cmap.set_under(color='white')

        ## now generate the histogram itself
        
        s_fine = self._data["s_fine"]
        s_coarse = self._data["s_coarse"]
 
        fines = s_fine.flatten()
        crses = s_coarse.flatten()

        fine_min = np.min(fines)
        fine_max = np.max(fines)

	## ascertain all crses are identical:
        no_crses = crses.shape[0]
        eq_crses = crses[crses == crses[0]]
        no_eq_crses = eq_crses.shape[0]

        print("Number of coarse values: ", no_crses)
        print("Number of equal coarse values: ", no_eq_crses)


        if (no_crses == no_eq_crses) :

            #n, bins, patches = plt.hist(s_fine.flatten(), bins=(fine_max-fine_min+1), range=[(fine_min-0.5),(fine_max+0.5)], histtype='bar')

            plt.hist(s_fine.flatten(), bins=(fine_max-fine_min+1), range=[(fine_min-0.5),(fine_max+0.5)], histtype='bar')

            fig.suptitle(title)   
            plt.xlabel("fine value")
            plt.ylabel("number of occurrences")
            
            plt.axis([0,255,0,500]

            fig.savefig(out) 

            fig.show()
            plt.show()

            input('Press enter to end')

            fig.clf()
            plt.close(fig)

        if (no_crses != no_eq_crses) :
            print("Not all coarses identical for this data set, no plot")

    def plot_reset(self):
        pass

    def plot_combined(self):
        pass
    
