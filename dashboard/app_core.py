#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 12:54:33 2025

@author: abbylute
"""

from shiny import App, ui, render, reactive
from shinywidgets import render_widget, output_widget
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from faicons import icon_svg

from shared import app_dir, df, dfmed, dfquant

# pretty palette, but hard to distinguish some colors
hex_colors = ['#001219', '#004757', '#047380', '#159899', '#74c3b4', '#bbd5b2',
              '#eacf8c', '#eda41a', '#db7f01', '#c75e02', '#bc4103', '#b32c0c',
              '#9c1e15', '#751a1d']
# tab20 based palette:
#hex_colors = ['#d62728','#ff9896','#ff7f0e','#ffbb78','#bcbd22','#dbdb8d',
# '#2ca02c','#98df8a','#17becf','#9edae5','#1f77b4','#aec7e8','#9467bd','#c5b0d5']
# distinctipy: light/bright colors are hard to see on white background
#hex_colors = ['#00ff00','#ff00ff','#0080ff','#ff8000','#80bf80','#5e07a3',
# '#e3033e','#ed7edd','#027a3e','#00ffff','#ffff00','#00ff80','#8b5545','#0000ff']

all_colors =  {
    "Low Demand": hex_colors[1],
    "Net Zero 2050": hex_colors[3],
    "Below 2°C": hex_colors[5],
    "Delayed Transition": hex_colors[6],
    "Fragmented World": hex_colors[7],
    "Nationally Determined Contributions (NDCs)": hex_colors[8],
    "Current Policies": hex_colors[11],
    "Very Low with Limited Overshoot":hex_colors[0],
    "Very Low after High Overshoot":hex_colors[2],
    "Low":hex_colors[4],
    "Medium Low":hex_colors[9],
    "Medium":hex_colors[10],
    "High":hex_colors[13],#[12],
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
        ui.nav_spacer(),
        ui.nav_control(ui.input_action_button("toggle_temp", "°C", class_="btn-outline-dark"),
                       #ui.input_dark_mode(id='darklight')
                       ),
        title = "Warming Dashboard",
        ),
    
    ui.page_sidebar(

    ui.sidebar(
        ui.input_slider("year", "Year", 2000, 2100, 2030),

        ui.input_checkbox_group(
            "scenario", 
            ui.tags.div(
                ui.tags.span("NGFS Scenarios"),
                ui.input_action_button("info_btn_ngfs", "i", class_="info-btn"),#, icon=icon_svg("circle-info")),
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
                ui.input_action_button("info_btn_cmip7", "i", class_="info-btn"),#, icon=icon_svg("circle-info")),
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
        ui.value_box("Median Warming", ui.output_ui("median_box"), 
                     showcase=icon_svg("temperature-half"), fill="grey"),
                     #showcase="fi fi-rr-temperature-high"),
        ui.value_box("Probability of Exceeding 1.5°C", ui.output_ui("prob15_box"), 
                     showcase=icon_svg("fire")),
        ui.value_box("Probability of Exceeding 2.0°C", ui.output_ui("prob20_box"), 
                     showcase=icon_svg("dumpster-fire")),
        fill=False,
    ),
    
    ui.layout_columns(
        ui.card("Warming Timeseries", output_widget("timeseries"), full_screen=True),
        ui.card("Warming Possibilities", output_widget("year_warming_dist"), full_screen=True),
    ),
    # the below code sets the color of the background of the main panel.
    # need to make this dynamic depending on dark/light mode
    ui.tags.style("""
                  :root {
                      --bslib-sidebar-main-bg: #004757; /*#f8f8f8;*/
                      }
                 """
                 ),
    ui.include_css(app_dir / "styles.css"),
    fillable = True,
)
)

def server(input, output, session):
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
        )
    
    @reactive.Effect
    @reactive.event(input.darklight)
    def set_background_colors():
        if input.darklight() == 'dark':
            pio.templates.default = "plotly_dark"
            bg_color = 'grey'
            card_bg_color = 'black'
        else:
            pio.templates.default = "plotly_white"
            bg_color = 'white'
            card_bg_color = 'white'
        return bg_color, card_bg_color
    
    @reactive.calc
    def year_number():
        return input.year()

    @reactive.calc
    def scenario_name():
        #return list(input.scenario())
        return list(input.scenario()) + list(input.scenario_cmip7())

    @reactive.calc
    def filtered_df():
        df1 = df[df["scenario"].isin(scenario_name())]
        if temp_unit.get() == "°F":
            df1['warming'] = df1['warming'] * 9/5
        return df1
        #return df[df["scenario"].isin(scenario_name())]

    @reactive.calc
    def year_df():
        df1 = df[(df["scenario"].isin(scenario_name())) & (df["year"] == year_number())]
        if temp_unit.get() == "°F":
            df1['warming'] = df1['warming'] * 9/5
        return df1
#        return df[(df["scenario"].isin(scenario_name())) & (df["year"] == year_number())]

    def med_warming_text():
        ydf = year_df()
        lines = []
        for sname in scenario_name():
            filt_df = ydf[ydf["scenario"] == sname]
            swarm = f"{filt_df['warming'].median():.2f} {temp_unit.get()}"
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
    
    def plot_scenarios_plotly(ds):
       ds = dfquant[dfquant['year'].between(1850,2101)]
       x = ds.year.unique()
       
       def hex_to_rgb(hex_color):
           hex_color = hex_color.lstrip('#')
           return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

       fig = go.Figure()

       for scenario in scenario_name():#ds.scenario.unique():
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
                # TODO: add plot of median trajectories
                ui.output_plot("cmip7_info_plot",width='1000px',height='600px'),
                size='xl',
                easy_close=True,
                footer=ui.modal_button("Close"),
            )
        )

    @output
    @render.plot
    def ngfs_info_plot():
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
        fig, ax = plt.subplots(figsize=(9,6))
        sns.lineplot(data=dfmed[dfmed['scenario'].isin(CMIP7_scenarios)], x="year", y="median_warming", hue="scenario", palette=CMIP7_colors)
        ax.set_title("Median Warming by Scenario")
        ax.set_ylabel("Warming (°C)")
        ax.set_xlabel("Year")
        ax.legend(frameon=False)
        return ax
    

    @output
    @render_widget
    @reactive.event(input.go)
    def timeseries():
        return plot_scenarios_plotly(filtered_df())

    @output
    @render_widget
    @reactive.event(input.go)
    def year_warming_dist():
        return plot_year_warming_probabilities_plotly()

    @output(id="median_box")
    @render.ui
    @reactive.event(input.go)
    def median_box_ui():
        return ui.HTML(med_warming_text())

    @output(id="prob15_box")
    @render.ui
    @reactive.event(input.go)
    def prob15_box_ui():
        return ui.HTML(exceedance_probability_text(1.5))

    @output(id="prob20_box")
    @render.ui
    @reactive.event(input.go)
    def prob20_box_ui():
        return ui.HTML(exceedance_probability_text(2.0))


app = App(ui=ui_app, server=server)
