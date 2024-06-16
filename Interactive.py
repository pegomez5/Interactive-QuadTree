#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 18:21:54 2024

@author: kaaotic
"""
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from QuadTree import *


def updatePlot(ix=None, iy=None):
    if ix and iy:
        points.append([ix, iy])
        qt.insert(Point(ix, iy))
    
    # Update the scatter plot
    ax.cla()  # Clear the existing plot
    ax.scatter([p[0] for p in points], [p[1] for p in points])  # Plot updated points
    
    lines = qt.get_all_lines()
    for line in lines:
        ax.add_line(line)
        
    ax.set_ylim(0, 5)
    ax.set_xlim(0, 5)
    plt.title("Interactive Points Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.draw()  # Redraw the plot

"""
@Function: A callback function to execute on 'button_press_event'
"""
def onclick(event):
    if event.inaxes is not None:
        # Get the x and y coordinates where the click occurred
        ix, iy = event.xdata, event.ydata
        print(f"Adding point ({ix}, {iy})\n")
        
        updatePlot(ix, iy)


if __name__ == "__main__":
    fig, ax = plt.subplots()
    qt      = QuadTree(Point(0, 0), Point(5, 5))
    points  = generatePointsInRadius(25, .5)
    #points  = []

    for p in points:
        qt.insert(Point(p[0], p[1]))

    updatePlot()

    # Connect the click event to the onclick function
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()