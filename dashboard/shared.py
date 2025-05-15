from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
#df = pd.read_csv(app_dir / "fair_warming.csv")

#fair_dir = "/Users/abbylute/Documents/FaIR/outputs/AL_V5/csv/"
#df = pd.read_csv(fair_dir + "fair_warming.csv")
#dfmed = pd.read_csv(fair_dir + "fair_warming_scenario_medians.csv")

#cmip7_dir = "/Users/abbylute/Documents/FaIR/chrisroadmap-cmip7-scenariomip/output/csv/"
#df_cmip7 = pd.read_csv(cmip7_dir + "fair_warming.csv")
#dfmed_cmip7 = pd.read_csv(cmip7_dir + "fair_warming_scenario_medians.csv")

data_dir =  "/Users/abbylute/Documents/FaIR/FaIR_dashboard_data/"
df = pd.read_csv(data_dir + "fair_warming.csv")
dfmed = pd.read_csv(data_dir + "fair_warming_scenario_medians_exceedances.csv")
dfquant = pd.read_csv(data_dir + "fair_warming_scenario_quantiles.csv")