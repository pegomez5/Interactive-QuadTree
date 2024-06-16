# -*- coding: utf-8 -*-
import matplotlib.lines as mlines
import math
import random


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __str__(self):
        return "X: {}, Y: {}".format(self.x, self.y)

"""
@Function: Generate a random set of points in the format [[x,y], ...]
@Params: num_points: Number of points to gen
         radius: radius???
@Returns: List of points
"""
def generatePointsInRadius(num_points: int, radius: float):
    points = []
    
    for _ in range(num_points):
        # Generate random angle
        angle = random.uniform(0, 2*math.pi)
        
        # Generate random radius
        r = radius * (math.sqrt(random.uniform(0, 1)))
        
        # Convert polar coordinates to Cartesian coordinates
        x = 2.5 + (r * math.cos(angle))
        y = 2.5 + (r * math.sin(angle))
        
        points.append([x, y])
    return points
        
class QuadTree:
    """ 
    @Function: Initialize quadtree
    
    @Params: BL: Bottom left point
             TR: Top right points
             capacity: self explanatory. Default=1
    """
    def __init__(self, BL: Point, TR: Point, capacity: int = 1):
        self.BL = BL 
        self.TR = TR
        self.Capacity = capacity
        self.Points = []
        self.Lines  = []
        
        self.NWTree = None
        self.NETree = None
        self.SWTree = None
        self.SETree = None
        
    """
    @Function: Split current QT tree into 4 more, store new subdivision lines, 
               and reinsert the points as needed
    """
    def subdivide(self):
        bl, tr = self.BL, self.TR
        # Initialize points needed for new quads
        bl1, tr1 = Point(bl.x, (tr.y + bl.y)/2), Point((bl.x + tr.x)/2, tr.y)
        bl2      = Point((bl.x + tr.x)/2, (tr.y + bl.y)/2)
        bl4, tr4 = Point((bl.x + tr.x)/2, bl.y), Point(tr.x, (tr.y + bl.y)/2)
        
        # Create a new QuadTree for each direction (NW/NE/SW/SE)
        # eg. self.NWTree = QuadTree(self.TL, midPoint)
        self.NWTree = QuadTree(bl1, tr1, self.Capacity)
        self.NETree = QuadTree(bl2, tr, self.Capacity)
        self.SWTree = QuadTree(bl, bl2, self.Capacity)
        self.SETree = QuadTree(bl4, tr4, self.Capacity)
        
        # Reinsert existing points into one of the new quads
        for p in self.Points:
            self.NWTree.insert(p)
            self.NETree.insert(p)
            self.SWTree.insert(p)
            self.SETree.insert(p)
        
        # Add new lines to lines list, and return
        line1 = mlines.Line2D([bl1.x, tr4.x], [bl1.y, tr4.y], color='purple')
        line2 = mlines.Line2D([bl4.x, tr1.x], [bl4.y, tr1.y], color='purple')
        self.Lines.append(line1)
        self.Lines.append(line2)
        
    """
    @Function: Insert point into quad if under capacity, else, subdivide and 
               insert point to one of the new children
    @Params: pt: Point to insert
    @Returns: True if successfuly inserted, false otherwise
    """
    def insert(self, pt: Point):
        # Given a point to insert into the quad tree
        
        # Check if points is within bounds, if not return false (insertion unsuccessful)
        if not self.isInBounds(pt):
            return False
        
        # Check if the quadtree is at capacity, if not then we can insert and 
        # return true (insertion successful)
        if len(self.Points) < self.Capacity and not self.NWTree:
            self.Points.append(pt)
            return True
        
        
        # If not subdivided, create new quadtree using points within each quads 
        # bounds
        if not self.NWTree:
            self.subdivide()
        
        if self.NWTree.insert(pt): return True
        if self.NETree.insert(pt): return True
        if self.SWTree.insert(pt): return True
        if self.SETree.insert(pt): return True
        
        print("Unknown error: point couldn't be inserted")
        return False
        
    """
    @Function: Check if a given point is within the quads boundaries.
    @Params: pt: Point to validate
    @Retursn: True if in bounds else false
    """
    def isInBounds(self, pt: Point):
        #print("x: ", pt.x, "\ny: ", pt.y)
        #print("Bounds: {},{}\t{},{}".format(self.BL.x, self.TR.x, self.BL.y, self.TR.y))
        
        return (self.BL.x <= pt.x <= self.TR.x and 
                self.BL.y <= pt.y <= self.TR.y)
    
    """
    @Function: Recursively check children for subdivision lines
    @Returns: A list of all found subd. lines
    """
    def get_all_lines(self):
        lines = self.Lines.copy()
        if self.NWTree:
            lines.extend(self.NWTree.get_all_lines())
            lines.extend(self.NETree.get_all_lines())
            lines.extend(self.SWTree.get_all_lines())
            lines.extend(self.SETree.get_all_lines())
        return lines
