import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat



class data():
    def __init__(self,d):
        self.rawData = d
        #rawData (Dictionary) items x_pos,y_pos,z_pos,img_out1
        self.intensities = self.rawData['img_out1']
        self.xpos = self.rawData['x_pos'][0]
        self.ypos = self.rawData['y_pos'][0]
        self.zpos  = self.rawData['z_pos'][0]
        self.Rangex = [self.xpos[0] , self.xpos[-1]]
        self.Rangey = [self.ypos[0] , self.ypos[-1]]
        
    def display_segment(self):
         print (" xrange: " , self.Rangex  , " yrange: ", self.Rangey)
         print("input x_pos1,x_pos2,y_pos1,y_pos2")
         rectangle = [50,280,50,150]#input()
         

         
         fig,ax  = plt.subplots()

         inx = [ (abs(self.xpos - rectangle[0])).argmin() , 
                (abs(self.xpos  - rectangle[1])).argmin() ]

         iny = [ (abs(self.ypos - rectangle[2])).argmin() , 
                (abs(self.ypos  - rectangle[3])).argmin() ]                    
         print(inx,iny)
         im = ax.imshow(self.intensities[iny[0]:iny[1], inx[0]:inx[1]],vmin = 0 ,vmax =  5 )#np.amax(self.intensities) )
         fig.colorbar(im)
         plt.show()

d = loadmat(r'sasi-20150413-181203-vrak_13c-2-SLH90-BP-000_simppackage.mat')
#d = loadmat(r'sasi-20150413-181203-vrak_13c-2-PLH90-BP-000_simppackage.mat')

SASdata = data(d)


SASdata.display_segment()