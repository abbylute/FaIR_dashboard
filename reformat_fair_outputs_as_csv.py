#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reformat FaIR outputs 
from: netcdfs for each iam with temperatures on time bounds
to: a single csv for all iams with annual warming amounts

Created on Wed Mar 26 11:50:35 2025

@author: abbylute
"""

import xarray as xr
import pandas as pd
import numpy as np

rawdir = '/Users/abbylute/Documents/FaIR/outputs/AL_V5/'
outdir = '/Users/abbylute/Documents/FaIR/outputs/AL_V5/csv/'



def calc_preindustrial_temp(dd):
    # array with 0.5 weights for 1850 and 1901 and 1.0 weights for all timebounds in between
    weights_51yr = np.ones(52)
    weights_51yr[0] = 0.5
    weights_51yr[-1] = 0.5

    return np.average(dd[dd['timebounds'].between(1850,1901)]['temperature'],
                      weights=weights_51yr,
                      axis=0)


def preprocess(x):
    fn = x['temperature'].encoding['source']
    iam = fn.split('_')[-2].split('/')[-1]
    x = x.assign_coords({'IAM':iam})
    x = x.expand_dims('IAM')
    x = x.sel(layer=0).drop_vars('layer')
    return x

x = xr.open_mfdataset(rawdir + "*temp.nc", preprocess=preprocess)


df = x.temperature.to_dataframe().reset_index()

preindustrial_temp = df.groupby(['IAM','scenario','config']
                                ).apply(calc_preindustrial_temp, 
                                        include_groups=False).reset_index(
                                            ).rename(columns={
                                                0:'preindustrial_temp'})
df = pd.merge(df,preindustrial_temp)
df['warming'] = df['temperature'] - df['preindustrial_temp']   
df = df.rename(columns={'timebounds':'year'}).drop(['temperature','preindustrial_temp'],axis=1)

# clean up scenario names
df = df.replace({'Delayed transition':'Delayed Transition','Low demand':'Low Demand'})

df.to_csv(outdir + 'fair_warming.csv', index=False)

# create dataframe of scenario medians:
df_median = df.groupby(['scenario','year']).warming.median().reset_index()
df_median = df_median[df_median['year']>=2000]
df_median['scenario'] = pd.Categorical(df_median['scenario'], 
                        categories=['Net Zero 2050','Low Demand','Below 2°C',
                                    'Delayed Transition','Fragmented World',
                                    'Nationally Determined Contributions (NDCs)',
                                    'Current Policies'], 
                        ordered=True)
df_median = df_median.sort_values('scenario')
df_median.to_csv(outdir + 'fair_warming_scenario_medians.csv', index=False)
