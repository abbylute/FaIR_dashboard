#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 11:30:09 2025

Create color palette for scenarios in the warming dashboard

Takes a list of hex colors, coolors is a good starting point for this.
Then 'steps' indicates the number of colors you want.
Generates a new palette from the original hex colors with the new number.

@author: abbylute
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors
import pandas as pd

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

def create_continuous_palette(hex_colors, steps):
    rgb_colors = [hex_to_rgb(hex_color) for hex_color in hex_colors]
    cmap = LinearSegmentedColormap.from_list("custom_cmap", rgb_colors, N=steps)
    return cmap

def display_palette(cmap, steps):
    gradient = np.linspace(0, 1, steps)
    plt.imshow(np.vstack([gradient, gradient]), aspect='auto', cmap=cmap)
    plt.yticks([])
    plt.xlabel("Color progression")
    plt.show()

def get_hex_colors_from_cmap(cmap, num_colors):
  """
  Extracts a list of hex color values from a matplotlib LinearSegmentedColormap.

  Args:
    cmap: The LinearSegmentedColormap object.
    num_colors: The number of colors to extract.

  Returns:
    A list of hex color strings.
  """
  colors_rgba = cmap(np.linspace(0, 1, num_colors))
  colors_hex = [matplotlib.colors.rgb2hex(rgba) for rgba in colors_rgba]
  return colors_hex


# original colors from: https://coolors.co/001219-005f73-0a9396-94d2bd-e9d8a6-ee9b00-ca6702-bb3e03-ae2012-751a1d
hex_colors = ["#001219", "#005F73", "#0A9396", "#94D2BD", "#E9D8A6", "#EE9B00", "#CA6702", "#BB3E03", "#AE2012", "#751A1D"]
steps = 14

# create a new palette with desired number of colors
palette = create_continuous_palette(hex_colors, steps)

# see what it looks like
display_palette(palette, steps)

# get the hex values for the new palette
hex_colors = get_hex_colors_from_cmap(palette, steps)
print(hex_colors)


data_dir =  "/Users/abbylute/Documents/FaIR/FaIR_dashboard_data/"
dfmed = pd.read_csv(data_dir + "fair_warming_scenario_medians.csv")
# sort scenarios by warming in 2100 to assign colors:
dfmed[dfmed['year']==2100].sort_values('warming')


### TRY OUT TAB20 INSTEAD
cmap = matplotlib.colormaps['tab20']
cols = get_hex_colors_from_cmap(matplotlib.colormaps['tab20'],20)

display_palette(cmap,20)

reordered_cmap_list = [cols[6],cols[7],cols[12],cols[13],cols[2],cols[3],
                       cols[16],cols[17],cols[4],cols[5],cols[0],cols[1],
                       cols[18],cols[19],cols[14],cols[15],cols[10],cols[11],
                       cols[8],cols[9]]

# ok reordering of 20 item color list:
reordered_cmap_list = [cols[6],cols[7],cols[12],cols[13],cols[2],cols[3],
                       cols[16],cols[17],cols[4],cols[5],
                       cols[14],cols[15],
                       cols[18],cols[19],
                       cols[0],cols[1],
                       cols[8],cols[9], 
                       cols[10],cols[11],
                       ]
new_cmap = LinearSegmentedColormap.from_list('new_cmap', reordered_cmap_list)
display_palette(new_cmap,len(reordered_cmap_list))

# new list for 14 colors:
reordered_cmap_list = [cols[6],cols[7],cols[2],cols[3],
                       cols[16],cols[17],cols[4],cols[5],
                       #cols[14],cols[15],# greys
                       cols[18],cols[19],
                       cols[0],cols[1],
                       cols[8],cols[9], 
                       ]
new_cmap = LinearSegmentedColormap.from_list('new_cmap', reordered_cmap_list)
display_palette(new_cmap,len(reordered_cmap_list))

import seaborn as sns
# Seaborn palettes don't work because they loop colors instead of adding new ones
cmap = sns.color_palette("colorblind",14)
hex_colors = [matplotlib.colors.rgb2hex(rgba) for rgba in cmap]
new_cmap = LinearSegmentedColormap.from_list('new_cmap', hex_colors)
display_palette(new_cmap,len(hex_colors))


import distinctipy
cmap = distinctipy.get_colors(14)
hex_colors = [matplotlib.colors.rgb2hex(rgba) for rgba in cmap]
new_cmap = LinearSegmentedColormap.from_list('new_cmap', hex_colors)
display_palette(new_cmap,len(hex_colors))

