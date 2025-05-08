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

from shared import app_dir, df, dfmed

# NGFS_colors = {
#     "Low Demand": "#00a9cf",
#     "Net Zero 2050": "#2274ae",
#     "Below 2°C": "#003466",
#     "Delayed Transition": "#92397a",
#     "Fragmented World": "#b0724e",
#     "Nationally Determined Contributions (NDCs)": "#f69320",
#     "Current Policies": "#df0000",
# }
# CMIP7_colors = {
#     "Very Low with Limited Overshoot":"@00a9cf",
#     "Very Low after High Overshoot":"#003466",
#     "Low":"#00a9cf",
#     "Medium Low":"#df0000",
#     "Medium":"#92397a",
#     "High":"#f69320",
#     "High Overshoot":"#df000",
#     }

hex_colors = ['#001219', '#004757', '#047380', '#159899', '#74c3b4', '#bbd5b2',
              '#eacf8c', '#eda41a', '#db7f01', '#c75e02', '#bc4103', '#b32c0c',
              '#9c1e15', '#751a1d']
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
    "High":hex_colors[12],
    "High Overshoot":hex_colors[13],
    }

NGFS_scenarios = ["Low Demand","Net Zero 2050","Below 2°C","Delayed Transition",
                  "Fragmented World","Nationally Determined Contributions (NDCs)",
                  "Current Policies"]
CMIP7_scenarios = ["Very Low with Limited Overshoot",
                   "Very Low after High Overshoot","Low","Medium Low","Medium",
                   "High","High Overshoot"]

NGFS_colors = {k: all_colors[k] for k in NGFS_scenarios}
CMIP7_colors = {k: all_colors[k] for k in CMIP7_scenarios}

pio.templates.default = "plotly_white"



ui_app = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("year", "Year", 2000, 2100, 2030),

        ui.input_checkbox_group(
            "scenario", 
            ui.tags.div(
                ui.tags.span("NGFS Scenarios"),
                ui.input_action_button("info_btn", "", icon=icon_svg("circle-info"), class_="info-btn"),
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
                ui.input_action_button("info_btn_cmip7", "", icon=icon_svg("circle-info"), class_="info-btn"),
            ),
            {
                name: ui.span(name, style=f"color: {color}; font-weight: bold;")
                for name, color in CMIP7_colors.items()
            },
        ),

        ui.input_action_button("toggle_button", "°C", class_="btn-outline-dark", style="width: 10%"),#icon=ui.HTML("<i class='fa fa-play'></i>")), #class_="btn-primary"),
        #ui.output_text("current_option_out"),

        ui.input_action_button("go", "Calculate"),
        width=400,
        ),

    ui.layout_columns(
        ui.value_box("Median Warming", ui.output_ui("median_box"), 
                     showcase=icon_svg("temperature-half", fill="grey")),
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
    ui.include_css(app_dir / "styles.css"),
    title = "Warming Dashboard",
    fillable = True
)


