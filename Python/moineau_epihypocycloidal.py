# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 16:53:38 2020

@author: AdamFerrick

Requires ezdxf instead of sdxf.
"""

import ezdxf
#import matplotlib.pyplot as plt
import math
import numpy as np


# Create a new DXF document.
doc = ezdxf.new(dxfversion='R2018')


# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.new(name='TEXT', dxfattribs={'color': 2})
doc.layers.new(name='ROTOR',dxfattribs={'color': 1})
doc.layers.new(name='STATOR',dxfattribs={'color': 5})

msp = doc.modelspace()

'''
Functions for epicycloid
'''

def xepi(t,lobes): 
    r = 1
    R = lobes*2
    return (R+r)*math.cos(t)-r*math.cos((R+r)/r*t)

def yepi(t,lobes):
    r = 1
    R = lobes*2
    return (R+r)*math.sin(t)-r*math.sin((R+r)/r*t)

'''
Functions hypocycloid
'''

def xhypo(t,lobes):
    r = 1
    R = lobes*2
    return (R-r)*math.cos(t)+r*math.cos((R-r)/r*t)

def yhypo(t,lobes):
    r = 1
    R = lobes*2
    return (R-r)*math.sin(t)-r*math.sin((R-r)/r*t)

'''
Moineau curve generator function. Takes input of angle and number of lobes you want for your rotor/stator
'''

def epihypo(t,lobes):
    nums = np.arange(0,2*math.pi,2*math.pi/(2*lobes)) 
    #Numpy list of epi/hypo intervals i.e. 0 to pi/3, pi/3 to 2pi/3 etc, divided based on number of lobes
    pos = list(t<nums) #Gives list of True/False/1/0 based on where t falls in the intervals
    if True in pos: #If t<some item in the nums list, if not then it's between the last item and 2pi
        if pos.index(True)%2 != 0 or t == 0: #If the first True is odd (i.e. pos 1 or 2nd item) or if t = 0
            return [xhypo(t,lobes), yhypo(t,lobes)]
        else: #If index is even
            return [xepi(t,lobes), yepi(t,lobes)]
    else: #If between last index and 2pi
        return [xepi(t,lobes), yepi(t,lobes)]

def dxfgen(x,y,layer): #Run this in console to make a dxf of your generated rotor/stator
    startx = x[0]
    starty = y[0]
    for pointx,pointy in zip(x,y):
        msp.add_line((startx,starty),(pointx,pointy),dxfattribs={'layer': layer})
        startx, starty = pointx, pointy

    doc.saveas(layer + '_'+str(lobes)+'_lobes'+'.dxf')

#Choose your number of lobes and step size
lobes = 3
step = 100
q = 2*math.pi/step
x,y = [], []
for i in range(step+1):
    x.append(epihypo(q*i,lobes)[0])
    y.append(epihypo(q*i,lobes)[1])
#plt.scatter(x,y)
#plt.show()
