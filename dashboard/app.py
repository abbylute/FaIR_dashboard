import seaborn as sns
import matplotlib.pyplot as plt
#import plotly.figure_factory as ff
import numpy as np
import pandas as pd

from faicons import icon_svg
# search icons here: https://fontawesome.com/search?q=thermometer&o=r&ip=classic%2Cbrands

# Import data from shared.py
from shared import app_dir, df, dfmed
from shiny import reactive, render, App
from shiny.express import input, ui #render
from shinywidgets import render_widget#, output_widget  
#from shinywidgets import render_plotly
#import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


ui.page_opts(title="Warming Dashboard", fillable=True)

# dark mode toggle in navbar. This is supposed to work according to: https://shiny.posit.co/py/components/inputs/dark-mode/, but gives an error
#ui.nav_spacer()  
#with ui.nav_control():  
#    ui.input_dark_mode()  
    
    
NGFS_colors = {
    "Low Demand": "#00a9cf",#"#003466",#"#2274ae",
    "Net Zero 2050": "#2274ae",#"#00a9cf",
    "Below 2°C": "#003466",
    "Delayed Transition": "#92397a",
    "Fragmented World": "#b0724e",
    "Nationally Determined Contributions (NDCs)": "#f69320",
    "Current Policies": "#df0000",
}


pio.templates.default = "plotly_white"