def server(input, output, session):
    current_option = reactive.Value("°C")

    @reactive.Effect
    @reactive.event(input.toggle_button)
    def _():
        if current_option.get() == "°C":
            current_option.set("°F")
        else:
            current_option.set("°C")
        ui.update_action_button(
            "toggle_button", 
            label=current_option.get(), 
            #class_="btn-primary"
        )
    
    #@output
    #@render.text
    #def current_option_out():
    #    return f"Current option: {current_option.get()}"
    
    
    
    
    
    @reactive.calc
    def year_number():
        return input.year()

    @reactive.calc
    def scenario_name():
        #return list(input.scenario())
        return list(input.scenario()) + list(input.scenario_cmip7())

    @reactive.calc
    def filtered_df():
        return df[df["scenario"].isin(scenario_name())]

    @reactive.calc
    def year_df():
        return df[(df["scenario"].isin(scenario_name())) & (df["year"] == year_number())]

    def med_warming_text():
        ydf = year_df()
        lines = []
        for sname in scenario_name():
            filt_df = ydf[ydf["scenario"] == sname]
            swarm = f"{filt_df['warming'].median():.2f} °C"
            color = all_colors[sname]
            line = f'<div style="color: {color}; font-weight: bold; margin: 0; line-height: 1.2;">{swarm}</div>'
            lines.append(line)
        return "".join(lines)

    def exceedance_probability_text(level):
        lines = []
        for sname in scenario_name():
            filt_df = df[(df["scenario"] == sname) & (df["year"] == year_number())]
            prob = round((filt_df["warming"] > level).mean() * 100, 1)
            color = all_colors[sname]
            line = f'<div style="color: {color}; font-weight: bold; margin: 0; line-height: 1.2;">{prob:.1f} %</div>'
            lines.append(line)
        return "".join(lines)
    
    def plot_scenarios_plotly(ds):
       ds = ds[ds['year'].between(1850,2101)]
       x = ds.year.unique()
       
       def hex_to_rgb(hex_color):
           hex_color = hex_color.lstrip('#')
           return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

       fig = go.Figure()

       for scenario in ds.scenario.unique():
           for pp in ((0, 1.00, .2), (.05, .95, .3), (.16, .84, .4)): # lower CI, upper CI, alpha value
               ylower = ds[ds['scenario']==scenario].groupby('year')[['warming','year']].quantile(pp[0])['warming']
               yupper = ds[ds['scenario']==scenario].groupby('year')[['warming','year']].quantile(pp[1])['warming']
           
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
               y=ds[ds['scenario']==scenario].groupby('year')['warming'].median(),
               line_color=all_colors[scenario], 
               showlegend=False,
               name=scenario + ' Median',
               hovertemplate='<b>%{fullData.name}</b><br>year: %{x}<br>warming: %{y:.3f}<extra></extra>',
           ))
           
       # add final touches
       fig.add_hline(y=0, line_width=.5)
       fig.add_hline(y=1.5, line_width=.5)#,
                     #annotation_text='  1.5°C', annotation_position='top left')
       fig.add_hline(y=2, line_width=.5)#,
                     #annotation_text='  2°C', annotation_position='top left')
       fig.add_vline(x=year_number(), line_dash='dot', line_width=1,
                     annotation_text=str(year_number())+'  ', 
                     annotation_position="top left",
                     annotation_font_size=15,
                     annotation_textangle=-90)
       
       fig.update_traces(mode='lines')
       fig.update_layout(
           yaxis_title="warming",
           yaxis_ticksuffix="°C",
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
                histnorm="probability",
                xbins=dict(start=binbreaks[st_index], end=binbreaks[en_index], size=0.25),
                marker_color=all_colors[scenario],
                name=scenario + ', ' + str(year_number()),
                showlegend=False,
                hovertemplate='<b>%{fullData.name}</b><br>warming: %{x}°C<br>probability: %{y:.3f}<extra></extra>',
                ), row=2,col=1)
            
        fig.update_layout(
            #xaxis = dict(
            #    tickmode = 'array',
            #    tickvals = binbreaks[st_index:en_index],),
            #xaxis_title="warming (°C)",
            #yaxis_title="probability",
            width=600, height=525)
        
        # Update axis properties
        fig.update_yaxes(title_text='probability',row=2,col=1)
        fig.update_yaxes(showticklabels=False, row=1, col=1)
        fig.update_xaxes(title_text='warming (°C)',
            tickmode = 'array',tickvals = binbreaks[st_index:en_index], 
            row=2,col=1)
        
        return fig


    @reactive.effect
    @reactive.event(input.info_btn)
    def show_modal():
        ui.modal_show(
            ui.modal(
                "NGFS Scenarios Info",
                ui.tags.p("The ", ui.tags.a("NGFS (Network for Greening the Financial System) scenarios", href='https://www.ngfs.net/ngfs-scenarios-portal/', target='_blank'), " explore a range of climate policy and socioeconomic pathways."),
                ui.output_plot("info_plot"),
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
                "Preliminary CMIP7 Scenarios Info",
                ui.tags.p("The preliminary CMIP7 scenarios ", ui.tags.a("(more info here)", href='https://egusphere.copernicus.org/preprints/2025/egusphere-2024-3765/', target='_blank'), " ..."),
                #ui.output_plot("info_plot"),
                size='xl',
                easy_close=True,
                footer=ui.modal_button("Close"),
            )
        )

    @output
    @render.plot
    def info_plot():
        #plt.figure()
        fig, ax = plt.subplots(figsize=(9,6))
        #ax = 
        sns.lineplot(data=dfmed[dfmed['scenario'] in NGFS_scenarios], x="year", y="warming", hue="scenario", palette=NGFS_colors)
        ax.set_title("Median Warming by Scenario")
        ax.set_ylabel("Warming (°C)")
        ax.set_xlabel("Year")
        #fig.legend(loc='outside center right')
        ax.legend(loc='center right', bbox_to_anchor=(1.1, 0, .4, 1), frameon=False, borderaxespad=0.)
        #plt.subplots_adjust(right=1)
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
