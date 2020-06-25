import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import matplotlib.patches as patches
from matplotlib.widgets  import RectangleSelector

class data:
    def __init__(self,d):
        self.rawData = d
        #rawData (Dictionary) items x_pos,y_pos,z_pos,img_out1
        self.intensities = 10*np.log10(self.rawData['img_out1'] / 10)  # in dB....this needs talking through with Alan!!!
        self.xpos = self.rawData['x_pos'][0]
        self.ypos = self.rawData['y_pos'][0]
        self.zpos  = self.rawData['z_pos'][0]
        self.Rangex = [self.xpos[0] , self.xpos[-1]]
        self.Rangey = [self.ypos[0] , self.ypos[-1]]
        
    def display_segment(self):
        def line_select_callback(eclick, erelease):
            x1, y1 = eclick.xdata, eclick.ydata
            print(eclick.xdata)
            x2, y2 = erelease.xdata, erelease.ydata
            rect = plt.Rectangle( (min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2) )
            ax.add_patch(rect)


            

        fig,ax  = plt.subplots()
                 
        im = ax.imshow(self.intensities.T,  origin='lower',
                       cmap=plt.get_cmap("copper"),extent = (self.xpos[-1],self.xpos[0],self.ypos[0],self.ypos[-1]))

        fig.colorbar(im)




        rs = RectangleSelector(ax, line_select_callback,
                       drawtype='box', useblit=False, button=[1], 
                       minspanx=500, minspany=500, spancoords='pixels', 
                       interactive=True)

        plt.show()

#d = loadmat(r'../DataLabelled/sasi-20150413-181203-vrak_13c-2-SLH90-BP-000_simppackage.mat')
#d = loadmat(r'sasi-20150413-181203-vrak_13c-2-PLH90-BP-000_simppackage.mat')

SASdata = data(d)


SASdata.display_segment()