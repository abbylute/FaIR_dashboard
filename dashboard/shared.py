from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
#df = pd.read_csv(app_dir / "fair_warming.csv")

fair_dir = "/Users/abbylute/Documents/FaIR/outputs/AL_V5/csv/"
df = pd.read_csv(fair_dir + "fair_warming.csv")
dfmed = pd.read_csv(fair_dir + "fair_warming_scenario_medians.csv")
