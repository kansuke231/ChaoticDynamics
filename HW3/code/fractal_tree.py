from __future__ import division
import cairocffi as cairo
from contextlib import contextmanager
import math
import random

@contextmanager
def saved(cr):
    cr.save()
    try:
        yield cr
    finally:
        cr.restore()

def Tree(angle,depth):
    cr.move_to(0, 0)
    cr.translate(0, -150)
    cr.line_to(0, 0)
    cr.stroke()
    cr.scale(0.6, 0.6)
    
    if depth > 1:#angle > 0.12:
        for a in [-angle, angle]:
            with saved(cr):
                cr.rotate(a)
                Tree(angle,depth-1)
    
def Tree_multiple_args(angles,depth,scale):
    cr.move_to(0, 0)
    cr.translate(0, -150)
    cr.line_to(0, 0)
    cr.stroke()
    cr.scale(scale, scale)
    
    if depth > 1:#angle > 0.12:
        for a in angles:
            with saved(cr):
                cr.rotate(a)
                if a > 0: # right side
                    Tree_multiple_args(angles,depth-1,scale=0.725)
                else: # left side
                    Tree_multiple_args(angles,depth-1,scale=0.675)


surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 580, 480)
cr = cairo.Context(surf)
cr.translate(280, 440)
cr.set_line_width(10)
Tree_multiple_args([-math.pi*1/2.5, math.pi*1/9],depth=15,scale=0.62)
angle_random = lambda: random.uniform(math.pi/6, math.pi/2)
scale_random = lambda: random.uniform(0.55, 0.8)

#Tree_multiple_args([-angle_random(), angle_random()],depth=15,scale=scale_random())

surf.write_to_png('fractal-tree.png')

