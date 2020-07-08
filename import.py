import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import matplotlib.patches as patches
from matplotlib.widgets  import RectangleSelector
import matplotlib as mpl
from tkinter import *
import json
from datetime import date



#e = Entry(master)
#e.pack()
#e.focus_set()
class GUI:
    def __init__(self, Datafilename, labelsTXTfile):
        self.ObjClassList = ["105mm_Shell","150mm_Shell","KC50","KC250","KC500","Drum","Can","Crate","Grenade","Debris_(man_made)","Natural"]
        self.obj = []
        self.Datafilename = Datafilename
        self.labelsTXTfile = labelsTXTfile
        self.user ="Oscar Bryan"
    def ObjChoiceCallback(self,window, ObjClass,buttons,T):
        self.obj.append(ObjClass)
        #disable button once pressed
        for b in buttons:
            if b.cget('text') == ObjClass:
                b.configure(state=DISABLED)
        T.insert(END,ObjClass + ",")

    def OKCallback(self,window,corners,labelsTXTfile):
        print("save", self.obj, len(self.obj))
        #f = open(self.labelsTXTfile , "a") # "a" create a new file if the specified file doesnt exists        
        #f.close()
        
        Label_dic = {"Datafilename":self.Datafilename,
                     "objects":self.obj,
                     "uncertainty":len(self.obj),
                     "corners":corners,
                     "Date": date.today().strftime('%m/%d/%Y'),
                     "User":self.user}
        
        with open('data.txt', 'a') as outfile:
            json.dump(Label_dic, outfile)
        self.obj = []
        window.destroy()
        

        

def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    #print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    #print(" The button you used were: %s %s" % (eclick.button, erelease.button))

    return x1,y1,x2,y2


def toggle_selector(event):
    
    #if event.key in ['enter'] and toggle_selector.RS.active:

    
    if event.key in ['enter'] and toggle_selector.RS.active:
        print("rectangle accepted")
        corners = toggle_selector.RS.corners
        
        #draw bounding box on figure
        SASdata.ax.add_patch( patches.Rectangle((corners[0][1], corners[1][0]),
                                                corners[0][0]-corners[0][1],
                                                corners[1][2]-corners[1][0],
                                                fill=False))
        
        # add labels for size of box
        #y
        SASdata.ax.text(corners[0][0],corners[1][0] + (corners[1][2] - corners[1][0])/2,
                        str(np.around(corners[1][2]-corners[1][0],1)),
                        fontsize=(10))
        #x
        SASdata.ax.text(corners[0][0] + (corners[0][1] - corners[0][0])/2, corners[1][0],
                str(np.around(corners[0][1]-corners[0][0],1)),
                fontsize=(10))
        
        
        plt.show()
        plt.pause(0.01)



        window = Tk() # make window
        T = Text(window, width=35,height = 3)
        T.grid(row = 0,columnspan = 2)
        buttons = []
        for row , ObjClass in enumerate(myGUI.ObjClassList):
            buttons.append(  Button(window, text = ObjClass, width = 20, command =  lambda ObjClass = ObjClass: myGUI.ObjChoiceCallback(window, ObjClass, buttons,T))  )
            buttons[row].grid(row = row+1,column = 0)
        Button(window, text = "OK", width = 20, command =  lambda: myGUI.OKCallback(window, corners, labelsTXTfile)).grid(row = int(row/2),column = 1)
        window.mainloop()

        

class data:
    def __init__(self,d, labelsTXTfile):
        self.rawData = d
        #rawData (Dictionary) items x_pos,y_pos,z_pos,img_out1
        self.intensities = 10*np.log10(self.rawData['img_out1'] )#/ np.mean(self.rawData['img_out1']))  # in dB....this needs talking through with Alan!!!
        self.xpos = self.rawData['x_pos'][0]
        self.ypos = self.rawData['y_pos'][0]
        self.zpos  = self.rawData['z_pos'][0]
        self.Rangex = [self.xpos[0] , self.xpos[-1]]
        self.Rangey = [self.ypos[0] , self.ypos[-1]]
        self.labelsTXTfile = labelsTXTfile
        

    def display_segment(self):


        
        fig,self.ax  = plt.subplots()       
        im = self.ax.imshow(self.intensities.T,  origin='lower',
                       cmap=plt.get_cmap("copper"),
                       extent = (self.xpos[-1],self.xpos[0],self.ypos[0],self.ypos[-1]),
                       vmin = -20,
                       vmax = 0)

        fig.colorbar(im)
        toggle_selector.RS = RectangleSelector(self.ax,  line_select_callback,drawtype='box', useblit=True,button=[1, 3], minspanx=5, minspany=5,spancoords='pixels',interactive=True)
        plt.connect('key_press_event', toggle_selector)
        plt.show()
        
    def displayLabels(self, Datafilename):
        #read txt file
        f = open(self.labelsTXTfile)
        lines = f.readlines() # lines is a list containing all lines in the file
        
        cmap = plt.cm.Paired
        norm = mpl.colors.Normalize(vmin = 0 ,vmax = len(myGUI.ObjClassList))
        self.uncertainty_stat = np.zeros(len(myGUI.ObjClassList))
        self.class_stat = np.zeros(len(myGUI.ObjClassList))
        
        
        for line in lines:
            sections = line.split("~")
            if sections[0] == Datafilename:

                labels = sections[1].strip('][').replace("'","").split(',')

                c = myGUI.ObjClassList.index(labels[0])
                
                corners = np.array(sections[3].replace('(','').replace(')','').split(','),dtype = float)
                self.ax.add_patch( patches.Rectangle((corners[1], corners[4]),
                                        corners[0]-corners[1],
                                        corners[6]-corners[4],
                                        fill=False, color = cmap(norm(c))))
                self.uncertainty_stat[int(sections[2])] += 1
                self.class_stat[c] += 1

        f.close()
        
    def plotLabelStats(self):
        fig2,ax2 = plt.subplots(2)
        ax2[0].bar(range(len(myGUI.ObjClassList)), self.uncertainty_stat)
        ax2[0].set_xlabel("uncertainty")
        ax2[1].bar(myGUI.ObjClassList, self.class_stat)
            
            
            


Datafilename = "sasi-20150413-181203-vrak_13c-2-SLH90-BP-000_simppackage.mat"
#Datafilename = "sasi-20150413-181203-vrak_13c-2-PLH90-BP-000_simppackage.mat"
d = loadmat(r'../DataLabelled/' + Datafilename)

labelsTXTfile = "demolabelfile.txt"

myGUI = GUI(Datafilename, labelsTXTfile)

SASdata = data(d, labelsTXTfile)
SASdata.display_segment()
#SASdata.displayLabels(Datafilename) # Datafilename is data .mat file 
#SASdata.plotLabelStats()



