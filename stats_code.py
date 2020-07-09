# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:35:58 2020

@author: ozzyb
"""

class DataStats():
    def __init__():
        self.ObjClassList = ["105mm_Shell","150mm_Shell","KC50","KC250","KC500","Drum","Can","Crate","Grenade","Debris_(man_made)","Natural","UNKNOWN"]

    
        
    def loadLabels(self):
        cf_Matrix = np.zeros((len(self.ObjClassList), len(self.ObjClassList)))
        
        with open(self.labelsTXTfile, 'r', encoding='utf-8') as f:
            for line in f:
                labelObj = json.loads(line.rstrip('\n|\r'))
                if labelObj['Datafilename']==Datafilename:
                    
                    c = myGUI.ObjClassList.index( labelObj['objects'][0])
                    
                    self.ax.add_patch( patches.Rectangle((labelObj['corners'][0][1], labelObj['corners'][1][0]),
                       labelObj['corners'][0][0]-labelObj['corners'][0][1],
                       labelObj['corners'][1][2]-labelObj['corners'][1][0],
                       fill=False, color = cmap(norm(c))))
                    self.uncertainty_stat[labelObj['uncertainty']] += 1
                    self.class_stat[c] += 1
