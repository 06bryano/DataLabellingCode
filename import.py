import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import matplotlib.patches as patches
from matplotlib.widgets  import RectangleSelector


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))


def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)


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


        fig,ax  = plt.subplots()
            
        #intensities  = np.zeros((100,100))
        #ax.imshow(intensities.T,  origin='lower',
        #       cmap=plt.get_cmap("copper"))#,extent = (self.xpos[-1],self.xpos[0],self.ypos[0],self.ypos[-1]))

        
                 
        ax.imshow(self.intensities.T,  origin='lower',
                       cmap=plt.get_cmap("copper"),extent = (self.xpos[-1],self.xpos[0],self.ypos[0],self.ypos[-1]))

        #fig.colorbar(im)




        toggle_selector.RS = RectangleSelector(ax,  line_select_callback,drawtype='box', useblit=True,button=[1, 3], minspanx=5, minspany=5,spancoords='pixels',interactive=True)
        plt.connect('key_press_event', toggle_selector)
        plt.show()

d = loadmat(r'../DataLabelled/sasi-20150413-181203-vrak_13c-2-SLH90-BP-000_simppackage.mat')
#d = loadmat(r'sasi-20150413-181203-vrak_13c-2-PLH90-BP-000_simppackage.mat')

SASdata = data(d)


SASdata.display_segment()