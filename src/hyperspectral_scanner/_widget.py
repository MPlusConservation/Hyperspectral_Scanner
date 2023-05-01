"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
from napari.qt import thread_worker
from PIL import Image, ImageOps
import time
import numpy as np

if TYPE_CHECKING:
    import napari


tsr = Image.open("/Users/homelyp/Desktop/ghos.tif")

width, height = tsr.size #X and Y image dimensions
#chose desired image width, for example, a width of 200 should be used if you have a slow machine
X_dim = width #chose "width" if you want to use the whole image
Y_dim = height #int(height*(X_dim/width)) #maintain aspect ration as original image

#get the data into a numpy array
images = []
for i in range(tsr.n_frames):
    tsr.seek(i)
    images.append(np.array(ImageOps.fit(tsr, (X_dim,Y_dim), Image.LANCZOS), dtype=np.float32)/ 255 ) 

scan = np.zeros((493,676,3))#initial blank image for display in Napari.
#Spatial dimensionsis 676 (in this example). This should be a fixed value for the spectral camera. 
#493 is the number of images collected. 3 is the 3-channel RGB dimension


@thread_worker

def collect_scan(layer, interval=0.05):
    update_scan = np.zeros((493,676,3)) #numpy array where color data is added for display in Napari 
      
    for i in range(492): #for loop takes one through the entire scan range
         #images = camera.capture() #capture with Asi ZWO camera. Output is a numpy array.
        
        buffer=np.zeros((1,676,3)) #Buffer to hold sudo-color image for single scan line
        buffer[:,:,0] = images[i][120] #red
        buffer[:,:,1] = images[i][90] #green
        buffer[:,:,2] = images[i][60] #blue
         
         
        update_scan[i] = buffer #add sudo-color scan line to update array
        layer.data = update_scan #update layer in Napari so one can visualize scan
        yield
        time.sleep(interval)
    
with napari.gui_qt():
    v = napari.Viewer()#(show=False)
      #v.window._qt_window.setWindowState(Qt.WindowMaximized)
      # #v.show()
      # image_layer = v.add_image(scan)
      # worker = collect_scan(image_layer)
      # #worker.start()
    button = QPushButton("Start Scan")
    button.clicked.connect(worker.start)
    v.window.add_dock_widget(widget=button, area='right')