# This is roughly working. Remaining issues:
    # - plot size changes when I go from a single to multiple scenarios
    # - consider changing plot background to maybe white, maybe w/o grid
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
            rgb_color = hex_to_rgb(NGFS_colors[scenario])
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
                hoverlabel=dict(bgcolor=NGFS_colors[scenario])
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
                hoverlabel=dict(bgcolor=NGFS_colors[scenario])
                ))
        
        # add median line
        fig.add_trace(go.Scatter(
            x=x, 
            y=ds[ds['scenario']==scenario].groupby('year')['warming'].median(),
            line_color=NGFS_colors[scenario], 
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
    scens = [n for n in list(NGFS_colors.keys()) if n in scens]
    for scenario in scens:
        ydf = year_df()
        
        fig.add_trace(go.Box(x=ydf[ydf['scenario']==scenario]['warming'], 
                      marker_color=NGFS_colors[scenario],
                      name=scenario,
                      showlegend=False),
                      row=1, col=1)

        fig.add_trace(go.Histogram(
            x=ydf[ydf['scenario']==scenario]['warming'], 
            histnorm="probability",
            xbins=dict(start=binbreaks[st_index], end=binbreaks[en_index], size=0.25),
            marker_color=NGFS_colors[scenario],
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



with ui.sidebar(title="Options",width=400):

    #with ui.card(full_screen=False):
    #    ui.card_header("Median Warming Trajectories")
    
    # Dark mode option. Would be better to put this in upper right if possible.
    # but, dark mode doesn't look very good anyway, unless maybe we change the colors and the plot backgrounds and line colors
    # see here for inspiration: https://climatechangetracker.org/global-warming
    # I think there's a way to get a variable from the line below so that we could better control plot backgrounds, etc depending on the user selection
    #ui.input_dark_mode()  

    @render.plot(width=370,height=300)
    def scenario_medians():
        plt.figure()
        ax1= sns.lineplot(
            data=dfmed,
            x="year",
            y="warming",
            hue="scenario",
            palette=NGFS_colors,
            legend=False,
        )
        ax1.set(ylabel='median warming')
        ax1.set(xlabel=None)
        ax1.tick_params(axis='y', direction='in', pad=-20)
        #plt.tight_layout()
        #ax1.layout(extent=[0.1, 0.1, 0.9, 0.9])
        return ax1
        
    
    ui.input_slider("year", "Year", 2000, 2100, 2030)
    
    ui.tags.div(
        ui.tags.span("NGFS Scenarios", class_="me-2 fw-bold"),
        ui.input_action_button("info_btn", "", icon=icon_svg("circle-info")),
        class_="d-flex align-items-center mb-2"
    )
    ui.input_checkbox_group(
        "scenario",
        "",#"NGFS Scenarios",
        {
            "Low Demand": ui.span("Low Demand", style="color: " + NGFS_colors["Low Demand"] + "; font-weight: bold;"),
            "Net Zero 2050": ui.span("Net Zero 2050", style="color: "+ NGFS_colors["Net Zero 2050"] + "; font-weight: bold;"),
            "Below 2°C": ui.span("Below 2°C", style="color: " + NGFS_colors["Below 2°C"] + "; font-weight: bold;"),
            "Delayed Transition": ui.span("Delayed Transition", style="color: " + NGFS_colors["Delayed Transition"] + "; font-weight: bold;"),
            "Fragmented World": ui.span("Fragmented World", style="color: " + NGFS_colors["Fragmented World"] + "; font-weight: bold;"),
            "Nationally Determined Contributions (NDCs)": ui.span("Nationally Determined Contributions (NDCs)", style="color: "+NGFS_colors["Nationally Determined Contributions (NDCs)"]+"; font-weight: bold;"),
            "Current Policies": ui.span("Current Policies", style="color: "+NGFS_colors["Current Policies"] + "; font-weight: bold;"),
        },
        selected=["Current Policies"] 
    )
    ui.input_action_button("go","Calculate")


    
with ui.layout_column_wrap(fill=False):
    with ui.value_box(class_="custom-value-box", showcase=icon_svg("temperature-half", fill="grey")):#fill="color: #545659;")):
        "Median Warming"# + str(input.year())
        
        @render.ui
        @reactive.event(input.go, ignore_none=False)
        def median_warming_C():
            return ui.HTML(med_warming_text())

    with ui.value_box(class_="custom-value-box", showcase=icon_svg("fire")):
        "Probability of Exceeding 1.5°C"

        @render.ui
        @reactive.event(input.go, ignore_none=False)
        def probability_15():
            return ui.HTML(exceedance_probability_text(1.5))

    with ui.value_box(class_="custom-value-box", showcase=icon_svg("dumpster-fire")):
        "Probability of Exceeding 2.0°C"

        @render.ui
        @reactive.event(input.go, ignore_none=False)
        def probability_2():
            return ui.HTML(exceedance_probability_text(2))


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Warming Timeseries")
        
        @render_widget(width=600,height=600)
        @reactive.event(input.go, ignore_none=False)
        def timeseries():
            return plot_scenarios_plotly(filtered_df())

    with ui.card(full_screen=True):
        ui.card_header("Warming Possibilities" )

        @render_widget(width=600,height=600) # this also does not keep the plot from changing size when scenarios are added
        @reactive.event(input.go, ignore_none=False)
        def year_warming_dist():
            return plot_year_warming_probabilities_plotly()



ui.include_css(app_dir / "styles.css")



@reactive.calc
def year_number():
    return input.year()
def scenario_name():
    return list(input.scenario())
def filtered_df():
    filt_df = df[df["scenario"].isin(input.scenario())]
    #filt_df = filt_df.loc[filt_df["year"].between(2000,input.year()+1)]# <= input.year()]
    return filt_df
def year_df():
    filt_df = df[df["scenario"].isin(input.scenario())]
    filt_df = filt_df.loc[filt_df["year"] == input.year()]
    return filt_df


def med_warming_text():
    ydf = year_df()
    lines = []
    for sname in scenario_name():
        filt_df = ydf[ydf['scenario'] == sname]
        swarm = f"{filt_df['warming'].median():.2f} °C"
        # to color lines by scenario use the following three lines:
        color= NGFS_colors[sname]
        line = f'<div style="color: {color}; font-weight: bold; margin: 0; line-height: 1.2;">{swarm}</div>'
        lines.append(line)
        # otherwise just use this one line:
        #lines.append(f"{sname}: {swarm}")
    return "".join(lines)#"<br>".join(lines)  # HTML line breaks
    
    
def exceedance_probability_text(level):
    lines = []
    for sname in scenario_name():        
        filt_df = df[df["scenario"]==sname]
        filt_df = filt_df.loc[filt_df["year"] == input.year()]
        med_warming_15 = round((filt_df['warming']>level).mean()*100,1)    
        
        swarm = f"{med_warming_15:.1f} %"
        color= NGFS_colors[sname]
        line = f'<div style="color: {color}; font-weight: bold; margin: 0; line-height: 1.2;">{swarm}</div>'
        lines.append(line)
    return "".join(lines)


def med_warming_2():
    filt_df = df[df["scenario"].isin(input.scenario())]
    filt_df = filt_df.loc[filt_df["year"] == input.year()]
    med_warming_2 = round((filt_df['warming']>2).mean()*100,1)    
    return med_warming_2
def data_for_dist_plot():
    df1 = df[(df.scenario.isin([input.scenario()])) & (df.year == input.year())]
    scens = df1['scenario'].unique()
    #mylist=[]
    #for s in scens:
    #    mylist.append(df1[df1.scenario==s]['warming'].values)
    #return scens, mylist
    newdf = pd.DataFrame()
    for s in scens:
        newdf[s] = df1[df1.scenario==s]['warming'].values
    newdf = newdf.reset_index(drop=True) # this doesn't seem to fix it
    # Why does the below data work but the above data doesn't?
   # newdf = pd.DataFrame({'2012': np.random.randn(200)})#,
#                   '2013': np.random.randn(200)+1})
    return newdf


def server(input):
    @reactive.effect
    @reactive.event(input.info_btn)
    def _():
        ui.modal_show(
            ui.modal(
                "NGFS Scenario Info",
                ui.tags.p("The NGFS (Network for Greening the Financial System) scenarios explore a range of climate policy and socioeconomic pathways."),
                ui.output_plot("info_plot"),
                easy_close=True,
                footer=ui.modal_button("Close")
            )
        )

    @render.plot
    def info_plot():
        plt.figure()
        ax = sns.lineplot(data=dfmed, x="year", y="warming", hue="scenario", palette=NGFS_colors)
        ax.set_title("Median Warming by Scenario")
        ax.set_ylabel("Warming (°C)")
        ax.set_xlabel("Year")
        return ax

# Attach the UI and server
app = App(ui=ui, server=server)
