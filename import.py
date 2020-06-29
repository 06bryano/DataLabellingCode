import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import matplotlib.patches as patches
from matplotlib.widgets  import RectangleSelector
from tkinter import *



#e = Entry(master)
#e.pack()
#e.focus_set()
class GUI:
    def __init__(self):
        self.ObjClassList = ["bomb","shell","debris"]
    def ObjChoiceCallback(self,window, ObjClass):
        #print (e.get() )# This is the text you may want to use later
        print("ObjClass: ", ObjClass)
        #b.configure(state=DISABLED)
        #window.destroy()

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    print(" The button you used were: %s %s" % (eclick.button, erelease.button))
    return x1,y1,x2,y2


def toggle_selector(event):

    if event.key in ['enter'] and toggle_selector.RS.active:
        print("rectangle accepted")
        print(toggle_selector.RS.corners)
        corners = toggle_selector.RS.corners
        SASdata.ax.add_patch( patches.Rectangle((corners[0][1], corners[1][0]),
                                                corners[0][0]-corners[0][1],
                                                corners[1][2]-corners[1][0],
                                                fill=False))
        plt.show()
        plt.pause(0.01)
        print("please select one of the options", SASdata.targetClasses )



        window = Tk() # make window
        for ObjClass in myGUI.ObjClassList:
            print(ObjClass)
            Button(window, text = ObjClass, width = 10, command =  lambda ObjClass = ObjClass: myGUI.ObjChoiceCallback(window, ObjClass)).pack()
        #for certainty in myGUI.CertaintyList:
        #    Button(window, text = certainty, width = 10, command =  lambda: myGUI.ObjChoiceCallback(window, certainty)).pack()
                
            
        window.mainloop()

        

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
        self.targetClasses = ["Munition","Debris (man made)","Natural","unknown"]
   

    def display_segment(self):


        fig,self.ax  = plt.subplots()
               
        im = self.ax.imshow(self.intensities.T,  origin='lower',
                       cmap=plt.get_cmap("copper"),
                       extent = (self.xpos[-1],self.xpos[0],self.ypos[0],self.ypos[-1]),
                       vmin = -40,
                       vmax = 0)

        fig.colorbar(im)
        toggle_selector.RS = RectangleSelector(self.ax,  line_select_callback,drawtype='box', useblit=True,button=[1, 3], minspanx=5, minspany=5,spancoords='pixels',interactive=True)
        plt.connect('key_press_event', toggle_selector)
        plt.show()

d = loadmat(r'../DataLabelled/sasi-20150413-181203-vrak_13c-2-SLH90-BP-000_simppackage.mat')
#d = loadmat(r'sasi-20150413-181203-vrak_13c-2-PLH90-BP-000_simppackage.mat')

SASdata = data(d)
myGUI = GUI()

SASdata.display_segment()