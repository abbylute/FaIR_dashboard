#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 12:54:33 2025

@author: abbylute
"""

from shiny import App, ui, render, reactive
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
#from faicons import icon_svg
from shinywidgets import render_widget, output_widget

#from shared import app_dir, df, dfmed, dfquant
from pathlib import Path
import pandas as pd

# load data files
app_dir = Path(__file__).parent
app_dir1 = Path(__file__).parent.parent
df = pd.read_csv(app_dir1 / "data/fair_warming.csv")
dfmed = pd.read_csv(app_dir1 / "data/fair_warming_scenario_medians_exceedances.csv")
dfquant = pd.read_csv(app_dir1 / "data/fair_warming_scenario_quantiles.csv")


# icons from https://icons8.com/. To find icons that aren't white, enter the color as a search term in the search bar. changing the color of white icon does not work.
thermometer_icon = ui.HTML('<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB+ElEQVR4nO2YSytFURTHt2cpZI6hEZIvYKKEwkDKVMbKe+gxkPIthAEy4hPwFbwlZS66qUseP+0suV3Xufues8+xz3F+w9N6/Ndae+27u0qlfAM0AbtAhp/ob3tAi3JY/B3F0TaNyjX47Lxmv5BA/Q04EJtt5Rp8H5tfuws0i82Dcg0EW3aRkxbw1yR2AsBRobtUuQZJLSCftICwSOwEiPsOEPcC8kkLCIvEToC47wBxLyCftICwSOwEiPsOULiAQ+UauNpZU/5NAUAf0K9cApgT/VnDP8DegSWgLBqF3oIWRPwLMGZgPy62mrVoVP4upgt4A56AnhL8eoBnmYSxn1WACuBKOjntw39WfG+B6nBUFl9GzQlQ7sO/HDiTGKPhqPQWsCXJpwLEmJEYO3bVmSW/keQdAWJ0Soxru+rMkusl1DQEiNFgev1aB3iU5LUBYtRJjIxddWbJLyR5a4AYbRLjzK46s+SbknwmQIwpibFhV51Z8mFJridR5fN35FhiDIej0ltAZc49Pu/Df0J8L/00wAr6VSnPgVdgsAS/7pynxEC4KouLWZZO6iLmvbopx2Yi5wpeiVZtYVFlwKJ0U3Muv7DtQA1QL7fNJHAqNtp21Ynn9BdAb85OeHFRynGLFH18gCF9LcojLwvcy6KuAyN6+aNVpdzmAw3UhPaDC6NyAAAAAElFTkSuQmCC" alt="temperature">')
thermometer_icon_black = ui.HTML('<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAACSklEQVR4nO2aTYsTQRCGa3dVEFSWhDD9vt0yJy9REcndiyAqqAcRvIrnBddVj34cRPBfiHpQ8aS/QP+CukYRwbsoIqi4ulJYQQ0hO5kkk55xHphLqKquz04xiUjNH7z3AcADkp9Irvc9+tlD7/0uidj59wMc/+dRmRCCl9jA78yrg48GOaifAXhsMvckNmhtMyy7JHdaAB8lNmgtMim5wqkDmDWVrQDJp4OuU4kNVjWAfuoApkVlK8CyzwDLHkA/dQDTorIVYNlngGUPoJ86gGlR2Qqw7DPAwQE8kdhgrJnNyn8TgHPuiPf+qMQEyYv2wupLxhdgPwFcFZG5Yjwc7tBly/53kmc2kgdw1mQ14JsyS5xzB0j+APAVwKGseioL4JtVIrPepFkA8Nqyf35UZZIXrArv2u32FikaHUZz/rmIzOcwMU9y1WyclqIheVcP994vj2Fjxapwf7LeZTv8rQWwbwwb+60Cb6RobAjX0zRdzGsjTdPFrNfvxCH5WQ9vtVrb8tpoNpvbe7+fSdEA6OrhSZLszmsjSZI9FsCqFA3JO3b4Sl4b3vtls3FbisY5d9L6t9vpdDbnMLFA8pnaUFsyAzb17nEAl0ZVBrBkuq9yJmB8dKvUdYDkGsnjWfVIHuytEiSPySwBcM36eE0rsUE2df1Y6l3BJK9LBMyRvGLZ1JZ4qYMdQtgbQtjaaDR26G0D4BzJF+a4yt6IYp3u4Zw7/NduM+yvBt1R2q1QtH0AnNBrUZc8/YYF8EEHFcAt7/0pHf5ivZK4+QUFpEqmGgBt1AAAAABJRU5ErkJggg==" alt="temperature">')
fire_icon = ui.HTML('<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFBElEQVR4nNWaaahVVRTHj6Zi+bTIrCjTSs0GTZQGqAwLo3oNRuaXhGi2voRhCEEZRSk0ERVEIWqQaRM5vKaXEY32jAxLs4nmLM0Gqle+8vWL1f0f3N3uPXude86z99ane8/9r/9a65yz115r7ZskJQuwC7AWeAkYkfRUAQ5lh/wMTE96ogDnKIgfg4AWAAOSniTAHDl/JTAD+F3fNwLjkp4iwKty/Eh9Hw98pGsW1MVJdxdgMLAd+BroHVzfHXgseNXmAr2S7irALDl6V53frwL+FGYp0D/pbkIl7X4sJydk4JqBX4R7Ddgr6U4CXCjnVjmwRwHfCm/BH5x0BwF2Bb6UYyc5dUYAH0rnM2BY13sad+p2ObQip94QYE3wZPbvOi/jzhynTNUOjGpAf0/gnWCv2adrPI078amcuKIAz77Ba/aupfFyPc023htYKePLSuAbDnwhvlbLguV4Gjc8T0Y3lZVCgdHA9+KdVwZnzOAFMtYBnBjB9gduAU5wcp8OdAJ/AeeW5nQNQ8cD2xTIJQ78ycJu8zoG3BS0AYeV4niVgQOBzTJyp1PniKDGsux2qXP9tUpndVi3FRZgYJAmn/YuRqCJf4u9Mpc595jN0plRVhB2h5aLdINVszn1t0rX2l+TP4BTcpQ9PwB7FwqiKkNtbaQPB96SvvUmq4IO8vCIXq+gv3mwaBDNeh3sLk5qkOMpOTNRr9q64On2i+iOU+lvPowtsuNukdFZDZFUeFrEMUXfRwY9/bUO/YXCLmnUgSXB4m64owueyNnBtWm6ZjXaQY6ngp5MvsLSFuM/qpUm6IBGgxCX3QiTM6quP6frDzs4XhR2Tl7jb0rxmgZ8r+ZKF+ykGjOw7brTmf1IMGbakHeBm3wV66ttXqWgnwX61sGk+8GwjKeVuVbUvKWjpUO8gayQwkwH9h52yH8KPTOq37bUWmfAVP2+xmHreWEv9450OpRuBzt677TAa6+1awM3yvjiOhxNerXM3m4Re7PFtdATyHSBWxzY9LVYBJwmZyyYO3RDjg4mJhMzeKyZMqk7fRFusnCrPYHcLfDsCG6UcOb8UF07X0+zWhY495kznQXoJk8gr9fKMBkz3qVV1ycAT2qBf2CLOFZgAo+Ia6qjtTZp9wSS9uDDI7i0zJ4WJY3bXCausyK4fsJ1eEh/EnhQBPe5cIUPc3QwZDLeUTKZfOMhTWezfSK4tLcuuuun+4NtjAMj2DGyud5DnBZzmT1HML4Z04D/Ic+p4mlzYNPdvdVDvNHjoKbphapi8Twknusd2FuFvdlD/LjAmWd/wHnBqDNzI8vgGKrXqtMz+6UyvY+m6RQ8U+BFjmOEdG57f84YUo4HvH0GlcFHp6Yxe3jIR2p3tuzV5NigfkuDyXNwo5lxp5LLaAf+Btl51GvDlF6Q0tUO7OQgmLWxbBforZfOXAd2gCaaJs2NNFU2bBjiwI8F3tY5R2YPHujYvKrN8xSB6+TPutwzrqD+WZljhlXeIE1ibbAmjvmeRkCwH/CdCOb/H6ewQF/gDfnwTBGiY4O7cV+9DrArhMpMa35akhQ+ALIzwaDFbNsZB5dUgrhXNju855Ie4mOAT0T8K3BbVx2RUWnIWoJeZ0rZBuzfC4u1x6CU+wRwkfaTQQX5+1ibrH9NoH0ss6wvJGqclgcBhfJKAd60SjCxzzvn7N1qI/0DyNLze0oKLxfgs33lfbXLudP43zjrlXuJCC9sAAAAAElFTkSuQmCC" alt="fire-element--v1">')
fire_icon_black = ui.HTML('<img src="data:image/png;base64,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" alt="fire-element--v1">')
house_fire_icon = ui.HTML('<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAADs0lEQVR4nO2aW8hOWRjHt3E+zESNQ84zIlGUQw43SHGDcmiM1EeiZFLU1JALbnDhkLhgrpS4kFOZGSlR3GkozPA5xWgS4+xzmoSfnvHfLGv23u9+D3u/r3z/Wn3vfvaznrV+e532WvsLggzFO90GDgDDg09RQGs+1htgVfCpCeghgLPAYQdoZVALAnqm9Jukim/S9VzglVpmUuYVLSRV7i9gHdArwW+LfL9zbD/KdgNoE1RLQFuv3zcAdRF+XwL3gWeWx7F/AfyuvEu8PMOBn4AWeYD0ViUuACf1+zUw0/Oz1jJtjogxXvfqPXtn2f8EBmQNMkOFrdfTXaPrB0BH+UzTOHgIdImI0QS4qHz9HXsL5TPdA4ZkCbJTBU1xbIdkWwpMBp7oenZCnNXy+cGxLZfNJgT0IAZmAdEHeAk8dgeqWsB0S93MtLpArIny+xlobuuLWuO1HsZ+pwu3qjRI+OQ3ePb2zuC3p7kiRaxezux3zcm7yFlMT8u+vJIQsxTUZqKvI+6Hg3RkibNfPTAuYhYLx1/LSkB0AP5R0LkxPnVAsyLjmq4CC+PyAkflN73U+gcRg/B42cE+jjvGZrACPotV9pZKFBiuF1PLDlZ82WNV9rFSA9S0gs8WJKgx0QhSY6KxRXIU8FXSi6Z8qjfYgU6WUvruBbbH7R6rBiKIP5QKwgATVPS5qG10VUAciFAFYXi3WbvpbAuGVhXEgwhbJC3MLgf+DtCvKiAREP+NkTgY/80ZWOIt5PaG3C5XkAIVjryn6/PAKF1PdfYoNlZMW3MDSYJI8OnuPPkX2gKHb7zXbc+uIyXbBg/OHCQNRIyvdRtXd4H5+n1Z/nZiY9pdMkgJSjvN+jPaIefg7pH+npBvV+Bft5CsQVJBOGV0BK4o7zIdej904r0/3AMOlgQSBVVS5uS4zbVWmAZFzFhjHd/Qvr2cArMCCWencx7cZeCSu58HRsj3VC2C7PFPG511pS7mHOx2UCmQpEFSZFw7nDN969mbWvJsbeT7ohZBbN0gzeEbHz7jPa84SJKPbN3VfRqU9gF9nftPla1tijp8I9+/cwURhB2v+jJbN/mc8WenOAHfy/e3IGeQcCD/YhVX+lW23d6nhX0p6nBEvovzBrGuRPj0va+8j5wVO+xeCxPKX+AcZnfIG+R/PjF+c/RCaGkHMFon9ZaGAducby6RB+hlg0SpWBDZ5jktE6uyIPIAcbrdWv1zQYPA7HvLxsxAyslTyVhFqxGExhbJtmtVW8HnAvIWDK0FVYK0rvkAAAAASUVORK5CYII=" alt="burning-house">')
house_fire_icon_black = ui.HTML('<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEVUlEQVR4nO2aW4gcRRSG23iNN3TXma7/PzM7XlaRFQw4Bo0vRgR9USEqXhBiEAVRAhGEGHwwL9GHqIh5MHkKiD6IRsFLEERB30QFL0lWoxhFxHjZbLIalZC4cpJToSh6Zntnu3smZA8UTJ8+dfnqcqrq9CRJiUJymuRukm845xYnx6I0Go2FBuLTfwDWJseakGwqAIAvSL4bAD2RDIIAGMljR/Ima/hz9ryC5EEdGX1XekNnEmvcDwDWO+daXew2mO0dge5R0/0I4PSkX5Km6RnRvJ8SkeWx3fDw8FkAJkju1zzBqwUkP7EptyrMo84AwOqxsbFTqgA53wB2APjYfh8ieWdop6Nl756PyyB5vb0bD/X1ej01/Tbn3FipICJyu/Xm09a7T9rzHudcTW2cc7eah5qs1Wouo5gTAHxt+S71Sh0JHlk/qv8DwBWlgZB8yXrtlkC3VXUi8gjJm0n+aY25p0s566ych70OwBrTHbT8k2maXlY4RLPZvAjAAZL7woVqI6AN+MWmmf5e160sADea3aZ2u32y7i82GoesM173U7jVap1WKIjveQDPhPpWq3VOsPi1Nx+fqSz1dt77kfw+yPtQsJl+ZvWtKQwCwN1W6ASA8zIgDy9SEbm6R+83LiLXRbCL/fobHR09dc4QIyMj55L81SpckWVjLvik2ZRrjfyO5IOd8gJ4X+2cc7f12v4kYxF+mBQozrlr1YPNUPdKq3vDnCv0+wWAZUnFIiJLre4Peiogmr8Dl5LjFiQZMOE8yIAJ50ekQhkaGjq720Gz7yOSpmldU856XwOwudPtsW8gCkDyK015YADcYBvgl1nX6L6ABBDe/+eBWQDgZ38tANDuK0gEcXhE8sKQfDmA/43kJX0BiSH8GukEE5+cAawKd3E9IddqtTMrBenW4E7v7Hk7ySUGssx047pWDOaFykC6QXSyEZFG0PP/6BXYn3hJ7tI7u4aU9BosIotKB8kDkWVrF6vwQPg7gPvt3U6114iNPb9S5ek3l5vN8Ghbg8DdXtN9pLbNZpMA/p3T6bcMCC8aBwPwrTX+MQ16A5gMyjsa3APwZk8gWVBJwaJhIAshaUzs8thjichSb+v1uuv3XGFZIN47qWfyuvaRGNdOAN+E93kRucra8ekggrwaRxv9vhIHxoM42O6kKJBu62SW5Wpwbrper18YvTrR0lHRQ6R30QMHoo3SPHmCbw37jAfg78JButmo6GZn02fK0hYRuTjI85fmib6fZEqaphcYyE9JlSAGMRGPmOoajYaoDYDPY+/USUjeZfnfSaoE8QsZwFvacE0A3vY7dPRpYctMbQDwnuVdWSmITaVp3/vRV969fsf208viv50gHrB8ezQOXTVI5uLPsLvXvotoepHkNbpmNDnnrgSwMfjmkhlAL9Vr5QUx3X3ByEwX4RH7AmJ6nWdP2Z8LpgxsG4BnSwOZS54iy5q1zINwfkTKnVr9TsnxAvI/4hd4Kq4ifq0AAAAASUVORK5CYII=" alt="burning-house">')

# pretty palette, but hard to distinguish some colors
#hex_colors = ['#001219', '#004757', '#047380', '#159899', '#74c3b4', '#bbd5b2',
#              '#eacf8c', '#eda41a', '#db7f01', '#c75e02', '#bc4103', '#b32c0c',
#              '#9c1e15', '#751a1d']
# tab20 based palette:
#hex_colors = ['#d62728','#ff9896','#ff7f0e','#ffbb78','#bcbd22','#dbdb8d',
# '#2ca02c','#98df8a','#17becf','#9edae5','#1f77b4','#aec7e8','#9467bd','#c5b0d5']
# distinctipy: light/bright colors are hard to see on white background
#hex_colors = ['#00ff00','#ff00ff','#0080ff','#ff8000','#80bf80','#5e07a3',
# '#e3033e','#ed7edd','#027a3e','#00ffff','#ffff00','#00ff80','#8b5545','#0000ff']
# adapted from sashamaps: https://sashamaps.net/docs/resources/20-colors/
hex_colors = [
              '#f032e6', #magenta
              '#9A6324', #brown
              '#911eb4', #purple
              ##'#fabed4', #pink
              ##'#dcbeff', #lavender
              #'#fffac8', #beige
              ##'#aaffc3', # mint
              #'#808000', # olive
              #'#ffd8b1', # apricot
              ##'#000075', #navy too dark
              #'#ffffff',#white 
              #'#000000',# black
              '#4363d8', #blue
              '#42d4f4', #cyan
              '#a9a9a9', #grey
              '#469990', #teal
              '#0e731a',#'#3cb44b', #green
              '#97bd37',#'#bfef45', #lime
              '#ffe119', #yellow
              '#f58231', #orange
              '#e6194B', #red
              '#910606',#800000', #maroon
              ] 

all_colors =  {
    "Low Demand": hex_colors[1],
    "Net Zero 2050": hex_colors[3],
    "Below 2°C": hex_colors[5],
    "Delayed Transition": hex_colors[6],
    "Fragmented World": hex_colors[7],
    "Nationally Determined Contributions (NDCs)": hex_colors[9],
    "Current Policies": hex_colors[11],
    "Very Low with Limited Overshoot":hex_colors[0],
    "Very Low after High Overshoot":hex_colors[2],
    "Low":hex_colors[4],
    "Medium Low":hex_colors[8],
    "Medium":hex_colors[10],
    "High":hex_colors[12],#[12],
    #"High Overshoot":hex_colors[13],
    }

NGFS_scenarios = ["Low Demand","Net Zero 2050","Below 2°C","Delayed Transition",
                  "Fragmented World","Nationally Determined Contributions (NDCs)",
                  "Current Policies"]
CMIP7_scenarios = ["Very Low with Limited Overshoot",
                   "Very Low after High Overshoot","Low","Medium Low","Medium",
                   "High"]#,"High Overshoot"]

NGFS_colors = {k: all_colors[k] for k in NGFS_scenarios}
CMIP7_colors = {k: all_colors[k] for k in CMIP7_scenarios}



ui_app = ui.page_fluid(
    ui.page_navbar(
        ui.nav_control(ui.input_action_button(id="info_btn_title", label="i", class_="title-info-btn")),
        ui.nav_spacer(),
        ui.nav_control(ui.input_action_button("toggle_temp", "°C"),
                       ui.input_dark_mode(id='darklight'),
                       ),
        ui.nav_spacer(), 
        ui.nav_control(ui.tags.a(ui.output_ui(id='logo'),
                                 href='https://www.woodwellclimate.org/',
                                 target="_blank")),
        title = "Warming Dashboard",
        ),
    
    ui.head_content( # sets background panel color based on dark/light mode
        ui.output_ui("dynamic_style")
    ),
    
    ui.page_sidebar(

    ui.sidebar(
        ui.input_slider("year", "Year", 2000, 2100, 2030),

        ui.input_checkbox_group(
            "scenario", 
            ui.tags.div(
                ui.tags.span("NGFS Scenarios"),
                ui.input_action_button("info_btn_ngfs", "i", class_="info-btn"),
            ),
            {
                name: ui.span(name, style=f"color: {color}; font-weight: bold;")
                for name, color in NGFS_colors.items()
            },
            selected=["Current Policies"],
        ),
        
        ui.input_checkbox_group(
            "scenario_cmip7", 
            ui.tags.div(
                ui.tags.span("Preliminary CMIP7 Scenarios"),
                ui.input_action_button("info_btn_cmip7", "i", class_="info-btn"),
            ),
            {
                name: ui.span(name, style=f"color: {color}; font-weight: bold;")
                for name, color in CMIP7_colors.items()
            },
        ),

        ui.input_action_button("go", "Calculate"),
        
        width=400,
        ),

    ui.layout_columns(
        ui.output_ui(id='median_value_box'),
        ui.output_ui(id='prob15_value_box'),
        ui.output_ui(id='prob20_value_box'),

        fill=False,
    ),
    
    ui.layout_columns(
        ui.card("Warming Time Series", output_widget("timeseries"), full_screen=True),
        ui.card("Warming Possibilities", output_widget("year_warming_dist"), full_screen=True),
    ),

    ui.include_css(app_dir / "styles.css"),
    fillable = True,
)
)

def server(input, output, session):
    
    # update icon colors
    @reactive.event(input.darklight)
    def therm_icon():
        if input.darklight() == 'dark':
            return thermometer_icon, fire_icon, house_fire_icon
        else:
            return thermometer_icon_black, fire_icon_black, house_fire_icon_black
        
    # update value boxes    
    @output()
    @render.ui
    @reactive.event(input.darklight)
    def median_value_box():
        return ui.value_box(
            'Median Warming',
            ui.output_ui('median_box'),
            showcase=therm_icon()[0])

    @output()
    @render.ui
    @reactive.event(input.darklight)
    def prob15_value_box():
        return ui.value_box(
            "Probability of Exceeding 1.5°C",
            ui.output_ui('prob15_box'),
            showcase=therm_icon()[1])

    @output()
    @render.ui
    @reactive.event(input.darklight)
    def prob20_value_box():
        return ui.value_box(
            "Probability of Exceeding 2.0°C",
            ui.output_ui('prob20_box'),
            showcase=therm_icon()[2])    
    
    # update logo based on dark/light    
    def set_logo():
        if input.darklight() == 'dark':
            logo_source = "Horizontal-White Lettering - Woodwell logo.png"
        elif input.darklight() == 'light':
            logo_source = "Horizontal - Woodwell logo.png"
        return logo_source
    
    @reactive.Effect
    @reactive.event(input.darklight)
    def set_background_colors():
        if input.darklight() == 'dark':
            pio.templates.default = "plotly_dark" # this doesn't update plots that are already made
        elif input.darklight() == 'light':
            pio.templates.default = "plotly_white" # this doesn't update plots that are already made
        return

    @output
    @render.ui
    # use this to set background color, card colors, etc depending on dark/light mode
    def dynamic_style():
        if input.darklight() == 'dark':
            color = '#111111' # color to match plotly_dark background
        else:
            color = '#ffffff'
        # to set card color:
        return ui.tags.style(f"""
            .card {{
                background-color: {color} !important;
                }}
            .navbar {{
                background-color: {color} !important;
                margin-left: -10px;
                margin-right: -10px;
                }}
            .sidebar {{
                background-color: {color} !important;
                margin-bottom: -100px;
                margin-left: -10px;
                }}
            .irs-from, .irs-to, .irs-single, .irs-max, .irs-min {{
                font-size: 13px !important; 
            }}
            """
        )
            # to set color of background of main panel:
            #    :root {{
            #        --bslib-sidebar-main-bg: {color};
            #        }}    
            #.card {{
            #    color: {color} !important; # this sets the card title text color
            #    }}
    

    temp_unit = reactive.Value("°C")
    @reactive.Effect
    @reactive.event(input.toggle_temp)
    def _():
        if temp_unit.get() == "°C":
            temp_unit.set("°F")
        else:
            temp_unit.set("°C")
        ui.update_action_button(
            "toggle_temp", 
            label=temp_unit.get(), 
            #class_="btn-primary"
            #class_="btn-outline-dark"
        )
    
    @reactive.calc
    def year_number():
        return input.year()

    @reactive.calc
    def scenario_name():
        #return list(input.scenario())
        return list(input.scenario()) + list(input.scenario_cmip7())


    @reactive.calc
    def year_df():
        df1 = df[(df["scenario"].isin(scenario_name())) & (df["year"] == year_number())]
        if temp_unit.get() == "°F":
            df1['warming'] = df1['warming'] * 9/5
        return df1
#        return df[(df["scenario"].isin(scenario_name())) & (df["year"] == year_number())]


    def med_warming_text():
        lines = []
        for sname in scenario_name():
            filt_df = dfmed[(dfmed["scenario"] == sname) & (dfmed["year"]==year_number())]
            swarm = f"{filt_df['median_warming'].values[0]:.2f} {temp_unit.get()}"
            color = all_colors[sname]
            line = f'<div style="color: {color}; font-weight: bold; margin: 0; line-height: 1.2;">{swarm}</div>'
            lines.append(line)
        return "".join(lines)

    def exceedance_probability_text(level):
        lines = []
        for sname in scenario_name():
            prob = dfmed[(dfmed['scenario'] == sname) & (dfmed['year'] == year_number())]['prob'+str(level)].iloc[0]
            color = all_colors[sname]
            line = f'<div style="color: {color}; font-weight: bold; margin: 0; line-height: 1.2;">{prob:.1f} %</div>'
            lines.append(line)
        return "".join(lines)
    

    def plot_scenarios_plotly():
        ds = dfquant[dfquant['year'].between(1850,2101)]
        x = ds.year.unique()
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
 
        fig = go.Figure()

        for scenario in scenario_name():
            ds1 = ds[ds['scenario']==scenario]
            ymed = ds1[ds1['CI_level']==0.50]['warming']
            for pp in ((0.00, 1.00, .2), (0.05, 0.95, .3), (0.16, 0.84, .4)): # lower CI, upper CI, alpha value
                ylower = ds1[ds1['CI_level']==pp[0]]['warming']
                yupper = ds1[ds1['CI_level']==pp[1]]['warming']
             
                lab0 = scenario + ' ' + str(int(pp[0]*100)) + '% CI'
                lab1 = scenario + ' ' + str(int(pp[1]*100)) + '% CI' 
                rgb_color = hex_to_rgb(all_colors[scenario])
                rgba_color = f'rgba{rgb_color + (pp[2],)}'
        
                fig.add_trace(go.Scatter(
                    x=x, 
                    y=ylower,
                    fill=None,
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    name=lab0,
                    hovertemplate='<b>%{fullData.name}</b><br>year: %{x}<br>warming: %{y:.3f}<extra></extra>',
                    hoverlabel=dict(bgcolor=all_colors[scenario])
                    ))
                fig.add_trace(go.Scatter(
                    x=x,
                    y=yupper,
                    fill='tonexty', # fill area between trace0 and trace1
                    mode='lines', 
                    line=dict(width=0),
                    fillcolor=rgba_color, 
                    line_color=rgba_color,
                    showlegend=False,
                    name=lab1,
                    hovertemplate='<b>%{fullData.name}</b><br>year: %{x}<br>warming: %{y:.3f}<extra></extra>',
                    hoverlabel=dict(bgcolor=all_colors[scenario])
                    ))
            
            # add median line
            fig.add_trace(go.Scatter(
                x=x, 
                y=ymed, 
                line_color=all_colors[scenario], 
                showlegend=False,
                name=scenario + ' Median',
                hovertemplate='<b>%{fullData.name}</b><br>year: %{x}<br>warming: %{y:.3f}<extra></extra>',
            ))
            
        # add final touches
        fig.add_hline(y=0, line_width=.5)
        hlines = [1.5,2]
        if temp_unit.get() == '°F':
            hlines = [h*9/5 for h in hlines]
        fig.add_hline(y=hlines[0], line_width=.5,
                      annotation_text='   1.5°C', annotation_position='top left')
        fig.add_hline(y=hlines[1], line_width=.5,
                      annotation_text='   2°C', annotation_position='top left')
        fig.add_vline(x=year_number(), line_dash='dot', line_width=1,
                      annotation_text=str(year_number())+'  ', 
                      annotation_position="top left",
                      annotation_font_size=15,
                      annotation_textangle=-90)
        
        fig.update_traces(mode='lines')
        fig.update_layout(
            yaxis_title="warming",
            yaxis_ticksuffix=temp_unit.get(),
            width=600,height=500) # this helps control the plot size, but it is still changing a bit when I add scenarios
        return fig


    def plot_year_warming_probabilities_plotly():
        binbreaks=list(np.arange(0,8,.25))
        mx = year_df()['warming'].max()
        mn = year_df()['warming'].min()
        st_index = [x for x, val in enumerate(binbreaks) if val>mn][0] -1
        en_index = [x for x, val in enumerate(binbreaks) if val>mx][0] #+1
        
        fig = make_subplots(rows=2, cols=1, 
                        row_heights=[.3,.7],
                        shared_xaxes=True, 
                        vertical_spacing=0.03)

        # It seems the only way to add a marginal boxplot above this is to do a separate subplot.
        # If I didn't need to control the bin edges it might have been possible, but I do want to set the bins myself.
        # order the scenarios:
        scens = year_df()['scenario'].unique()
        scens = [n for n in list(all_colors.keys()) if n in scens]
        for scenario in scens:
            ydf = year_df()
            
            fig.add_trace(go.Box(x=ydf[ydf['scenario']==scenario]['warming'], 
                          marker_color=all_colors[scenario],
                          name=scenario,
                          showlegend=False),
                          row=1, col=1)

            fig.add_trace(go.Histogram(
                x=ydf[ydf['scenario']==scenario]['warming'], 
                customdata = list(temp_unit.get()),
                histnorm="probability",
                xbins=dict(start=binbreaks[st_index], end=binbreaks[en_index], size=0.25),
                marker_color=all_colors[scenario],
                name=scenario + ', ' + str(year_number()),
                showlegend=False,
                hovertemplate='<b>%{fullData.name}</b><br>warming: %{x}<br>probability: %{y:.3f}<extra></extra>',
                ), row=2,col=1)
            
        fig.update_layout(width=600, height=525)
        
        # Update axis properties
        fig.update_yaxes(title_text='probability',row=2,col=1)
        fig.update_yaxes(showticklabels=False, row=1, col=1)
        fig.update_xaxes(title_text='warming ' + temp_unit.get(),
            tickmode = 'array',tickvals = binbreaks[st_index:en_index], 
            row=2,col=1, showgrid=True)
        fig.update_xaxes(tickmode = 'array',
                         tickvals = binbreaks[st_index:en_index], 
                         row=1,col=1, showgrid=True)
        return fig


    @reactive.effect
    @reactive.event(input.info_btn_ngfs)
    def show_modal():
        ui.modal_show(
            ui.modal(
                ui.HTML("<b>NGFS Scenarios</b>"),
                ui.tags.p("The ", ui.tags.a("NGFS (Network for Greening the Financial System) scenarios", href='https://www.ngfs.net/ngfs-scenarios-portal/', target='_blank'), " explore a range of climate policy and socioeconomic pathways. A brief description of each scenario is provided below, followed by a plot of the median warming projected by each scenario."),
                
                ui.tags.p("Low Demand", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("The Low Demand scenario assumes that significant behavioural changes - reducing energy demand - in addition to (shadow) carbon price and technology induced efforts, would mitigate pressure on the economy to reach global net zero CO2 emissions around 2050.", style="margin-left: 25px;"),
                ui.tags.p("Net Zero 2050", style="font-weight: bold; margin-bottom: 0; margin-left: 25px;"),
                ui.tags.p("Net Zero 2050 limits global warming to 1.5°C through stringent climate policies and innovation, reaching global net zero CO2 emissions around 2050.", style="margin-left: 25px;"),
                ui.tags.p("Below 2°C", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Below 2 °C gradually increases the stringency of climate policies, giving a 67 % chance of limiting global warming to below 2 °C.", style="margin-left: 25px;"),
                ui.tags.p("Delayed Transition", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Delayed Transition assumes global annual emissions do not decrease until 2030. Strong policies are then needed to limit warming to below 2 °C. Negative emissions are limited.", style="margin-left: 25px;"),
                ui.tags.p("Fragmented World", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("The Fragmented World scenario assumes delayed and divergent climate policy ambition globally, leading to high physical and transition risks.", style="margin-left: 25px;"),
                ui.tags.p("Nationally Determined Contributions", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Nationally Determined Contributions (NDCs) includes all pledged policies as of March 2024 even if not yet backed up by implemented effective policies.", style="margin-left: 25px;"),
                ui.tags.p("Current Policies", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Current Policies assumes that only currently implemented policies are preserved, leading to high physical risks.", style="margin-left: 25px;"),
                
                ui.output_plot("ngfs_info_plot",width='1000px',height='600px'),
                size='xl',
                easy_close=True,
                footer=ui.modal_button("Close"),
            )
        )


    @reactive.effect
    @reactive.event(input.info_btn_cmip7)
    def show_modal_cmip7():
        ui.modal_show(
            ui.modal(
                ui.HTML("<b>Preliminary CMIP7 Scenarios<b/>"),
                ui.tags.p("The preliminary CMIP7 scenarios, taken from the Scenario Model Intercomparison Project for CMIP7 (", ui.tags.a("ScenarioMIP-CMIP7", href='https://egusphere.copernicus.org/preprints/2025/egusphere-2024-3765/', target='_blank'), 
                          ") provides a wide range of possible future outcomes spanning those representing ambitious emissions reductions to those representing pessimism about climate action. A brief summary of the scenarios is provided below followed by a plot of the median warming trajectories.", style="font-weight: normal;"),
                ui.tags.p("Very Low with Limited Overshoot", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Scenario consistent with limiting warming to 1.5°C by 2100 with limited overshoot (as low as plausible) of 1.5 °C during the 21st century", style="margin-left: 25px;font-weight: normal;"),
                ui.tags.p("Very Low after High Overshoot", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Scenario with similar end of-century temperature impact to the Very Low with Limited Overshoot scenario, but with less aggressive near-term mitigation and large reliance on net negative emissions, resulting in a higher overshoot.", style="margin-left: 25px;font-weight: normal;"),
                ui.tags.p("Low", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Scenario cnosistent with likely staying below 2°C.", style="margin-left: 25px;font-weight: normal;"),
                ui.tags.p("Medium-Low", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Scenario with delayed increase in mitigation effort, insufficient to meet Paris Agreement objectives", style="margin-left: 25px;font-weight: normal;"),
                ui.tags.p("Medium", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("Medium emissions scenario consistent with current policies.", style="margin-left: 25px;font-weight: normal;"),
                ui.tags.p("High", style="font-weight: bold; margin-bottom: 0;margin-left: 25px;"),
                ui.tags.p("High emission scenario to explore potential high-end impacts.", style="margin-left: 25px;font-weight: normal;"),
                ui.output_plot("cmip7_info_plot",width='1000px',height='600px'),
                size='xl',
                easy_close=True,
                footer=ui.modal_button("Close"),
            )
        )

    @reactive.effect
    @reactive.event(input.info_btn_title)
    def show_modal_title():
        ui.modal_show(
            ui.modal(
                ui.HTML("<b>About<b/>"),
                ui.tags.p("The Warming Dashboard is based on simulations using the reduced complexity climate model ", 
                          ui.tags.a("FaIR", href='https://gmd.copernicus.org/articles/14/3007/2021/', target='_blank'), 
                          ". More details about the modeling approach and input data can be found in the ",
                          ui.tags.a("technical documentation", href="Warming Dashboard Technical Documentation.pdf", target='_blank'),".", style="font-weight: normal;"),
                ui.tags.p("Questions and comments can be directed to Dr. Abby Lute at alute@woodwellclimate.org.", style="font-weight: normal;"),
                easy_close=True,
                footer=ui.modal_button("Close"),
            )
        )

    @output
    @render.plot
    def ngfs_info_plot():
        if input.darklight() == 'dark':
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
        fig, ax = plt.subplots(figsize=(9,6))
        sns.lineplot(data=dfmed[dfmed['scenario'].isin(NGFS_scenarios)], x="year", y="median_warming", hue="scenario", palette=NGFS_colors)
        ax.set_title("Median Warming by Scenario")
        ax.set_ylabel("Warming (°C)")
        ax.set_xlabel("Year")
        ax.legend(frameon=False)
        return ax
    
    @output
    @render.plot
    def cmip7_info_plot():
        if input.darklight() == 'dark':
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
        fig, ax = plt.subplots(figsize=(9,6))
        sns.lineplot(data=dfmed[dfmed['scenario'].isin(CMIP7_scenarios)], x="year", y="median_warming", hue="scenario", palette=CMIP7_colors)
        ax.set_title("Median Warming by Scenario")
        ax.set_ylabel("Warming (°C)")
        ax.set_xlabel("Year")
        ax.legend(frameon=False)
        return ax
    

    @output
    @render_widget
    @reactive.event(input.go, input.darklight, input.toggle_temp)
    def timeseries():
        if input.darklight() == 'dark':
            pio.templates.default = "plotly_dark"
        elif input.darklight() == 'light':
            pio.templates.default = "plotly_white"
        return plot_scenarios_plotly()

    @output
    @render_widget
    @reactive.event(input.go, input.darklight, input.toggle_temp)
    def year_warming_dist():
        if input.darklight() == 'dark':
            pio.templates.default = "plotly_dark"
        elif input.darklight() == 'light':
            pio.templates.default = "plotly_white" 
        return plot_year_warming_probabilities_plotly()

    @output(id="median_box")
    @render.ui
    @reactive.event(input.go, input.darklight, input.toggle_temp)
    def median_box_ui():
        return ui.HTML(med_warming_text())

    @output(id="prob15_box")
    @render.ui
    @reactive.event(input.go, input.darklight)
    def prob15_box_ui():
        return ui.HTML(exceedance_probability_text(1.5))

    @output(id="prob20_box")
    @render.ui
    @reactive.event(input.go, input.darklight)
    def prob20_box_ui():
        return ui.HTML(exceedance_probability_text(2.0))
    
   
    @output(id="logo")
    @render.ui
    @reactive.event(input.go, input.darklight)
    def logo_img():
        return ui.img(src = set_logo(), style="max-width:220px;width:100%")


static_dir = Path(__file__).parent / "static"
app = App(ui=ui_app, server=server, static_assets=static_dir)
