# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:33:20 2018

@author: franz
"""

from walker import triangular_walker
import numpy as np
import sys

#if len(sys.argv) < 2:
#    exit()

length = 0
runs_per_length = 500


weights = []
with open("test.txt", "w") as file:
    while length < 250:
        count = 0
        while count < runs_per_length:
            walker = triangular_walker(np.zeros((2)), self_avoiding=True)
            try:
                for foo in range(length):
                    walker.walk()
            except IndexError:          
                continue
                
            file.write(str(length) + " " + str(np.linalg.norm(walker.position_coordinates(walker.pos))) + " " + str(walker.W) + "\n")      
            count += 1
        length += 1
        
