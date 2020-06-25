import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Annotate(object):
    def __init__(self,ax):
        #self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1, facecolor='none')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        ax.add_patch(self.rect)
        ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        print( 'press')
        self.x0 = event.xdata
        self.y0 = event.ydata

    def on_release(self, event):
        print ('release')
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        ax.figure.canvas.draw()


