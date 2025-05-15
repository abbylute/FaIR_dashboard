#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 15:39:05 2025

Combine data files from multiple scenario sources into one to use in fair app

@author: abbylute
"""
import pandas as pd

outdir = "/Users/abbylute/Documents/FaIR/FaIR_dashboard_data/"

fair_dir = "/Users/abbylute/Documents/FaIR/outputs/AL_V5/csv/"
df = pd.read_csv(fair_dir + "fair_warming.csv")
#dfmed = pd.read_csv(fair_dir + "fair_warming_scenario_medians.csv")
dfmed = pd.read_csv(fair_dir + "fair_warming_scenario_medians_exceedances.csv")
dfquant = pd.read_csv(fair_dir + "fair_warming_scenario_quantiles.csv")

cmip7_dir = "/Users/abbylute/Documents/FaIR/chrisroadmap-cmip7-scenariomip/output/csv/"
df_cmip7 = pd.read_csv(cmip7_dir + "fair_warming.csv")
#dfmed_cmip7 = pd.read_csv(cmip7_dir + "fair_warming_scenario_medians.csv")
dfmed_cmip7 = pd.read_csv(cmip7_dir + "fair_warming_scenario_medians_exceedances.csv")
dfquant_cmip7 = pd.read_csv(cmip7_dir + "fair_warming_scenario_quantiles.csv")


# Combine median files
dfmed_new = pd.concat([dfmed,dfmed_cmip7])
#dfmed_new.to_csv(outdir + 'fair_warming_scenario_medians.csv', index = False)
dfmed_new.to_csv(outdir + 'fair_warming_scenario_medians_exceedances.csv', index = False)

# Combine full files
df_cmip7['IAM'] = 'CMIP7'
df_new = pd.concat([df, df_cmip7])
df_new.to_csv(outdir + 'fair_warming.csv', index = False)

# combine quantile files
dfquant_new = pd.concat([dfquant, dfquant_cmip7])
dfquant_new.to_csv(outdir + 'fair_warming_scenario_quantiles.csv', index = False)
# TODO: could probably limit dfquant to years after 1849

