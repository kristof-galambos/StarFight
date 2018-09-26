

import skimage.io as io
import os
import numpy as np

files = os.listdir('.')
imagefiles = [img for img in files if img.endswith('final.jpg')]      
              
images = []
for filename in imagefiles:
    images.append(io.imread(filename))

for img in images:
    img[:, :, (0,1)] = 255

for i, img in enumerate(images):
    io.imsave(imagefiles[i][:-4]+'_selected.jpg', img)
    
    
    
    
    
    
############################## same thing again now with .png-s
#files = os.listdir('.')
#imagefiles = [img for img in files if img.endswith('final.png')]      
#              
#images = []
#for filename in imagefiles:
#    images.append(io.imread(filename))
#
#for img in images:
#    img[:, :, (0,1)] = 0
#
#for i, img in enumerate(images):
#    io.imsave(imagefiles[i][:-4]+'_selected.png', img)